export function useAnalytics() {
  const config = useRuntimeConfig()
  const gaId = config.public.gaId as string

  function loadGA() {
    if (!import.meta.client || !gaId) return
    if (document.getElementById('ga-script')) return

    const script = document.createElement('script')
    script.id = 'ga-script'
    script.src = `https://www.googletagmanager.com/gtag/js?id=${gaId}`
    script.async = true
    document.head.appendChild(script)

    window.dataLayer = window.dataLayer || []
    function gtag(...args: unknown[]) { window.dataLayer.push(args) }
    window.gtag = gtag
    gtag('js', new Date())
    gtag('config', gaId, { anonymize_ip: true })
  }

  function initFromConsent() {
    if (!import.meta.client) return
    const consent = localStorage.getItem('cookieConsent')
    if (consent === 'accepted') loadGA()
  }

  function accept() {
    localStorage.setItem('cookieConsent', 'accepted')
    loadGA()
  }

  function reject() {
    localStorage.setItem('cookieConsent', 'rejected')
  }

  function getConsent(): string | null {
    if (!import.meta.client) return null
    return localStorage.getItem('cookieConsent')
  }

  return { initFromConsent, accept, reject, getConsent }
}
