module.exports = {
    css: {
        loaderOptions: {
            less: {
                javascriptEnabled: true
            }
        }
    },
    publicPath: '/',
    devServer: {
        proxy: {
            '/api': {
                target: 'http://tcyhost.xyz:8668'
            },
            '/wapi':{
                target: 'http://aviation.nmc.cn',
                changeOrigin: true,
                pathRewrite: {
                    '/wapi': ''
                  }
          
            }
        }
    },
    /*
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:8080',
                changeOrigin: true,
                pathRewrite: {
                    '^/api': '/mock'
                }
            }
        }
    },
    */
    transpileDependencies: ["vuetify"]
}