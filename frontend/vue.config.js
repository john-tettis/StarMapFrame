module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  devServer: {
    hot: true,
    disableHostCheck: true,
    port: 8080,
    public: '0.0.0.0:8080',
    proxy: {
      "^/api": {
        target: "http://localhost:8000",
        secure: false,
        pathRewrite: {
          '^/api': '/'
        },
        logLevel: 'debug'
      }
    }
  },
}