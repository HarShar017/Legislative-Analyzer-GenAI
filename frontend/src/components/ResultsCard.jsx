import { motion } from 'framer-motion'
import { BarChart2, CheckCircle, X } from 'lucide-react'
import InsightSection from './InsightSection'

function ResultsCard({
  results,
  setResults,
  setError,
  setTextInput,
  setSelectedFile,
  onClear,
}) {
  if (!results) {
    return null
  }

  const outputText =
    typeof results.summary === 'string'
      ? results.summary
      : JSON.stringify(results, null, 2)

  return (
    <motion.section
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{
        borderColor: 'rgba(255,255,255,0.14)',
        boxShadow:
          '0 0 0 1px rgba(255,255,255,0.07), inset 0 0 30px rgba(192,210,255,0.03)',
        transition: { duration: 0.25 },
      }}
      className="mx-auto mt-[14px] max-w-[700px] rounded-2xl border border-white/10 bg-white/[0.02] p-7"
      style={{
        boxShadow:
          '0 0 0 1px rgba(255,255,255,0.04), 0 32px 64px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06)',
      }}
    >
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-2 text-[13px] font-semibold text-white">
          <BarChart2 size={14} />
          Analysis Results
        </div>

        <button
          type="button"
          className="silver-button flex items-center gap-1.5 rounded-lg px-4 py-1.5 text-xs font-medium"
          onClick={() => {
            setResults(null)
            setError(null)
            setTextInput('')
            setSelectedFile(null)
            onClear?.()
          }}
        >
          <X size={12} />
          Clear
        </button>
      </div>

      <div className="mb-[14px] flex items-center gap-2 rounded-[10px] border border-green-400/20 bg-green-500/10 px-4 py-[10px] text-[12px] text-green-200/90">
        <CheckCircle size={13} />
        Analysis completed successfully
      </div>

      <div
        className="result-scrollbar rounded-[10px] border border-white/[0.05] bg-black/20 p-[18px] text-[12px] leading-[1.9] text-slate-300 transition-all duration-200 hover:border-white/10"
        style={{
          whiteSpace: 'pre-wrap',
          fontFamily: 'Inter, sans-serif',
          maxHeight: '480px',
          overflowY: 'auto',
          boxShadow: 'inset 0 0 20px rgba(192,210,255,0.02)',
        }}
      >
        <InsightSection summary={results.summary} />
        {!results.summary && outputText}
      </div>
    </motion.section>
  )
}

export default ResultsCard
