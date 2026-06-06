import React, { useState } from 'react'
import { toolAPI } from '../services/api'
import { Wrench, Play, CheckCircle, XCircle } from 'lucide-react'

function ToolLogsViewer() {
  const [toolName, setToolName] = useState('crm')
  const [functionName, setFunctionName] = useState('fetch_customer_data')
  const [parameters, setParameters] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const toolFunctions = {
    crm: ['fetch_customer_data', 'get_customer_summary'],
    payment: ['calculate_settlement', 'calculate_emi_restructuring'],
    ticket: ['create_ticket', 'get_tickets'],
    sms: ['send_reminder', 'send_confirmation']
  }

  const handleCallTool = async () => {
    setLoading(true)
    try {
      let parsedParams = {}
      if (parameters) {
        try {
          parsedParams = JSON.parse(parameters)
        } catch (e) {
          parsedParams = { phone_number: parameters }
        }
      }

      const response = await toolAPI.callTool(toolName, functionName, parsedParams)
      setResult(response)
    } catch (error) {
      console.error('Error calling tool:', error)
      setResult({ success: false, result: { error: str(error) } })
    } finally {
      setLoading(false)
    }
  }

  const handleToolChange = (newTool) => {
    setToolName(newTool)
    setFunctionName(toolFunctions[newTool][0])
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4 flex items-center">
          <Wrench className="w-6 h-6 mr-2" />
          Tool Logs Viewer
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tool
            </label>
            <select
              value={toolName}
              onChange={(e) => handleToolChange(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              <option value="crm">CRM Tool</option>
              <option value="payment">Payment Tool</option>
              <option value="ticket">Ticket Tool</option>
              <option value="sms">SMS Tool</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Function
            </label>
            <select
              value={functionName}
              onChange={(e) => setFunctionName(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              {toolFunctions[toolName].map(func => (
                <option key={func} value={func}>{func}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Parameters (JSON or phone number)
          </label>
          <input
            type="text"
            value={parameters}
            onChange={(e) => setParameters(e.target.value)}
            placeholder='{"phone_number": "+919876543210"} or just +919876543210'
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
          />
        </div>

        <button
          onClick={handleCallTool}
          disabled={loading}
          className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-secondary disabled:opacity-50 flex items-center"
        >
          {loading ? 'Calling...' : <><Play className="w-5 h-5 mr-2" /> Call Tool</>}
        </button>
      </div>

      {result && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center space-x-2 mb-4">
            {result.success ? (
              <CheckCircle className="w-6 h-6 text-green-500" />
            ) : (
              <XCircle className="w-6 h-6 text-red-500" />
            )}
            <h3 className="text-xl font-semibold">Tool Result</h3>
          </div>
          <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm">
            {JSON.stringify(result.result, null, 2)}
          </pre>
        </div>
      )}

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-xl font-semibold mb-4">Tool Descriptions</h3>
        <div className="space-y-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-semibold mb-2">CRM Tool</h4>
            <p className="text-sm text-gray-600">Fetch customer data including name, due amount, loan type, and risk category.</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-semibold mb-2">Payment Tool</h4>
            <p className="text-sm text-gray-600">Calculate settlement amounts, EMI restructuring, and outstanding balances.</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-semibold mb-2">Ticket Tool</h4>
            <p className="text-sm text-gray-600">Create and manage support tickets for escalations and disputes.</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <h4 className="font-semibold mb-2">SMS Tool</h4>
            <p className="text-sm text-gray-600">Send reminder and confirmation SMS messages to borrowers.</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ToolLogsViewer
