import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default {
  server: {
    host: '0.0.0.0', // or your desired host
    port: 3000, // or your desired host
    watch: {
      usePolling: true, // use polling for file watching
      interval: 1000, // polling interval in milliseconds
    },
  },
  plugins: [react()],    
};