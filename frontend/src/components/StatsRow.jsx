import { motion } from 'framer-motion'

function StatsRow({ results }) {
  if (!results) {
    return null
  }

  const originalTokens = results?.chunk_stats?.original_total_tokens ?? 0
  const compressedTokens = results?.chunk_stats?.compressed_total_tokens ?? 0
  const compressionRate =
    originalTokens > 0
      ? `${((1 - compressedTokens / originalTokens) * 100).toFixed(1)}%`
      : '0.0%'

  const stats = [
    { label: 'Chunks Processed', value: results?.num_chunks ?? 0 },
    { label: 'Original Tokens', value: originalTokens },
    { label: 'Compressed Tokens', value: compressedTokens },
    { label: 'Compression Rate', value: compressionRate },
  ]

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={{
        hidden: {},
        visible: {
          transition: {
            staggerChildren: 0.08,
          },
        },
      }}
      className="mx-auto mt-6 grid max-w-[700px] grid-cols-2 gap-[10px] md:grid-cols-4"
    >
      {stats.map((item) => (
        <motion.div
          key={item.label}
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          whileHover={{
            background: 'rgba(255,255,255,0.04)',
            borderColor: 'rgba(192, 210, 255, 0.15)',
            boxShadow:
              '0 0 0 1px rgba(192,210,255,0.08), inset 0 0 20px rgba(192,210,255,0.03)',
            transition: { duration: 0.25 },
          }}
          className="rounded-xl border border-white/10 bg-white/[0.02] px-[18px] py-[14px]"
        >
          <div className="mb-[5px] text-[10px] font-medium uppercase text-[#4a5568]" style={{ letterSpacing: '0.08em' }}>
            {item.label}
          </div>
          <div className="text-[22px] font-bold text-white" style={{ letterSpacing: '-0.02em' }}>
            {item.value}
          </div>
        </motion.div>
      ))}
    </motion.div>
  )
}

export default StatsRow
