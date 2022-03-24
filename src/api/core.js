import Cookies from 'js-cookie'
const axios = require('axios')

const api_urls = {
    getCity: '/api/core/city',
    queryAirlines: '/api/core/airline',
    getUsers: "/api/core/user",
    addManager: "/api/permission",
    queryFlight: "/api/core/flight",
    queryAirport: "/api/core/airport",
    queryCompany: "/api/core/company",
    getMyInfo: "/api/core/check",
    getFlightWorker: "/api/core/relation",
    tripRecord: "/api/core/trip_record",
    getAirportOntime: "/api/core/airport_ontime",
    getAirportCpn: "/api/core/airport_cpn",
    getAirportFlow: "/api/core/airport_flow"
}

axios.defaults.headers.common['Authorization'] = Cookies.get('access-token') == null ? '' : 'Bearer ' + Cookies.get('access-token');

export function setToken(){
    axios.defaults.headers.common['Authorization'] = Cookies.get('access-token') == null ? '' : 'Bearer ' + Cookies.get('access-token');
}

export function addCity(data) {
    return axios({
        url: api_urls.getCity,
        data: data,
        method: 'post'
    })
}

export function getCities() {
    return axios({
        url: api_urls.getCity,
        method: 'get'
    })
}

export function getAllAirlines() {
    return axios({
        url: api_urls.queryAirlines,
        method: 'get'
    })
}

export function queryAirlines(params) {
    return axios({
        url: api_urls.queryAirlines,
        params: params,
        method: 'get'
    })
}

export function getUsers() {
    return axios({
        url: api_urls.getUsers,
        method: 'get'
    })
}

export function deleteUser(account) {
    return axios({
        url: api_urls.getUsers + '/'+ account,
        method: 'delete'
    })
}

export function modifyUser(account, data) {
    return axios({
        url: api_urls.getUsers + '/'+ account,
        data: data,
        method: 'patch'
    })
}

export function addManager(data) {
    return axios({
        url: api_urls.addManager,
        data: data,
        method: 'post'
    })
}

export function queryFlight(params) {
    return axios({
        url: api_urls.queryFlight,
        params: params,
        method: 'get'
    })
}

export function deleteFlight(id) {
    return axios({
        url: api_urls.queryFlight + '/'+ id,
        method: 'delete'
    })
}

export function modifyFlight(id, data) {
    return axios({
        url: api_urls.queryFlight + '/'+ id,
        data: data,
        method: 'patch'
    })
}

export function getFlightDetail(id) {
    return axios({
        url: api_urls.queryFlight + '/'+ id,
        method: 'get'
    })
}

export function addFlight(data) {
    return axios({
        url: api_urls.queryFlight,
        data:data,
        method: 'post'
    })
}


export function queryAirport(params) {
    return axios({
        url: api_urls.queryAirport,
        params: params,
        method: 'get'
    })
}

export function getAirportDetail(id) {
    return axios({
        url: api_urls.queryAirport + '/'+ id,
        method: 'get'
    })
}


export function queryCompany() {
    return axios({
        url: api_urls.queryCompany,
        method: 'get'
    })
}

export function getMyInfo() {
    return axios({
        url: api_urls.getMyInfo,
        method: 'get'
    })
}

export function getFlightWorker(params) {
    return axios({
        url: api_urls.getFlightWorker,
        params: params,
        method: 'get'
    })
}

export function buyTicket(data) {
    return axios({
        url: api_urls.tripRecord,
        data: data,
        method: 'post'
    })
}

export function queryTicket(params) {
    return axios({
        url: api_urls.tripRecord,
        params: params,
        method: 'get'
    })
}

export function delTicket(data) {
    return axios({
        url: api_urls.tripRecord,
        data: data,
        method: 'delete'
    })
}

export function getAirportOntime(data) {
    return axios({
        url: api_urls.getAirportOntime,
        data: data,
        method: 'post'
    })
}

export function getAirportCpn(data) {
    return axios({
        url: api_urls.getAirportCpn,
        data: data,
        method: 'post'
    })
}

export function getAirportFlow(data) {
    return axios({
        url: api_urls.getAirportFlow,
        data: data,
        method: 'post'
    })
}