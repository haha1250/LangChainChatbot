export default {
  plugins: [
    require('@tailwindcss/postcss')({
      config: './tailwind.config.js', // optional path
    }),
    require('autoprefixer'),
  ],
};