import { describe, it, expect } from 'vitest'
import {
  getAvailableTags,
  buildApiQuery,
  buildUrlQuery,
  hasActiveFilters,
  toggleTag,
} from '../utils/filters'
import type { Opportunity } from '../types/opportunity'

// ─── Fixture ────────────────────────────────────────────────────────────────

const makeOpportunity = (tags: string[]): Opportunity => ({
  id: 1,
  title: 'Test',
  description: null,
  opportunity_type: 'course',
  provider: 'Test',
  source: 'test',
  source_url: 'https://example.com',
  location: null,
  start_date: null,
  end_date: null,
  is_free: true,
  tags,
})

// ─── getAvailableTags ────────────────────────────────────────────────────────

describe('getAvailableTags', () => {
  it('devuelve lista vacía si no hay oportunidades', () => {
    expect(getAvailableTags([])).toEqual([])
  })

  it('devuelve los tags únicos de todas las oportunidades', () => {
    const opportunities = [
      makeOpportunity(['python', 'programación']),
      makeOpportunity(['python', 'datos']),
    ]
    expect(getAvailableTags(opportunities)).toEqual(['datos', 'programación', 'python'])
  })

  it('devuelve los tags ordenados alfabéticamente', () => {
    const opportunities = [makeOpportunity(['zebra', 'apple', 'mango'])]
    expect(getAvailableTags(opportunities)).toEqual(['apple', 'mango', 'zebra'])
  })

  it('elimina duplicados aunque vengan de distintas oportunidades', () => {
    const opportunities = [
      makeOpportunity(['stem']),
      makeOpportunity(['stem']),
      makeOpportunity(['stem']),
    ]
    expect(getAvailableTags(opportunities)).toEqual(['stem'])
  })

  it('devuelve lista vacía si todas las oportunidades tienen tags vacíos', () => {
    const opportunities = [makeOpportunity([]), makeOpportunity([])]
    expect(getAvailableTags(opportunities)).toEqual([])
  })
})

// ─── buildApiQuery ───────────────────────────────────────────────────────────

describe('buildApiQuery', () => {
  it('incluye limit y offset siempre', () => {
    const q = buildApiQuery('', '', '', '', 1, 12)
    expect(q.limit).toBe(12)
    expect(q.offset).toBe(0)
  })

  it('calcula el offset correctamente según la página', () => {
    expect(buildApiQuery('', '', '', '', 1, 12).offset).toBe(0)
    expect(buildApiQuery('', '', '', '', 2, 12).offset).toBe(12)
    expect(buildApiQuery('', '', '', '', 3, 12).offset).toBe(24)
  })

  it('omite los filtros vacíos (undefined) en lugar de enviar string vacío', () => {
    const q = buildApiQuery('', '', '', '', 1, 12)
    expect(q.search).toBeUndefined()
    expect(q.opportunity_type).toBeUndefined()
    expect(q.source).toBeUndefined()
    expect(q.tag).toBeUndefined()
  })

  it('incluye los filtros cuando tienen valor', () => {
    const q = buildApiQuery('python', 'course', 'coursera', 'stem', 1, 12)
    expect(q.search).toBe('python')
    expect(q.opportunity_type).toBe('course')
    expect(q.source).toBe('coursera')
    expect(q.tag).toBe('stem')
  })
})

// ─── buildUrlQuery ───────────────────────────────────────────────────────────

describe('buildUrlQuery', () => {
  it('devuelve objeto vacío si no hay filtros activos en página 1', () => {
    expect(buildUrlQuery('', '', '', '', 1)).toEqual({})
  })

  it('no incluye page si es 1', () => {
    const q = buildUrlQuery('python', '', '', '', 1)
    expect(q).not.toHaveProperty('page')
  })

  it('incluye page solo si es mayor a 1', () => {
    const q = buildUrlQuery('', '', '', '', 3)
    expect(q.page).toBe(3)
  })

  it('incluye solo los filtros con valor', () => {
    const q = buildUrlQuery('becas', 'scholarship', '', '', 1)
    expect(q.search).toBe('becas')
    expect(q.opportunity_type).toBe('scholarship')
    expect(q).not.toHaveProperty('source')
    expect(q).not.toHaveProperty('tag')
  })
})

// ─── hasActiveFilters ────────────────────────────────────────────────────────

describe('hasActiveFilters', () => {
  it('devuelve false cuando todos los filtros están vacíos', () => {
    expect(hasActiveFilters('', '', '')).toBe(false)
  })

  it('devuelve true si hay búsqueda activa', () => {
    expect(hasActiveFilters('python', '', '')).toBe(true)
  })

  it('devuelve true si hay tipo activo', () => {
    expect(hasActiveFilters('', 'course', '')).toBe(true)
  })

  it('devuelve true si hay fuente activa', () => {
    expect(hasActiveFilters('', '', 'coursera')).toBe(true)
  })

  it('devuelve true si hay múltiples filtros activos', () => {
    expect(hasActiveFilters('python', 'course', 'coursera')).toBe(true)
  })

  it('devuelve true si solo hay un tag activo', () => {
    expect(hasActiveFilters('', '', '', 'stem')).toBe(true)
  })

  it('devuelve false cuando todos los filtros incluido tag están vacíos', () => {
    expect(hasActiveFilters('', '', '', '')).toBe(false)
  })
})

// ─── toggleTag ───────────────────────────────────────────────────────────────

describe('toggleTag', () => {
  it('selecciona un tag cuando no hay ninguno activo', () => {
    expect(toggleTag('', 'stem')).toBe('stem')
  })

  it('deselecciona el tag si se hace click en el activo', () => {
    expect(toggleTag('stem', 'stem')).toBe('')
  })

  it('cambia al nuevo tag si se hace click en uno distinto', () => {
    expect(toggleTag('stem', 'python')).toBe('python')
  })

  it('es consistente: dos clicks en el mismo tag vuelven al estado inicial', () => {
    const afterFirst = toggleTag('', 'stem')
    const afterSecond = toggleTag(afterFirst, 'stem')
    expect(afterSecond).toBe('')
  })
})
