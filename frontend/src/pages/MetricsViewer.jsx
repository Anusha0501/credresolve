import React, { useState, useEffect } from 'react'
import { metricsAPI } from '../services/api'
import { BarChart3, Activity, Clock, CheckCircle, AlertCircle } from 'lucide-react'

function MetricsViewer() {
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMetrics()
    const interval = setInterval(fetchMetrics, 5000) // Refresh every 5 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchMetrics = async () => {
    try {
      const data = await metricsAPI.getMetrics()
      setMetrics(data)
    } catch (error) {
      console.error('Error fetching metrics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md text-center">
        <p>Loading metrics...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4 flex items-center">
          <BarChart3 className="w-6 h-6 mr-2" />
          System Metrics
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between mb-2">
            <Activity className="w-8 h-8 text-primary" />
            <span className="text-sm text-gray-500">Total Conversations</span>
          </div>
          <p className="text-3xl font-bold">
            {metrics?.counters?.conversation_end || 0}
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between mb-2">
            <CheckCircle className="w-8 h-8 text-green-500" />
            <span className="text-sm text-gray-500">Resolutions</span>
          </div>
          <p className="text-3xl font-bold">
            {metrics?.counters?.resolution || 0}
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between mb-2">
            <AlertCircle className="w-8 h-8 text-orange-500" />
            <span className="text-sm text-gray-500">Escalations</span>
          </div>
          <p className="text-3xl font-bold">
            {metrics?.counters?.escalation || 0}
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between mb-2">
            <Clock className="w-8 h-8 text-blue-500" />
            <span className="text-sm text-gray-500">Tool Calls</span>
          </div>
          <p className="text-3xl font-bold">
            {metrics?.counters?.tool_call || 0}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">State Transitions</h3>
          <div className="space-y-2">
            {Object.entries(metrics?.counters || {}).map(([key, value]) => {
              if (key.startsWith('state_')) {
                return (
                  <div key={key} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                    <span className="text-sm">{key.replace('state_', '')}</span>
                    <span className="font-semibold">{value}</span>
                  </div>
                )
              }
              return null
            })}
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">Recent Events</h3>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {Object.entries(metrics?.recent_metrics || {}).map(([key, events]) => (
              <div key={key} className="mb-4">
                <p className="font-semibold text-sm mb-1">{key}</p>
                {events.slice(-3).map((event, index) => (
                  <div key={index} className="text-xs text-gray-600 p-2 bg-gray-50 rounded">
                    <p>{event.timestamp}</p>
                    {event.metadata && Object.keys(event.metadata).length > 0 && (
                      <pre className="mt-1 text-xs">{JSON.stringify(event.metadata, null, 2)}</pre>
                    )}
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default MetricsViewer
