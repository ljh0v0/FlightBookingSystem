const axios = require('axios')

const api_urls = {
    getStationCode: '/wapi/f/airportinfo/autocomplete',
    getWeather: '/wapi/f/restapi/weather',
}

export function getStationCode(params) {
    return axios({
        url: api_urls.getStationCode,
        params: params,
        method: 'get'
    })
}

export function getWeather(stationCode) {
    return axios({
        url: api_urls.getWeather + '/' + stationCode,
        method: 'get'
    })
}

