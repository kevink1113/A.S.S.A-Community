const colors = require('tailwindcss/colors')

module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        teal: colors.teal,
        mint: {
          light: "#1ac4eb",
          DEFAULT: "#17a8c9",
          dark: "#128aa6",
        },
      },
      maxWidth:{
        "30px": "30px",
        "50px": "50px",
        "70px": "70px",
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
