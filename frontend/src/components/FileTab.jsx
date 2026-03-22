import { useRef, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { FileCheck, UploadCloud } from 'lucide-react'

function FileTab({ selectedFile, setSelectedFile }) {
  const inputRef = useRef(null)
  const [isDragOver, setIsDragOver] = useState(false)

  const handleFile = (file) => {
    if (!file) {
      return
    }
    setSelectedFile(file)
  }

  return (
    <div>
      <motion.div
        onClick={() => inputRef.current?.click()}
        onDragOver={(event) => {
          event.preventDefault()
          setIsDragOver(true)
        }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={(event) => {
          event.preventDefault()
          setIsDragOver(false)
          handleFile(event.dataTransfer.files?.[0])
        }}
        whileHover={{
          borderColor: 'rgba(192, 210, 255, 0.15)',
          boxShadow:
            '0 0 0 1px rgba(192,210,255,0.08), inset 0 0 24px rgba(192,210,255,0.025), inset 0 0 40px rgba(192,210,255,0.03)',
        }}
        animate={
          isDragOver
            ? {
                borderColor: 'rgba(59,130,246,0.45)',
                backgroundColor: 'rgba(59,130,246,0.04)',
                boxShadow:
                  '0 0 0 1px rgba(192,210,255,0.06), inset 0 0 30px rgba(59,130,246,0.03), inset 0 0 40px rgba(192,210,255,0.03)',
              }
            : {
                borderColor: 'rgba(255,255,255,0.12)',
                backgroundColor: 'transparent',
              }
        }
        transition={{ duration: 0.25 }}
        className="cursor-pointer rounded-[10px] border border-dashed px-8 py-12 text-center"
      >
        <UploadCloud size={32} color="rgba(255,255,255,0.25)" className="mx-auto" />
        <p className="mb-1 mt-3 text-[14px] font-medium text-white/65">Drop your document here</p>
        <p className="text-[12px] text-[#4a5568]">or click to browse — PDF or text files</p>
      </motion.div>

      <input
        ref={inputRef}
        type="file"
        className="hidden"
        accept=".pdf,.txt,.md,.doc,.docx"
        onChange={(event) => handleFile(event.target.files?.[0])}
      />

      <AnimatePresence>
        {selectedFile && (
          <motion.div
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -6 }}
            className="mt-[10px] flex items-center justify-center gap-1.5 text-[12px]"
            style={{ color: 'rgba(147,197,253,0.9)' }}
          >
            <FileCheck size={13} />
            <span>{selectedFile.name}</span>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default FileTab
