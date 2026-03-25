export function useColorMode() {
  const isDark = useState<boolean>('colorMode', () => true)

  function apply(dark: boolean) {
    isDark.value = dark
    if (import.meta.client) {
      document.documentElement.classList.toggle('dark', dark)
      localStorage.setItem('colorMode', dark ? 'dark' : 'light')
    }
  }

  function toggle() {
    apply(!isDark.value)
  }

  function init() {
    if (import.meta.client) {
      const stored = localStorage.getItem('colorMode')
      if (stored) {
        apply(stored === 'dark')
      }
      else {
        apply(window.matchMedia('(prefers-color-scheme: dark)').matches)
      }
    }
  }

  return { isDark, toggle, init }
}
