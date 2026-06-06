import React, { useState } from 'react'
import { knowledgeAPI } from '../services/api'
import { BookOpen, Search, FileText } from 'lucide-react'

function KnowledgeBaseViewer() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  const handleSearch = async () => {
    if (!query.trim()) return

    setLoading(true)
    try {
      const data = await knowledgeAPI.retrieve(query, 3)
      setResults(data.results || [])
    } catch (error) {
      console.error('Error searching knowledge base:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4 flex items-center">
          <BookOpen className="w-6 h-6 mr-2" />
          Knowledge Base Viewer
        </h2>

        <div className="flex space-x-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Search knowledge base (e.g., 'settlement policy', 'RBI guidelines')"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
          />
          <button
            onClick={handleSearch}
            disabled={loading || !query.trim()}
            className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-secondary disabled:opacity-50 flex items-center"
          >
            {loading ? 'Searching...' : <><Search className="w-5 h-5 mr-2" /> Search</>}
          </button>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-xl font-semibold mb-4">Available Documents</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            'rbi_collection_guidelines.md',
            'settlement_policy.md',
            'payment_dispute_policy.md',
            'escalation_policy.md',
            'faq.md'
          ].map((doc, index) => (
            <div key={index} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              <FileText className="w-5 h-5 text-primary" />
              <span className="text-sm">{doc}</span>
            </div>
          ))}
        </div>
      </div>

      {results.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">Search Results ({results.length})</h3>
          <div className="space-y-4">
            {results.map((result, index) => (
              <div key={index} className="border-l-4 border-primary pl-4">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-sm font-medium bg-blue-100 px-2 py-1 rounded">
                    Source: {result.metadata?.source || 'Unknown'}
                  </span>
                  <span className="text-sm text-gray-500">
                    Distance: {result.distance?.toFixed(4)}
                  </span>
                </div>
                <p className="text-gray-700">{result.content}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {query && results.length === 0 && !loading && (
        <div className="bg-white p-6 rounded-lg shadow-md text-center text-gray-500">
          No results found for "{query}"
        </div>
      )}
    </div>
  )
}

export default KnowledgeBaseViewer
