import { motion } from 'framer-motion'

const containerVariants = {
  hidden: {},
  show: {
    transition: {
      staggerChildren: 0.12,
    },
  },
}

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  show: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.5,
      ease: 'easeOut',
    },
  },
}

function Hero() {
  return (
    <motion.section
      variants={containerVariants}
      initial="hidden"
      animate="show"
      className="pb-14 pt-[120px] text-center"
    >
      <motion.h1
        variants={itemVariants}
        className="mx-auto mb-[18px] max-w-[980px] px-2 font-extrabold"
        style={{
          fontSize: 'clamp(52px, 7vw, 88px)',
          lineHeight: 1,
          letterSpacing: '-0.04em',
          background:
            'linear-gradient(135deg, #ffffff 0%, #c0d2ff 40%, #8ba8e8 70%, #ffffff 100%)',
          WebkitBackgroundClip: 'text',
          backgroundClip: 'text',
          color: 'transparent',
          filter: 'drop-shadow(0 0 40px rgba(147,197,253,0.3))',
        }}
      >
        AI Legislative Analyzer
      </motion.h1>

      <motion.p
        variants={itemVariants}
        className="mx-auto mb-12 max-w-[400px] px-4 text-[15px] leading-[1.6]"
        style={{ color: '#8b9cb8' }}
      >
        Extract structured insights from legal and policy documents using intelligent
        compression and AI analysis
      </motion.p>
    </motion.section>
  )
}

export default Hero
