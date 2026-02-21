import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../server/static',
    emptyOutDir: false,
    rollupOptions: {
      output: {
        entryFileNames: 'js/script_react_compiled.js',
        assetFileNames: (assetInfo) => {
          if (assetInfo.name && assetInfo.name.endsWith('.css')) {
            return 'css/style_react_compiled.css';
          }
          return 'assets/[name][extname]';
        },
      },
    },
  },
})
