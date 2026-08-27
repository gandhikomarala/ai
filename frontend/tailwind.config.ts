import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "#090d16",
        surface: "#111827",
        surfaceBorder: "#1f293d",
        primary: "#3b82f6",
        primaryHover: "#2563eb",
        accent: "#10b981",
        danger: "#ef4444",
        warning: "#f59e0b"
      }
    },
  },
  plugins: [],
};
export default config;
