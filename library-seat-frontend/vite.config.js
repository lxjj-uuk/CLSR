import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 后端 Spring Boot（context-path 为空），默认 8080
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5175,
    open: false,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
      }
    }
  }
})
