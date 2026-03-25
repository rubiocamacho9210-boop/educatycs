/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    './components/**/*.{vue,js,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './app.vue',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        brand: {
          DEFAULT: '#1A73E8',
          dark: '#1558B0',
        },
        border: '#D7DCE3',
        surface: '#EEF2F7',
        ink: {
          DEFAULT: '#1F2937',
          muted: '#6B7280',
        },
      },
    },
  },
}
