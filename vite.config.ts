import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import { resolve } from "path";
import { renameSync } from "fs";

export default defineConfig({
  plugins: [
    tailwindcss(),
    {
      name: "rename-html",
      closeBundle() {
        try {
          renameSync(
            resolve(__dirname, "dist/index.vite.html"),
            resolve(__dirname, "dist/index.html"),
          );
        } catch {}
      },
    },
  ],
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
