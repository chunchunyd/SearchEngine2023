// module.exports = defineConfig({
//   transpileDependencies: true
// })

module.exports = {
  publicPath: '/',
  outputDir: 'dist',
  devServer: {
    open: true,
    host: 'localhost',
    port: '8080',
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/api',
        ws: true,
        secure: true,
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      },
      '/static': {
        target: 'http://127.0.0.1:8000/static',
        ws: true,
        secure: true,
        changeOrigin: true,
        pathRewrite: {
          '^/static': ''
        }
      }
    }
  }
}
