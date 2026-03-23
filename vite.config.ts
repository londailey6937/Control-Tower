import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import { resolve } from "path";

export default defineConfig({
  plugins: [tailwindcss()],
  resolve: {
    alias: {
      "@": "/src",
    },
  },
  build: {
    rollupOptions: {
      input: resolve(__dirname, "index.vite.html"),
    },
  },
  server: {
    open: "/index.vite.html",
  },
});
