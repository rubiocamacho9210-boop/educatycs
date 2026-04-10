import { readFileSync } from "node:fs"
import { resolve } from "node:path"

interface Opportunity {
  id: number
  [key: string]: unknown
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
  const id = Number(getRouterParam(event, "id"))
  const data = loadData()
  const opp = data.find((o) => o.id === id)
  if (!opp) {
    throw createError({ statusCode: 404, message: "Opportunity not found" })
  }
  return opp
})
