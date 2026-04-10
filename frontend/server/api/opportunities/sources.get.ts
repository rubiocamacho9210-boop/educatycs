import { readFileSync } from "node:fs"
import { resolve } from "node:path"

const SOURCE_NAMES: Record<string, string> = {
  capacitate: "Capacítate para el Empleo",
  google: "Google Actívate",
  aprende_mx: "Aprende.mx",
  edx: "edX en Español",
  coursera: "Coursera",
  khan: "Khan Academy",
  santander: "Santander Open Academy",
  unam: "UNAM",
  idiomas: "Idiomas",
  becas: "Becas",
}

interface Opportunity {
  source: string
}

let cached: Opportunity[] | null = null

function loadData(): Opportunity[] {
  if (!cached) {
    const path = resolve("public/data/opportunities.json")
    cached = JSON.parse(readFileSync(path, "utf-8")) as Opportunity[]
  }
  return cached
}

export default defineEventHandler(() => {
  const data = loadData()
  const counts: Record<string, number> = {}
  for (const o of data) {
    counts[o.source] = (counts[o.source] ?? 0) + 1
  }

  const sources: Record<string, { name: string; count: number }> = {}
  for (const [key, count] of Object.entries(counts)) {
    sources[key] = { name: SOURCE_NAMES[key] ?? key, count }
  }

  return {
    sources,
    total_opportunities: data.length,
    tip: "Data served from static JSON",
  }
})
