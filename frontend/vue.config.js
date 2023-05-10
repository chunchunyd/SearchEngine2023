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
      '/': {
        target: 'http://127.0.0.1:8000',
        ws: true,
        secure: true,
        changeOrigin: true,
        pathRewrite: {
        }
      }
    }
  }
}
