const axios = require('axios')

const api_urls = {
    loginurl: '/api/login',
    register: '/api/register'
}

export function login(data) {
    return axios({
        url: api_urls.loginurl,
        data: data,
        method: 'post'
    })
}

export function register(data) {
    return axios({
        url: api_urls.register,
        data: data,
        method: 'post'
    })
}
