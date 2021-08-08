module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  publicPath: "/",
  devServer: {
    proxy: {
      "^/api": {
        target: "http://localhost:5000",
        secure: false,
        pathRewrite: {
          '^/api': '/'
        },
        logLevel: 'debug'
      }
    }
  },
}