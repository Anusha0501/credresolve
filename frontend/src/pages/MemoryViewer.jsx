import React, { useState } from 'react'
import { memoryAPI } from '../services/api'
import { Database, Clock, User, FileText } from 'lucide-react'

function MemoryViewer() {
  const [phoneNumber, setPhoneNumber] = useState('')
  const [memoryData, setMemoryData] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleFetchMemory = async () => {
    if (!phoneNumber) return

    setLoading(true)
    try {
      const data = await memoryAPI.getMemory(phoneNumber)
      setMemoryData(data)
    } catch (error) {
      console.error('Error fetching memory:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4 flex items-center">
          <Database className="w-6 h-6 mr-2" />
          Memory Viewer
        </h2>

        <div className="flex space-x-4">
          <input
            type="text"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            placeholder="Enter phone number (+919876543210)"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
          />
          <button
            onClick={handleFetchMemory}
            disabled={loading || !phoneNumber}
            className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-secondary disabled:opacity-50"
          >
            {loading ? 'Loading...' : 'Fetch Memory'}
          </button>
        </div>
      </div>

      {memoryData && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {memoryData.user_memory && (
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <User className="w-5 h-5 mr-2" />
                User Memory
              </h3>
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-gray-500">Phone Number</p>
                  <p className="font-medium">{memoryData.user_memory.phone_number}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Preferred Callback Time</p>
                  <p className="font-medium">{memoryData.user_memory.preferred_callback_time || 'Not set'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Settlement Preference</p>
                  <p className="font-medium">{memoryData.user_memory.settlement_preference || 'Not set'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Language</p>
                  <p className="font-medium">{memoryData.user_memory.language}</p>
                </div>
              </div>
            </div>
          )}

          {memoryData.promises_to_pay && memoryData.promises_to_pay.length > 0 && (
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <Clock className="w-5 h-5 mr-2" />
                Promises to Pay
              </h3>
              <div className="space-y-3">
                {memoryData.promises_to_pay.map((promise, index) => (
                  <div key={index} className="bg-gray-50 p-3 rounded">
                    <p><strong>Amount:</strong> ₹{promise.amount?.toLocaleString()}</p>
                    <p><strong>Promise Date:</strong> {promise.promise_date}</p>
                    <p><strong>Status:</strong> {promise.status}</p>
                    <p className="text-sm text-gray-500">Created: {promise.created_at}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {memoryData.conversation_history && memoryData.conversation_history.length > 0 && (
            <div className="bg-white p-6 rounded-lg shadow-md lg:col-span-2">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <FileText className="w-5 h-5 mr-2" />
                Conversation History
              </h3>
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {memoryData.conversation_history.map((conv, index) => (
                  <div key={index} className="border-l-4 border-primary pl-4">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="text-sm font-medium bg-blue-100 px-2 py-1 rounded">
                        {conv.state}
                      </span>
                      <span className="text-sm text-gray-500">{conv.timestamp}</span>
                    </div>
                    <div className="bg-gray-50 p-3 rounded mb-2">
                      <p className="text-sm text-gray-500">User:</p>
                      <p>{conv.message}</p>
                    </div>
                    <div className="bg-blue-50 p-3 rounded">
                      <p className="text-sm text-gray-500">Agent:</p>
                      <p>{conv.response}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {memoryData && !memoryData.user_memory && !memoryData.conversation_history?.length && (
        <div className="bg-white p-6 rounded-lg shadow-md text-center text-gray-500">
          No memory data found for this phone number
        </div>
      )}
    </div>
  )
}

export default MemoryViewer
