import { AnimatePresence, motion } from 'framer-motion'
import axios from 'axios'
import { AlertCircle, FileText, Search, Upload } from 'lucide-react'
import TextTab from './TextTab'
import FileTab from './FileTab'

function AnalysisCard({
  activeTab,
  setActiveTab,
  textInput,
  setTextInput,
  selectedFile,
  setSelectedFile,
  isLoading,
  setIsLoading,
  error,
  setError,
  setResults,
}) {
  const handleAnalyze = async () => {
    if (activeTab === 'file' && !selectedFile) {
      setError('Please select a file to analyze')
      return
    }

    if (activeTab === 'text' && !textInput.trim()) {
      setError('Please provide text to analyze')
      return
    }

    setIsLoading(true)
    setError(null)
    setResults(null)

    try {
      const formData = new FormData()
      if (activeTab === 'file' && selectedFile) {
        formData.append('file', selectedFile)
      } else {
        formData.append('text', textInput)
      }

      const response = await axios.post('/analyze', formData)

      if (response.data.status === 'success') {
        setResults(response.data)
      } else {
        setError(response.data.error || 'Analysis failed')
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Could not connect to server')
    } finally {
      setIsLoading(false)
    }
  }

  const tabButtonBase =
    'relative z-10 flex flex-1 items-center justify-center gap-1.5 rounded-lg px-3 py-2 text-[12px] font-medium transition-colors duration-200'

  return (
    <motion.section
      initial={{ y: 30, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5, delay: 0.3 }}
      whileHover={{
        borderColor: 'rgba(255,255,255,0.14)',
        boxShadow:
          '0 0 0 1px rgba(255,255,255,0.07), 0 32px 64px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.10), 0 0 40px rgba(192,210,255,0.04)',
        transition: { duration: 0.3 },
      }}
      className="mx-auto max-w-[700px] rounded-2xl border border-white/10 bg-white/[0.02] p-7"
      style={{
        boxShadow:
          '0 0 0 1px rgba(255,255,255,0.04), 0 32px 64px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06)',
      }}
    >
      <div className="mb-[22px] flex gap-1 rounded-[10px] bg-black/30 p-1">
        <div className="relative flex w-full">
          <button
            type="button"
            onClick={() => setActiveTab('text')}
            className={`${tabButtonBase} ${
              activeTab === 'text' ? 'text-white' : 'text-[#8b9cb8]'
            }`}
          >
            {activeTab === 'text' && (
              <motion.div
                layoutId="activeTab"
                className="absolute inset-0 z-0 rounded-lg bg-blue-500/20"
                style={{
                  border: '1px solid rgba(59,130,246,0.35)',
                  boxShadow: '0 0 18px rgba(59,130,246,0.18)',
                }}
                transition={{ type: 'spring', bounce: 0.2, duration: 0.45 }}
              />
            )}
            <FileText size={13} className="relative z-10" />
            <span className="relative z-10">Text Input</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('file')}
            className={`${tabButtonBase} ${
              activeTab === 'file' ? 'text-white' : 'text-[#8b9cb8]'
            }`}
          >
            {activeTab === 'file' && (
              <motion.div
                layoutId="activeTab"
                className="absolute inset-0 z-0 rounded-lg bg-blue-500/20"
                style={{
                  border: '1px solid rgba(59,130,246,0.35)',
                  boxShadow: '0 0 18px rgba(59,130,246,0.18)',
                }}
                transition={{ type: 'spring', bounce: 0.2, duration: 0.45 }}
              />
            )}
            <Upload size={13} className="relative z-10" />
            <span className="relative z-10">File Upload</span>
          </button>
        </div>
      </div>

      {activeTab === 'text' ? (
        <TextTab textInput={textInput} setTextInput={setTextInput} />
      ) : (
        <FileTab selectedFile={selectedFile} setSelectedFile={setSelectedFile} />
      )}

      <motion.button
        type="button"
        whileTap={{ scale: 0.98 }}
        disabled={isLoading}
        onClick={handleAnalyze}
        className="mt-[18px] flex h-[46px] w-full items-center justify-center gap-2 rounded-[10px] text-[14px] font-semibold text-white transition-all duration-200 disabled:cursor-not-allowed disabled:opacity-80"
        style={{
          background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
          border: 'none',
        }}
        onMouseEnter={(event) => {
          if (!isLoading) {
            event.currentTarget.style.transform = 'translateY(-1px)'
            event.currentTarget.style.boxShadow =
              '0 8px 24px rgba(59,130,246,0.35), 0 0 0 1px rgba(59,130,246,0.4)'
          }
        }}
        onMouseLeave={(event) => {
          event.currentTarget.style.transform = ''
          event.currentTarget.style.boxShadow = ''
        }}
      >
        {isLoading ? (
          <>
            <span className="spin-loader" />
            Analyzing...
          </>
        ) : (
          <>
            <Search size={15} />
            Analyze Document
          </>
        )}
      </motion.button>

      <AnimatePresence mode="wait">
        {error && (
          <motion.div
            key="analysis-error"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="mt-[14px] flex items-center gap-2 rounded-[10px] border border-red-500/20 bg-red-500/10 px-4 py-3 text-[12px] text-red-200/90"
          >
            <AlertCircle size={13} />
            {error}
          </motion.div>
        )}
      </AnimatePresence>

    </motion.section>
  )
}

export default AnalysisCard
