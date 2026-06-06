import React from 'react'
import { Link } from 'react-router-dom'
import { MessageSquare, Database, BarChart3, BookOpen, Wrench, Phone, Zap, Shield } from 'lucide-react'

function Dashboard() {
  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">CredResolve AI</h1>
        <p className="text-gray-600 text-lg">Intelligent Debt Collection Agent</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Link to="/chat" className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
          <MessageSquare className="w-12 h-12 text-primary mb-4" />
          <h3 className="text-xl font-semibold mb-2">Chat Interface</h3>
          <p className="text-gray-600">Interact with the AI agent using text or voice</p>
        </Link>

        <Link to="/memory" className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
          <Database className="w-12 h-12 text-primary mb-4" />
          <h3 className="text-xl font-semibold mb-2">Memory Viewer</h3>
          <p className="text-gray-600">View user memory and conversation history</p>
        </Link>

        <Link to="/metrics" className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
          <BarChart3 className="w-12 h-12 text-primary mb-4" />
          <h3 className="text-xl font-semibold mb-2">Metrics</h3>
          <p className="text-gray-600">Monitor system performance and analytics</p>
        </Link>

        <Link to="/knowledge" className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
          <BookOpen className="w-12 h-12 text-primary mb-4" />
          <h3 className="text-xl font-semibold mb-2">Knowledge Base</h3>
          <p className="text-gray-600">Browse RAG knowledge base documents</p>
        </Link>

        <Link to="/tools" className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
          <Wrench className="w-12 h-12 text-primary mb-4" />
          <h3 className="text-xl font-semibold mb-2">Tool Logs</h3>
          <p className="text-gray-600">View tool call history and results</p>
        </Link>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flex items-start space-x-3">
            <Phone className="w-6 h-6 text-primary mt-1" />
            <div>
              <h4 className="font-semibold">Voice Interaction</h4>
              <p className="text-gray-600 text-sm">Hindi and Hinglish speech support</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <Zap className="w-6 h-6 text-primary mt-1" />
            <div>
              <h4 className="font-semibold">LangGraph Workflows</h4>
              <p className="text-gray-600 text-sm">11-state intelligent agent</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <Shield className="w-6 h-6 text-primary mt-1" />
            <div>
              <h4 className="font-semibold">RBI Compliant</h4>
              <p className="text-gray-600 text-sm">Ethical debt collection practices</p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Quick Start</h2>
        <ol className="list-decimal list-inside space-y-2 text-gray-700">
          <li>Navigate to the <strong>Chat Interface</strong> to start a conversation</li>
          <li>Enter a phone number (try: +919876543210, +919123456789, or +919876543211)</li>
          <li>Type your message or use voice input</li>
          <li>Watch the agent navigate through states and use tools</li>
          <li>Check <strong>Memory Viewer</strong> to see conversation history</li>
          <li>Visit <strong>Metrics</strong> to monitor system performance</li>
        </ol>
      </div>
    </div>
  )
}

export default Dashboard
