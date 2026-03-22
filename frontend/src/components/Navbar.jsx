import { motion } from 'framer-motion'
import { AlignLeft, FileText, Upload } from 'lucide-react'

function Navbar({ activeTab, setActiveTab }) {
  return (
    <motion.nav
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="fixed inset-x-0 top-0 z-50 h-14 border-b border-white/[0.06]"
      style={{
        background: 'rgba(5,8,22,0.85)',
        backdropFilter: 'blur(20px)',
      }}
    >
      <div className="mx-auto flex h-full w-full max-w-[1040px] items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <FileText size={16} color="white" opacity={0.85} />
          <span
            className="text-[14px] font-semibold text-white"
            style={{ letterSpacing: '-0.01em' }}
          >
            Legislative AI
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setActiveTab('text')}
            className={`silver-button flex items-center gap-1.5 rounded-lg px-4 py-1.5 text-xs font-medium ${
              activeTab === 'text' ? 'active' : ''
            }`}
          >
            <AlignLeft size={13} />
            Text Analysis
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('file')}
            className={`silver-button flex items-center gap-1.5 rounded-lg px-4 py-1.5 text-xs font-medium ${
              activeTab === 'file' ? 'active' : ''
            }`}
          >
            <Upload size={13} />
            File Upload
          </button>
        </div>
      </div>
    </motion.nav>
  )
}

export default Navbar
