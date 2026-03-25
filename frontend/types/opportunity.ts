export type OpportunityType = "course" | "workshop" | "scholarship" | "event" | "other"

export interface SourceInfo {
  value: string  // clave usada como query param (e.g. "capacitate")
  label: string  // nombre legible (e.g. "Capacítate para el Empleo")
  count: number
}

interface SourcesApiResponse {
  sources: Record<string, { name: string; count: number }>
  total_opportunities: number
  tip: string
}

export interface Opportunity {
  id: number
  title: string
  description: string | null
  opportunity_type: OpportunityType
  provider: string
  source: string
  source_url: string
  location: string | null
  start_date: string | null
  end_date: string | null
  is_free: boolean | null
  tags: string[]
}
