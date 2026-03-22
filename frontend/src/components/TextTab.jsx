import { motion } from 'framer-motion'

function TextTab({ textInput, setTextInput }) {
  return (
    <motion.textarea
      value={textInput}
      onChange={(event) => setTextInput(event.target.value)}
      placeholder="Paste legal or policy text here for analysis..."
      whileHover={{
        borderColor: 'rgba(192, 210, 255, 0.15)',
        boxShadow:
          '0 0 0 1px rgba(192,210,255,0.08), inset 0 0 24px rgba(192,210,255,0.025)',
        background: 'rgba(0,0,0,0.3)',
      }}
      className="w-full resize-y rounded-[10px] border border-white/10 bg-black/25 p-[14px] text-[13px] leading-[1.6] text-slate-200 outline-none transition-all duration-200 placeholder:text-[#4a5568] focus:border-blue-500/40"
      style={{
        minHeight: '200px',
        fontFamily: 'Inter, sans-serif',
      }}
      onFocus={(event) => {
        event.currentTarget.style.boxShadow = '0 0 0 3px rgba(59,130,246,0.08)'
      }}
      onBlur={(event) => {
        event.currentTarget.style.boxShadow = ''
      }}
    />
  )
}

export default TextTab
