export function buildApiUrl(base: string, path: string): string {
  const normalizedBase = base.endsWith("/") ? base : `${base}/`
  const normalizedPath = path.startsWith("/") ? path.slice(1) : path
  return new URL(normalizedPath, normalizedBase).toString()
}
