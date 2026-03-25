import type { Opportunity } from '../types/opportunity'

/**
 * Extrae los tags únicos y ordenados de una lista de oportunidades.
 */
export function getAvailableTags(opportunities: Opportunity[]): string[] {
  const all = opportunities.flatMap(o => o.tags)
  return [...new Set(all)].sort()
}

/**
 * Construye el objeto de query params para la API.
 */
export function buildApiQuery(
  search: string,
  type: string,
  source: string,
  tag: string,
  page: number,
  limit: number,
): Record<string, string | number | undefined> {
  return {
    search: search || undefined,
    opportunity_type: type || undefined,
    source: source || undefined,
    tag: tag || undefined,
    limit,
    offset: (page - 1) * limit,
  }
}

/**
 * Construye el objeto de query params para la URL del navegador.
 */
export function buildUrlQuery(
  search: string,
  type: string,
  source: string,
  tag: string,
  page: number,
): Record<string, string | number> {
  return {
    ...(search ? { search } : {}),
    ...(type ? { opportunity_type: type } : {}),
    ...(source ? { source } : {}),
    ...(tag ? { tag } : {}),
    ...(page > 1 ? { page } : {}),
  }
}

/**
 * Indica si hay algún filtro activo.
 */
export function hasActiveFilters(search: string, type: string, source: string, tag = ''): boolean {
  return search !== '' || type !== '' || source !== '' || tag !== ''
}

/**
 * Alterna un tag: si ya está seleccionado lo deselecciona, si no lo selecciona.
 */
export function toggleTag(current: string, clicked: string): string {
  return current === clicked ? '' : clicked
}
