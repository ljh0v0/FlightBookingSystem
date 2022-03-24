import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '@/views/home'
import Flight from '@/views/flight'
import User from '@/views/user'
    import UserInfo from '@/views/User/user-info'
    import TripRecord from '@/views/User/trip-record'
import Airport from '@/views/airport.vue'
import Login from '@/views/Login/login.vue'
import Register from '@/views/Login/register'
import Manager from '@/views/manager'
    import UsersTable from '@/views/Manager/users-table'
    import FlightsTable from '@/views/Manager/flights-table'

Vue.use(VueRouter)

const DEFAULT_TITLE = "Wechat"

const router = new VueRouter({
    routes: [
        {
            path: '/',
            name: 'home',
            meta: {
                title: '首页'
            },
            component: Home
        },
        {
            path: '/flight',
            name: 'flight',
            meta: {
                title: '航班信息'
            },
            component: Flight
        },
        {
            path: '/airport',
            name: 'airport',
            meta: {
                title: '机场信息'
            },
            component: Airport
        },
        {
            path: '/user',
            name: 'user',
            meta: {
                title: '用户中心'
            },
            component: User,
            children: [
                {
                    path: 'user_info',
                    name: 'user_info',
                    meta: {
                        title: '用户信息'
                    },
                    component: UserInfo
                },
                {
                    path: 'trip_record',
                    name: 'trip_record',
                    meta: {
                        title: '行程记录'
                    },
                    component: TripRecord
                },
            ]
        },
        {
            path: '/manager',
            name: 'manager',
            meta: {
                title: '管理端'
            },
            component: Manager,
            children: [
                {
                    path: 'users_table',
                    name: 'users_table',
                    meta: {
                        title: '用户列表'
                    },
                    component: UsersTable
                },
                {
                    path: 'flights_table',
                    name: 'flights_table',
                    meta: {
                        title: '航班列表'
                    },
                    component: FlightsTable
                }
            ]
        },
        {
            path: '/login',
            name: 'login',
            meta: {
                title: '登录'
            },
            component: Login
        },
        {
            path: '/register',
            name: 'register',
            meta: {
                title: '注册'
            },
            component: Register
        },
    ],
    mode: 'history',
})

// eslint-disable-next-line
router.afterEach((to, _from) => {
    document.title = to.meta.title || DEFAULT_TITLE
})

export default router
