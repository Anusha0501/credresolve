import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import ChatInterface from './pages/ChatInterface'
import MemoryViewer from './pages/MemoryViewer'
import MetricsViewer from './pages/MetricsViewer'
import KnowledgeBaseViewer from './pages/KnowledgeBaseViewer'
import ToolLogsViewer from './pages/ToolLogsViewer'
import { MessageSquare, Database, BarChart3, BookOpen, Wrench, Home } from 'lucide-react'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-primary text-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center space-x-2">
                <MessageSquare className="w-8 h-8" />
                <span className="text-xl font-bold">CredResolve AI</span>
              </div>
              <div className="flex space-x-4">
                <Link to="/" className="flex items-center space-x-1 hover:text-gray-200">
                  <Home className="w-5 h-5" />
                  <span>Dashboard</span>
                </Link>
                <Link to="/chat" className="flex items-center space-x-1 hover:text-gray-200">
                  <MessageSquare className="w-5 h-5" />
                  <span>Chat</span>
                </Link>
                <Link to="/memory" className="flex items-center space-x-1 hover:text-gray-200">
                  <Database className="w-5 h-5" />
                  <span>Memory</span>
                </Link>
                <Link to="/metrics" className="flex items-center space-x-1 hover:text-gray-200">
                  <BarChart3 className="w-5 h-5" />
                  <span>Metrics</span>
                </Link>
                <Link to="/knowledge" className="flex items-center space-x-1 hover:text-gray-200">
                  <BookOpen className="w-5 h-5" />
                  <span>Knowledge</span>
                </Link>
                <Link to="/tools" className="flex items-center space-x-1 hover:text-gray-200">
                  <Wrench className="w-5 h-5" />
                  <span>Tools</span>
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/chat" element={<ChatInterface />} />
            <Route path="/memory" element={<MemoryViewer />} />
            <Route path="/metrics" element={<MetricsViewer />} />
            <Route path="/knowledge" element={<KnowledgeBaseViewer />} />
            <Route path="/tools" element={<ToolLogsViewer />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
