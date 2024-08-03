import daisyui from "daisyui"

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,ts,jsx,tsx}"],
  daisyui: {
    themes: ["night"],
  },
  plugins: [daisyui],
};
