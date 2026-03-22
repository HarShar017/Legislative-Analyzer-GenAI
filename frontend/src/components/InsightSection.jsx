import { motion } from 'framer-motion'
import { AlertTriangle, Clock, TrendingUp, Users, Zap } from 'lucide-react'

const sectionDefinitions = [
  { key: 'Key Changes', icon: Zap },
  { key: 'Who Is Affected', icon: Users },
  { key: 'Financial Impact', icon: TrendingUp },
  { key: 'Timeline', icon: Clock },
  { key: 'Risks and Concerns', icon: AlertTriangle },
]

function parseSummary(summary) {
  const sections = {}

  sectionDefinitions.forEach(({ key }) => {
    const escapedKey = key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    const nextKeys = sectionDefinitions
      .filter((item) => item.key !== key)
      .map((item) => item.key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))
      .join('|')

    const regex = new RegExp(
      `${escapedKey}:?([\\s\\S]*?)(?=\\n(?:${nextKeys}):?|$)`,
      'i',
    )
    const match = summary.match(regex)

    if (match?.[1]) {
      const bullets = match[1]
        .split('\n')
        .map((line) => line.replace(/^[-*\u2022\s]+/, '').trim())
        .filter(Boolean)

      if (bullets.length > 0) {
        sections[key] = bullets
      }
    }
  })

  return sections
}

function InsightSection({ summary }) {
  if (!summary || typeof summary !== 'string') {
    return null
  }

  const parsed = parseSummary(summary)
  const hasParsedSections = sectionDefinitions.some(
    ({ key }) => parsed[key] && parsed[key].length > 0,
  )

  if (!hasParsedSections) {
    return <div>{summary}</div>
  }

  return (
    <div>
      {sectionDefinitions.map(({ key, icon: Icon }) => {
        const items = parsed[key]

        if (!items || items.length === 0) {
          return null
        }

        return (
          <div key={key}>
            <div
              className="mb-[6px] mt-4 flex items-center gap-1.5 text-[11px] font-semibold uppercase"
              style={{ color: 'rgba(147,197,253,0.9)', letterSpacing: '0.08em' }}
            >
              <Icon size={11} />
              <span>{key}</span>
            </div>

            {items.map((item, index) => (
              <motion.div
                key={`${key}-${item}-${index}`}
                initial={{ x: -8, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ duration: 0.24, delay: index * 0.03 }}
                className="py-[3px] text-[13px]"
                style={{ color: '#e2e8f0' }}
              >
                • {item}
              </motion.div>
            ))}
          </div>
        )
      })}
    </div>
  )
}

export default InsightSection
