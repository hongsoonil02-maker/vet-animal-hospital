import { defineConfig } from "vite";
import { resolve } from "path";

export default defineConfig({
  server: { port: 5173, host: true },
  preview: { port: 4173 },
  publicDir: "public",
  build: {
    outDir: "dist",
    assetsDir: "assets",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html"),
        hospital: resolve(__dirname, "hospital.html"),
        privacy: resolve(__dirname, "privacy.html"),
        terms: resolve(__dirname, "terms.html"),
      },
    },
  },
});
