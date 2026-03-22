import { useState } from 'react'
import { motion } from 'framer-motion'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import AnalysisCard from './components/AnalysisCard'
import StatsRow from './components/StatsRow'
import ResultsCard from './components/ResultsCard'

function App() {
  const [activeTab, setActiveTab] = useState('text')
  const [textInput, setTextInput] = useState('')
  const [selectedFile, setSelectedFile] = useState(null)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleClear = () => {
    setResults(null)
    setError(null)
    setTextInput('')
    setSelectedFile(null)
  }

  return (
    <div
      style={{
        background: '#050816',
        position: 'relative',
        overflowX: 'hidden',
        minHeight: '100vh',
      }}
    >
      <div
        style={{
          position: 'absolute',
          inset: 0,
          zIndex: 0,
          backgroundImage:
            'linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px)',
          backgroundSize: '60px 60px',
          pointerEvents: 'none',
        }}
      />
      <div
        style={{
          position: 'absolute',
          top: '-120px',
          left: '50%',
          transform: 'translateX(-50%)',
          width: '900px',
          height: '500px',
          background:
            'radial-gradient(ellipse at center, rgba(59,130,246,0.13) 0%, transparent 70%)',
          pointerEvents: 'none',
          zIndex: 0,
        }}
      />

      <div className="relative z-10 px-4 pb-12">
        <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
        <Hero />

        <AnalysisCard
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          textInput={textInput}
          setTextInput={setTextInput}
          selectedFile={selectedFile}
          setSelectedFile={setSelectedFile}
          isLoading={isLoading}
          setIsLoading={setIsLoading}
          error={error}
          setError={setError}
          setResults={setResults}
        />

        {!results && (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.45, delay: 0.45 }}
            className="mx-auto mt-5 flex max-w-[700px] flex-wrap items-center justify-center gap-[10px]"
          >
            {['Legal Documents', 'Policy Text', 'Legislative Bills'].map((item) => (
              <span
                key={item}
                className="rounded-full border border-white/10 bg-white/[0.03] px-[14px] py-[5px] text-[11px] font-medium text-[#4a5568]"
              >
                {item}
              </span>
            ))}
          </motion.div>
        )}

        {results && <StatsRow results={results} />}

        {results && (
          <ResultsCard
            results={results}
            setResults={setResults}
            setError={setError}
            setTextInput={setTextInput}
            setSelectedFile={setSelectedFile}
            onClear={handleClear}
          />
        )}
      </div>
    </div>
  )
}

export default App
