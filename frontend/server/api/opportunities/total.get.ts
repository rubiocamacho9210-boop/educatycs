import { readFileSync } from "node:fs"
import { resolve } from "node:path"

interface Opportunity {
  id: number
  title: string
  description: string | null
  opportunity_type: string
  source: string
  tags: string[]
}

let cached: Opportunity[] | null = null

function loadData(): Opportunity[] {
  if (!cached) {
    const path = resolve("public/data/opportunities.json")
    cached = JSON.parse(readFileSync(path, "utf-8")) as Opportunity[]
  }
  return cached
}

export default defineEventHandler((event) => {
  const query = getQuery(event)
  const search = (query.search as string) ?? ""
  const opportunity_type = (query.opportunity_type as string) ?? ""
  const source = (query.source as string) ?? ""
  const tag = (query.tag as string) ?? ""

  let data = loadData()

  if (opportunity_type) data = data.filter((o) => o.opportunity_type === opportunity_type)
  if (source) data = data.filter((o) => o.source === source)
  if (tag) data = data.filter((o) => o.tags.includes(tag))
  if (search) {
    const q = search.toLowerCase()
    data = data.filter(
      (o) =>
        o.title.toLowerCase().includes(q) ||
        (o.description ?? "").toLowerCase().includes(q),
    )
  }

  return { total: data.length }
})
