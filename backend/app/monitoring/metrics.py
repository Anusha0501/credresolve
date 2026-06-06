import time
from typing import Dict, List
from collections import defaultdict
from datetime import datetime

class MetricsTracker:
    """Track and store application metrics"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.counters = defaultdict(int)
        self.start_times = {}
    
    def track_metric(self, metric_name: str, metadata: Dict = None):
        """Track a metric event"""
        timestamp = datetime.now().isoformat()
        self.metrics[metric_name].append({
            "timestamp": timestamp,
            "metadata": metadata or {}
        })
        self.counters[metric_name] += 1
    
    def start_timer(self, operation: str):
        """Start a timer for an operation"""
        self.start_times[operation] = time.time()
    
    def end_timer(self, operation: str) -> float:
        """End a timer and return duration"""
        if operation in self.start_times:
            duration = time.time() - self.start_times[operation]
            self.track_metric(f"{operation}_latency", {"duration": duration})
            del self.start_times[operation]
            return duration
        return 0.0
    
    def get_metrics_summary(self) -> Dict:
        """Get summary of all metrics"""
        summary = {
            "counters": dict(self.counters),
            "recent_metrics": {}
        }
        
        # Get recent metrics (last 10)
        for metric_name, events in self.metrics.items():
            summary["recent_metrics"][metric_name] = events[-10:] if events else []
        
        return summary
    
    def get_metric_count(self, metric_name: str) -> int:
        """Get count for a specific metric"""
        return self.counters.get(metric_name, 0)
    
    def get_average_latency(self, operation: str) -> float:
        """Calculate average latency for an operation"""
        latency_events = self.metrics.get(f"{operation}_latency", [])
        if not latency_events:
            return 0.0
        
        total_duration = sum(event["metadata"].get("duration", 0) for event in latency_events)
        return total_duration / len(latency_events)
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.metrics.clear()
        self.counters.clear()
        self.start_times.clear()

# Global instance
metrics_tracker = MetricsTracker()

def track_metric(metric_name: str, metadata: Dict = None):
    """Convenience function to track metrics"""
    metrics_tracker.track_metric(metric_name, metadata)
