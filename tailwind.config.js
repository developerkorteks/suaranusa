/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./portal/views/**/*.py",
    "./static/js/**/*.js",
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ['"Playfair Display"', 'serif'],
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        'nusa-red': '#ff3b30',
        'nusa-bg': '#f7f7f5',
        'nusa-dark': '#0a0a0a',
      },
      letterSpacing: {
        'luxury': '0.12em',
        'editorial': '0.4em',
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
