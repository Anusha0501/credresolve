import React, { useState, useRef, useEffect } from 'react'
import { chatAPI } from '../services/api'
import { Mic, MicOff, Volume2, Send, Phone, MessageSquare } from 'lucide-react'

function ChatInterface() {
  const [phoneNumber, setPhoneNumber] = useState('')
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([])
  const [currentState, setCurrentState] = useState('')
  const [toolCalls, setToolCalls] = useState([])
  const [customerData, setCustomerData] = useState(null)
  const [isListening, setIsListening] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)

  const recognitionRef = useRef(null)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
      recognitionRef.current = new SpeechRecognition()
      recognitionRef.current.continuous = false
      recognitionRef.current.interimResults = false
      recognitionRef.current.lang = 'hi-IN'

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript
        setMessage(transcript)
        setIsListening(false)
      }

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error)
        setIsListening(false)
      }

      recognitionRef.current.onend = () => {
        setIsListening(false)
      }
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
    }
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const startListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.start()
      setIsListening(true)
    }
  }

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop()
      setIsListening(false)
    }
  }

  const speakResponse = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = 'hi-IN'
      utterance.onstart = () => setIsSpeaking(true)
      utterance.onend = () => setIsSpeaking(false)
      window.speechSynthesis.speak(utterance)
    }
  }

  const handleSendMessage = async () => {
    if (!phoneNumber || !message.trim()) return

    const userMessage = message
    setMessage('')
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])

    try {
      const response = await chatAPI.sendMessage(phoneNumber, userMessage, 'hindi')
      
      setMessages(prev => [...prev, { role: 'assistant', content: response.response }])
      setCurrentState(response.current_state)
      setToolCalls(response.tool_calls || [])
      setCustomerData(response.customer_data)
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, there was an error processing your request.' }])
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4 flex items-center">
          <MessageSquare className="w-6 h-6 mr-2" />
          Chat Interface
        </h2>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Phone Number
          </label>
          <input
            type="text"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            placeholder="+919876543210"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
          />
          <p className="text-sm text-gray-500 mt-1">
            Try: +919876543210, +919123456789, or +919876543211
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white p-6 rounded-lg shadow-md">
          <div className="h-96 overflow-y-auto mb-4 space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 py-8">
                Start a conversation by typing a message or using voice input
              </div>
            )}
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] p-3 rounded-lg ${
                    msg.role === 'user'
                      ? 'bg-primary text-white'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <div className="flex space-x-2">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
            <button
              onClick={isListening ? stopListening : startListening}
              className={`px-4 py-2 rounded-lg ${
                isListening ? 'bg-red-500' : 'bg-gray-200'
              } hover:opacity-80 transition-opacity`}
              title={isListening ? 'Stop listening' : 'Start voice input'}
            >
              {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
            </button>
            <button
              onClick={handleSendMessage}
              disabled={!message.trim()}
              className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-secondary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>

        <div className="space-y-4">
          {customerData && (
            <div className="bg-white p-4 rounded-lg shadow-md">
              <h3 className="font-semibold mb-2 flex items-center">
                <Phone className="w-4 h-4 mr-2" />
                Customer Data
              </h3>
              <div className="text-sm space-y-1">
                <p><strong>Name:</strong> {customerData.name}</p>
                <p><strong>Due:</strong> ₹{customerData.due_amount?.toLocaleString()}</p>
                <p><strong>Loan Type:</strong> {customerData.loan_type}</p>
                <p><strong>Risk:</strong> {customerData.risk_category}</p>
              </div>
            </div>
          )}

          {currentState && (
            <div className="bg-white p-4 rounded-lg shadow-md">
              <h3 className="font-semibold mb-2">Current State</h3>
              <p className="text-sm bg-blue-100 px-3 py-1 rounded inline-block">
                {currentState}
              </p>
            </div>
          )}

          {toolCalls.length > 0 && (
            <div className="bg-white p-4 rounded-lg shadow-md">
              <h3 className="font-semibold mb-2">Tool Calls</h3>
              <div className="space-y-2 text-sm">
                {toolCalls.map((call, index) => (
                  <div key={index} className="bg-gray-50 p-2 rounded">
                    <p><strong>Tool:</strong> {call.tool}</p>
                    <p><strong>Function:</strong> {call.function}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {messages.length > 0 && (
            <button
              onClick={() => speakResponse(messages[messages.length - 1].content)}
              disabled={isSpeaking}
              className="w-full px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 flex items-center justify-center"
            >
              <Volume2 className="w-5 h-5 mr-2" />
              Speak Last Response
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default ChatInterface
