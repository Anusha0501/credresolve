import React, { useState, useRef, useEffect } from 'react'
import { Mic, MicOff, Upload, Play, Phone, MessageSquare, Volume2, FileAudio } from 'lucide-react'

function VoiceChat() {
  const [phoneNumber, setPhoneNumber] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [response, setResponse] = useState('')
  const [audioUrl, setAudioUrl] = useState('')
  const [currentState, setCurrentState] = useState('')
  const [toolsUsed, setToolsUsed] = useState<any[]>([])
  const [sources, setSources] = useState<any[]>([])
  const [latency, setLatency] = useState<any>(null)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])
  const audioRef = useRef<HTMLAudioElement>(null)

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorderRef.current = new MediaRecorder(stream)
      audioChunksRef.current = []

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data)
      }

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
        const audioFile = new File([audioBlob], 'recording.wav', { type: 'audio/wav' })
        setUploadedFile(audioFile)
        await processAudio(audioFile)
      }

      mediaRecorderRef.current.start()
      setIsRecording(true)
    } catch (error) {
      console.error('Error starting recording:', error)
      alert('Could not access microphone. Please check permissions.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setUploadedFile(file)
      processAudio(file)
    }
  }

  const processAudio = async (file: File) => {
    if (!phoneNumber) {
      alert('Please enter a phone number first')
      return
    }

    setIsProcessing(true)
    setTranscript('')
    setResponse('')
    setAudioUrl('')
    setToolsUsed([])
    setSources([])
    setLatency(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('phone_number', phoneNumber)
    formData.append('language', 'hi-IN')

    try {
      const response = await fetch('http://localhost:8000/voice/chat', {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (response.ok) {
        setTranscript(data.transcript)
        setResponse(data.response)
        setAudioUrl(data.audio_url)
        setCurrentState(data.current_state)
        setToolsUsed(data.tools_used || [])
        setSources(data.sources || [])
        setLatency(data.latency)

        // Auto-play audio if available
        if (data.audio_url && audioRef.current) {
          audioRef.current.src = `http://localhost:8000${data.audio_url}`
          audioRef.current.play()
        }
      } else {
        alert(`Error: ${data.detail || 'Failed to process audio'}`)
      }
    } catch (error) {
      console.error('Error processing audio:', error)
      alert('Failed to connect to server. Please ensure the backend is running.')
    } finally {
      setIsProcessing(false)
    }
  }

  const playAudio = () => {
    if (audioRef.current && audioUrl) {
      audioRef.current.play()
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4 flex items-center">
          <MessageSquare className="w-6 h-6 mr-2" />
          Voice Chat Interface
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

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-xl font-semibold mb-4 flex items-center">
          <Mic className="w-5 h-5 mr-2" />
          Voice Input
        </h3>

        <div className="flex flex-wrap gap-4 mb-4">
          <button
            onClick={isRecording ? stopRecording : startRecording}
            disabled={isProcessing}
            className={`px-6 py-3 rounded-lg flex items-center space-x-2 ${
              isRecording
                ? 'bg-red-500 text-white hover:bg-red-600'
                : 'bg-primary text-white hover:bg-secondary'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            {isRecording ? (
              <>
                <MicOff className="w-5 h-5" />
                <span>Stop Recording</span>
              </>
            ) : (
              <>
                <Mic className="w-5 h-5" />
                <span>Start Recording</span>
              </>
            )}
          </button>

          <label className="px-6 py-3 bg-gray-200 rounded-lg flex items-center space-x-2 cursor-pointer hover:bg-gray-300">
            <Upload className="w-5 h-5" />
            <span>Upload Audio</span>
            <input
              type="file"
              accept="audio/*"
              onChange={handleFileUpload}
              className="hidden"
              disabled={isProcessing}
            />
          </label>

          {uploadedFile && (
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <FileAudio className="w-4 h-4" />
              <span>{uploadedFile.name}</span>
            </div>
          )}
        </div>

        {isRecording && (
          <div className="flex items-center space-x-2 text-red-500">
            <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
            <span>Recording...</span>
          </div>
        )}

        {isProcessing && (
          <div className="flex items-center space-x-2 text-blue-500">
            <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse" />
            <span>Processing audio...</span>
          </div>
        )}
      </div>

      {(transcript || response) && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-4 flex items-center">
              <Phone className="w-5 h-5 mr-2" />
              Transcript
            </h3>
            <div className="bg-gray-50 p-4 rounded-lg">
              <p className="text-gray-800">{transcript || 'No transcript available'}</p>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-4 flex items-center">
              <Volume2 className="w-5 h-5 mr-2" />
              Agent Response
            </h3>
            <div className="bg-blue-50 p-4 rounded-lg mb-4">
              <p className="text-gray-800">{response || 'No response available'}</p>
            </div>

            {audioUrl && (
              <div className="flex items-center space-x-4">
                <audio ref={audioRef} className="w-full" controls />
                <button
                  onClick={playAudio}
                  className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 flex items-center space-x-2"
                >
                  <Play className="w-4 h-4" />
                  <span>Replay</span>
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {currentState && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">Current State</h3>
          <div className="inline-block bg-blue-100 px-4 py-2 rounded-lg">
            <span className="font-semibold">{currentState}</span>
          </div>
        </div>
      )}

      {toolsUsed.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">Tools Used</h3>
          <div className="space-y-2">
            {toolsUsed.map((tool, index) => (
              <div key={index} className="bg-gray-50 p-3 rounded-lg">
                <p><strong>Tool:</strong> {tool.tool}</p>
                <p><strong>Function:</strong> {tool.function}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {sources.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">Retrieved Documents</h3>
          <div className="space-y-2">
            {sources.map((source, index) => (
              <div key={index} className="bg-gray-50 p-3 rounded-lg">
                <p><strong>Source:</strong> {source.metadata?.source || 'Unknown'}</p>
                <p className="text-sm text-gray-600 mt-1">{source.content?.substring(0, 150)}...</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {latency && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4">Latency Metrics</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-50 p-3 rounded-lg">
              <p className="text-sm text-gray-500">STT</p>
              <p className="font-semibold">{latency.stt?.toFixed(2)}s</p>
            </div>
            <div className="bg-gray-50 p-3 rounded-lg">
              <p className="text-sm text-gray-500">TTS</p>
              <p className="font-semibold">{latency.tts?.toFixed(2)}s</p>
            </div>
            <div className="bg-gray-50 p-3 rounded-lg">
              <p className="text-sm text-gray-500">Total</p>
              <p className="font-semibold">{latency.total?.toFixed(2)}s</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default VoiceChat
