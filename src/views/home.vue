<template>
    <v-app id="home">

            <!-- 航班查询窗口 -->
            <v-navigation-drawer
                v-model="searchFlightDrawer"
                hide-overlay
                width=400
                absolute
                right
            >
            <v-card class="mx-auto" flat>
                <v-card-title>
                    <span class="headline">航班查询</span>
                    <v-spacer></v-spacer>
                    <v-btn
                        icon
                        small
                        @click="closeSearchFlight"
                    >
                        <v-icon>mdi-close-circle-outline</v-icon>
                    </v-btn>
                </v-card-title>
                <v-divider></v-divider>
                <v-form ref="flightForm" style="margin-top: 40px; margin-bottom: 25px; margin-left:5%; width: 90%;">
                    <v-select
                        label="出发地"
                        outlined
                        :items="cities"
                        prepend-icon="mdi-airplane-takeoff"
                        menu-props="auto"
                        v-model="flightInfo.from"
                    ></v-select>
                    <v-select
                        label="目的地"
                        outlined
                        :items="cities"
                        prepend-icon="mdi-airplane-landing"
                        menu-props="auto"
                        v-model="flightInfo.to"
                    ></v-select>
                    <v-menu
                        ref="menu"
                        v-model="datePiker"
                        :close-on-content-click="false"
                        :return-value.sync="flightInfo.date"
                        transition="scale-transition"
                        offset-y
                        min-width="290px"
                    >
                        <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                            v-model="flightInfo.date"
                            label="出发日期"
                            prepend-icon="mdi-calendar"
                            readonly
                            outlined
                            v-bind="attrs"
                            v-on="on"
                        ></v-text-field>
                        </template>
                        <v-date-picker
                        v-model="flightInfo.date"
                        no-title
                        scrollable
                        >
                        <v-spacer></v-spacer>
                        <v-btn
                            text
                            color="primary"
                            @click="menu = false"
                        >
                            Cancel
                        </v-btn>
                        <v-btn
                            text
                            color="primary"
                            @click="$refs.menu.save(flightInfo.date)"
                        >
                            OK
                        </v-btn>
                        </v-date-picker>
                    </v-menu>
                    <v-select
                        label="航空公司"
                        outlined
                        :items="companies"
                        prepend-icon="mdi-bag-carry-on"
                        menu-props="auto"
                        v-model="flightInfo.company"
                    ></v-select>
                    <v-btn
                    outlined
                    class="ma-2"
                    large
                    right
                    @click="searchFlight"
                    >
                        <v-icon>mdi-magnify</v-icon>
                        查询航班
                    </v-btn>
                </v-form>
            </v-card>
            </v-navigation-drawer>

            <!-- 机场查询窗口 -->
            <v-navigation-drawer
                v-model="searchAirportDrawer"
                hide-overlay
                width=400
                absolute
                right
            >
                <v-card class="mx-auto" flat>
                    <v-card-title>
                        <span class="headline">机场查询</span>
                        <v-spacer></v-spacer>
                        <v-btn
                            icon
                            small
                            @click="closeSearchAirport"
                        >
                            <v-icon>mdi-close-circle-outline</v-icon>
                        </v-btn>
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-form ref="airportForm" style="margin-top: 40px; margin-bottom: 40px; margin-left:5%; width: 90%;">
                        <v-select
                            label="所在城市"
                            outlined
                            :items="cities"
                            prepend-icon="mdi-map-marker"
                            menu-props="auto"
                            v-model="airportInfo.city_name"
                        ></v-select>
                        <v-text-field
                            label="机场名"
                            outlined
                            prepend-icon="mdi-card-text-outline"
                            v-model="airportInfo.airport_name"
                        ></v-text-field>
                        <v-btn
                        outlined
                        class="ma-2"
                        large
                        right
                        @click="searchAirport"
                        >
                            <v-icon>mdi-magnify</v-icon>
                            查询机场
                        </v-btn>
                    </v-form>
                    <v-divider></v-divider>

                    <v-list three-line v-if="showAirpots">
                        <template v-for="(airport, index) in airportData" >
                            <v-list-item
                                :key="airport.airport_name"
                                @click="clickAirpot(airport.airport_id)"
                            >
                                <v-list-item-content>
                                    <v-list-item-title v-text="airport.airport_name"></v-list-item-title>
                                    <v-list-item-subtitle class="text--primary">
                                        {{airport.city}} | {{airport.start_time}}
                                    </v-list-item-subtitle>
                                    <v-list-item-subtitle v-text="airport.location"></v-list-item-subtitle>
                                </v-list-item-content>
                            </v-list-item>
                            <v-divider :key="index"></v-divider>
                        </template>
                    </v-list>
                </v-card>
            </v-navigation-drawer>

            <!-- 航班信息窗口 -->
            <v-navigation-drawer
                v-model="showFlights"
                hide-overlay
                width=400
                absolute
                right
            >
            <v-card class="mx-auto" flat>
                <v-card-title>
                    <span class="headline">航班信息</span>
                    <v-spacer></v-spacer>
                    <v-btn
                        icon
                        small
                        @click="closeFlights"
                    >
                        <v-icon>mdi-close-circle-outline</v-icon>
                    </v-btn>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                    <v-container>
                        <v-col
                        v-for="(flight, i) in flghtsData"
                        :key="i"
                        cols="12"
                        >
                            <v-card @click="clickFlight(flight.flight_id)">
                                <v-img
                                class="white--text align-end"
                                height="80px"
                                src="../assets/tickets_head.jpeg"
                                >
                                <v-list-item two-line dark>
                                    <v-list-item-content>
                                        <v-list-item-title class="headline mb-1">
                                            {{flight.flight_id}}
                                        </v-list-item-title>
                                        <v-list-item-subtitle>{{flight.company}} | {{flight.airplane}}</v-list-item-subtitle>
                                    </v-list-item-content>
                                </v-list-item>
                                </v-img>
                                <v-divider></v-divider>
                                <v-card-text>
                                <v-row>
                                    <v-col align-self='center'>
                                        {{flight.depart_time}}
                                        <br/>
                                        {{flight.from}}
                                    </v-col>
                                    <v-col align-self='center'>
                                        ----
                                        <v-icon>
                                            mdi-send
                                        </v-icon>
                                    </v-col>
                                    <v-col align-self='center'>
                                        {{flight.arrive_time}}
                                        <br/>
                                        {{flight.to}}
                                    </v-col>
                                </v-row>
                                </v-card-text>
                            </v-card>
                        </v-col>
                    </v-container>
                </v-card-text>
            </v-card>
            </v-navigation-drawer>

            <!-- 菜单 -->
            <v-speed-dial
                v-model="openMenu"
                top
                left
                fixed
                direction='bottom'
                transition='slide-y-transition'
            >
                <template v-slot:activator>
                    <v-fab-transition>
                        <v-btn
                            v-model="openMenu"
                            fab
                            :key="activeFab.icon"
                        >
                            <v-icon>{{ activeFab.icon }}</v-icon>
                        </v-btn> 
                    </v-fab-transition>
                </template>
                <v-tooltip right attach>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            fab
                            small
                            v-bind="attrs"
                            v-on="on"
                            @click="onSearchFligtDrawer"
                        >
                            <v-icon>mdi-magnify</v-icon>
                        </v-btn>
                    </template>
                    <span>航班查询</span>
                </v-tooltip>
                <v-tooltip right attach>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            fab
                            small
                            v-bind="attrs"
                            v-on="on"
                            @click="onSearchAirportDrawer"
                        >
                            <v-icon>mdi-airport</v-icon>
                        </v-btn>
                    </template>
                    <span>机场查询</span>
                </v-tooltip>
                <v-tooltip right attach>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            fab
                            small
                            v-bind="attrs"
                            v-on="on"
                            @click="clickLogin"
                        >
                            <v-icon>{{isLogined? 'mdi-logout' : 'mdi-login'}}</v-icon>
                        </v-btn>
                    </template>
                    <span>{{isLogined? '退出账号' : '登录账号'}}</span>
                </v-tooltip>
                <v-tooltip right attach>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            fab
                            small
                            v-bind="attrs"
                            v-on="on"
                            @click="clickUserCenter"
                        >
                            <v-icon>mdi-account-circle</v-icon>
                        </v-btn>
                    </template>
                    <span>用户中心</span>
                </v-tooltip>
                <v-tooltip right attach>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            fab
                            small
                            v-bind="attrs"
                            v-on="on"
                            v-if="isManager"
                            @click="clickManager"
                        >
                            <v-icon>mdi-cogs</v-icon>
                        </v-btn>
                    </template>
                    <span>管理端</span>
                </v-tooltip>
            </v-speed-dial>

            <!-- 航线图 -->
            <EchartMap  ref="map" :mapData="mapData" style="width: 100%;height: 100vh" :mapOption="{
                'title': '',
                'titleColor': 'pink'
            }"></EchartMap>

            <v-dialog
                v-model="pleaseLogin"
                max-width="290"
            >
                <v-card>
                    <v-card-title class="headline">
                        请先登录
                    </v-card-title>
                    <v-card-actions>
                    <v-spacer></v-spacer>
                        <v-btn
                            color="primary"
                            text
                            @click="clickLogin"
                        >
                            Login
                        </v-btn>
                        <v-btn
                            color="red darken-2"
                            text
                            @click="pleaseLogin = false"
                        >
                            Close
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>


            <v-dialog
                v-model="errorDialog"
                max-width="290"
            >
                <v-card>
                    <v-card-title class="headline">
                        {{errorMsg.title}}
                    </v-card-title>
                    <v-card-text>{{errorMsg.content}}</v-card-text>
                    <v-card-actions>
                    <v-spacer></v-spacer>
                        <v-btn
                            color="red darken-2"
                            text
                            @click="errorDialog = false"
                        >
                            Close
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
    </v-app>
</template>
<script>
    import EchartMap from '@/components/EchartMap'
    import { getAllAirlines, getCities, queryFlight, queryAirlines, queryAirport, queryCompany, getMyInfo } from "@/api/core";
    export default {
        components: {
            EchartMap
        },
        data() {
            return {
                    openMenu: false,
                    searchFlightDrawer:false,
                    searchAirportDrawer:false,
                    showFlights: false,
                    showAirpots: false,

                    isManager: false,
                    isLogined: false,

                    datePiker:false,

                    errorDialog: false,
                    errorMsg: {
                        title: "",
                        content: ""
                    },

                    pleaseLogin: false,

                    airlineInfo: {
                        from: null,
                        to: null,
                        airport_id: null
                    },
                    defaultAirlineInfo: {
                        from: null,
                        to: null,
                        airport_id: null
                    },

                    cities: [],
                    companies: [],
                    mapData: [],

                    flightInfo: {
                        from: null,
                        to: null,
                        date: null,
                        company: null
                    },
                    defaultFlightInfo: {
                        from: null,
                        to: null,
                        date: null,
                        company: null
                    },
                    flghtsData:[],

                    airportInfo: {
                        city_name: null,
                        airport_name: null
                    },
                    airportData: []
            }
        },

        mounted(){
            getCities().then(res=>{
                // console.log(res)
                var cityData = res.data.cities
                cityData.map((value) => {
                    this.cities.push(value.name)
                })
                // console.log(this.cities)

            }).catch(err=>{
                // console.log(err)
                this.errorMsg.title = "获取城市信息失败"
                this.errorMsg.content = err.response.data.error_msg
                this.errorDialog = true
            })

            queryCompany().then(res=>{
                // console.log(res)
                var cpnData = res.data.companies
                cpnData.map((value) => {
                    this.companies.push(value.full_name)
                })
                // console.log(this.cities)

            }).catch(err=>{
                // console.log(err)
                this.errorMsg.title = "获取航空公司失败"
                this.errorMsg.content = err.response.data.error_msg
                this.errorDialog = true
            })

            getAllAirlines().then(res=>{
                // console.log(res)
                this.mapData = res.data.airlines
                this.$refs.map.updateMap()
                
            }).catch(err=>{
                // console.log(err)
                this.errorMsg.title = "获取航线失败"
                this.errorMsg.content = err.response.data.error_msg
                this.errorDialog = true

            })

            getMyInfo().then(res=>{
                // console.log(res)
                this.isManager = res.data.auth
                this.isLogined = true
            }).catch(err=>{
                // console.log(err.response.data)
                this.isManager = false
                this.isLogined = false
                if(err.response.data.code == 520){
                    this.pleaseLogin = true
                }else{
                    this.errorMsg.title = "获取用户信息失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true
                }
            })
        },

        computed: {
            activeFab () {
                if (this.openMenu) {
                    return { color: 'success', icon: 'mdi-close' }
                }else{
                    return { color: 'success', icon: 'mdi-airplane' }
                }
            },
        },

        methods: {
            onSearchFligtDrawer(){
                this.searchFlightDrawer=!this.searchFlightDrawer
                this.searchAirportDrawer=false
                this.showFlights=false
                this.showAirpots=false
            },

            closeSearchFlight(){
                this.searchFlightDrawer = false
                // this.airlineInfo = this.defaultAirlineInfo
                this.$refs.flightForm.reset()
            },

            onSearchAirportDrawer(){
                this.searchFlightDrawer=false
                this.searchAirportDrawer=!this.searchAirportDrawer
                this.showFlights=false
                this.showAirpots=false
            },

            closeSearchAirport(){
                this.searchAirportDrawer=false
                this.$refs.airportForm.reset()
            },

            searchFlight(){
                // this.showFlights = true;
                // console.log(this.flightInfo)
                this.airlineInfo = this.defaultAirlineInfo
                this.airlineInfo.from = this.flightInfo.from
                this.airlineInfo.to = this.flightInfo.to
                queryAirlines(this.airlineInfo).then(res=>{
                    // console.log(res)
                    this.mapData = res.data.airlines
                    this.$refs.map.updateMap()
                    
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "获取航线失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true
                })
                queryFlight(this.flightInfo).then(res=>{
                    // console.log(res)
                    this.flghtsData = res.data.flights
                    this.showFlights = true;
                    
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "获取航班信息失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true

                })
            },

            clickFlight(flight_id){
                if(this.isLogined){
                    this.$router.push({
                        path: '/flight',
                        query: {
                            flight_id: flight_id
                        }
                    })
                }else{
                    this.pleaseLogin = true
                }
            },

            closeFlights(){
                this.showFlights=false
                getAllAirlines().then(res=>{
                    // console.log(res)
                    this.mapData = res.data.airlines
                    this.$refs.map.updateMap()
                    
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "获取航线失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true

                })
            },

            searchAirport(){
                queryAirport(this.airportInfo).then(res=>{
                    // console.log(res)
                    this.airportData = res.data.airports
                    this.showAirpots=true
                    
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "获取机场信息失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true

                })
                
            },

            clickAirpot(airport_id){
                if(this.isLogined){
                    this.$router.push({
                        path: '/airport',
                        query: {
                            airport_id: airport_id
                        }
                    })
                }else{
                    this.pleaseLogin = true
                }
                
            },

            clickUserCenter(){
                if(this.isLogined){
                    this.$router.push({
                        path: '/user',
                    })
                }else{
                    this.pleaseLogin = true
                }
                
            },

            clickManager(){
                if(this.isLogined && this.isManager){
                    this.$router.push({
                        path: '/manager',
                    })
                }else{
                    this.errorMsg.title = "对不起，您没有管理权限"
                    this.errorMsg.content = ""
                    this.errorDialog = true
                }
            },

            clickLogin(){
                if(this.isLogined){
                    this.isLogined = false
                    this.$cookie.set('access-token',"")
                }else{
                    this.$router.push({
                        path: '/login',
                    })
                }
            },
        }
    }

</script>
<style>
    * {
        margin: 0;
        padding: 0;
    }

</style>
