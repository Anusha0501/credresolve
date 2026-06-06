import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
import json

class MemoryDatabase:
    def __init__(self, db_path: str = "credresolve.db"):
        self.db_path = db_path
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User memory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT UNIQUE,
                preferred_callback_time TEXT,
                settlement_preference TEXT,
                language TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Conversation memory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT,
                state TEXT,
                message TEXT,
                response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        """)
        
        # Promises to pay table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS promises_to_pay (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT,
                amount REAL,
                promise_date DATE,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_user_memory(self, phone_number: str, data: Dict) -> bool:
        """Save or update user memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO user_memory 
                (phone_number, preferred_callback_time, settlement_preference, language, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                phone_number,
                data.get('preferred_callback_time'),
                data.get('settlement_preference'),
                data.get('language', 'hindi'),
                datetime.now().isoformat()
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving user memory: {e}")
            return False
        finally:
            conn.close()
    
    def get_user_memory(self, phone_number: str) -> Optional[Dict]:
        """Retrieve user memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT phone_number, preferred_callback_time, settlement_preference, language
                FROM user_memory WHERE phone_number = ?
            """, (phone_number,))
            row = cursor.fetchone()
            
            if row:
                return {
                    'phone_number': row[0],
                    'preferred_callback_time': row[1],
                    'settlement_preference': row[2],
                    'language': row[3]
                }
            return None
        except Exception as e:
            print(f"Error getting user memory: {e}")
            return None
        finally:
            conn.close()
    
    def save_conversation(self, phone_number: str, state: str, message: str, response: str, metadata: Dict = None) -> bool:
        """Save conversation turn"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO conversation_memory 
                (phone_number, state, message, response, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                phone_number,
                state,
                message,
                response,
                json.dumps(metadata) if metadata else None
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
        finally:
            conn.close()
    
    def get_conversation_history(self, phone_number: str, limit: int = 10) -> List[Dict]:
        """Retrieve conversation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT state, message, response, timestamp, metadata
                FROM conversation_memory 
                WHERE phone_number = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (phone_number, limit))
            rows = cursor.fetchall()
            
            return [
                {
                    'state': row[0],
                    'message': row[1],
                    'response': row[2],
                    'timestamp': row[3],
                    'metadata': json.loads(row[4]) if row[4] else None
                }
                for row in rows
            ]
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []
        finally:
            conn.close()
    
    def save_promise_to_pay(self, phone_number: str, amount: float, promise_date: str) -> bool:
        """Save promise to pay"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO promises_to_pay 
                (phone_number, amount, promise_date)
                VALUES (?, ?, ?)
            """, (phone_number, amount, promise_date))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving promise: {e}")
            return False
        finally:
            conn.close()
    
    def get_promises_to_pay(self, phone_number: str) -> List[Dict]:
        """Retrieve promises to pay"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT amount, promise_date, status, created_at
                FROM promises_to_pay 
                WHERE phone_number = ?
                ORDER BY created_at DESC
            """, (phone_number,))
            rows = cursor.fetchall()
            
            return [
                {
                    'amount': row[0],
                    'promise_date': row[1],
                    'status': row[2],
                    'created_at': row[3]
                }
                for row in rows
            ]
        except Exception as e:
            print(f"Error getting promises: {e}")
            return []
        finally:
            conn.close()

# Global instance
memory_db = MemoryDatabase()
