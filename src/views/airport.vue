<template>
    <v-app id="airport">
        <div class="background">
            <v-btn
                fab
                top
                left
                fixed
                @click="backHome"
            >
                <v-icon>mdi-home</v-icon>
            </v-btn>
            <v-row>
                <v-col cols="8">
                    <EchartMap ref="map" :mapData="mapData" style="width: 100%;height: 100vh" :mapOption="{
                            'title': `${airport_name}航线信息图`,
                            'titleColor': '#ffffff'
                    }"></EchartMap>
                </v-col>
                <v-col cols="4">
                    <v-row>
                        <v-col>
                            <RingChart ref="ring" color="#289DE7" :data="{value: ontime, text:'历史准点率'}"/>
                        </v-col>

                        <v-col>
                            <PieChart ref="pie"  title="航司航班量占比" :companies="companies"></PieChart>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col>
                            <MixChart ref="mix" :data="flight_flow"></MixChart>
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
        </div>

        <v-snackbar
            :timeout="0"
            :value="true"
            left
            bottom
            color="#435268"
            v-model="weatherShow"
        >
            <v-card
                color="#435268"
                width="100%"
                max-width="320"
                dark
                flat
                v-if="getWeatherSuccess"
            >
                <v-list-item two-line>
                    <v-list-item-content>
                        <v-list-item-title class="headline mb-1">
                            当前机场天气信息
                        </v-list-item-title>
                        <v-list-item-subtitle>{{this.weatherInfo.real.station.province}} {{this.weatherInfo.real.station.city}} | {{this.weatherInfo.real.publish_time}}</v-list-item-subtitle>
                    </v-list-item-content>
                    <v-btn
                        icon
                        small
                        @click="weatherShow=false"
                    >
                        <v-icon>mdi-arrow-collapse</v-icon>
                    </v-btn>
                </v-list-item>
                <v-divider></v-divider>

                <v-card-text>
                <v-row align="center">
                    <v-col
                    class="display-1"
                    cols="6"
                    >
                        <v-row>
                            <v-icon large>{{this.weatherIcon}}</v-icon>
                            &nbsp;{{this.weatherInfo.real.weather.info}}
                        </v-row>
                        <v-row>
                            {{this.weatherInfo.real.weather.temperature}}&deg;C
                        </v-row>
                    </v-col>
                    <v-col
                    cols="6"
                    >
                        <v-row>
                            降水：{{this.weatherInfo.real.weather.rain}}mm
                        </v-row>
                        <v-row>
                            气压：{{this.weatherInfo.real.weather.airpressure}}hPa
                        </v-row>
                        <v-row>
                            湿度：{{this.weatherInfo.real.weather.humidity}}%
                        </v-row>
                        <v-row>
                            风向：{{this.weatherInfo.real.wind.direct}}
                        </v-row>
                        <v-row>
                            风力：{{this.weatherInfo.real.wind.power}}
                        </v-row>
                    </v-col>
                </v-row>
                </v-card-text>
            </v-card>

            <v-card color="#435268"
                width="100%"
                max-width="320"
                dark
                flat
                v-if="!getWeatherSuccess"
            >
                <v-card-text>
                    <v-row>
                    <span>暂无天气信息</span>
                    <v-spacer></v-spacer>
                    <v-btn
                        icon
                        small
                        right
                        @click="weatherShow=false"
                    >
                        <v-icon>mdi-arrow-collapse</v-icon>
                    </v-btn>
                    </v-row>
                </v-card-text>
            </v-card>
        </v-snackbar>

        <v-btn
            fab
            bottom
            left
            fixed
            dark
            outlined
            color="blue lighten-3"
            v-if="!weatherShow"
            @click="weatherShow=true"
        >
            <v-icon>mdi-weather-partly-cloudy</v-icon>
        </v-btn>

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
import RingChart from '@/components/RingChart'
import PieChart from '@/components/PieChart'
import MixChart from '@/components/MixChart'
import { getStationCode, getWeather } from '@/api/weather'
import { getAirportDetail, queryAirlines, getAirportOntime, getAirportCpn, getAirportFlow } from '@/api/core'
export default {
    components: {
            EchartMap,
            RingChart,
            PieChart,
            MixChart
    },
    data() {
        return {
            airport_id: "",
            airport_name: "",
            airport_info: null,
            getWeatherSuccess: false,
            weatherShow: true,
            weatherInfo: null,
            weatherIcon: "",
            mapData: [],
            ontime: 0,
            companies: [],

            flight_flow: [],

            errorDialog: false,
            errorMsg: {
                title: "",
                content: ""
            },
        }
    },
    mounted() {
        this.airport_id = this.$route.query.airport_id ? this.$route.query.airport_id : null;
        // console.log(this.airport_id)
        // 获取天气信息
        getStationCode({
                 q: this.airport_id
            }).then(res => {
                // console.log(res);
                var stationCode = res.data[0].stationCode;
                getWeather(stationCode)
                    .then(res => {
                        this.getWeatherSuccess = true
                        this.weatherInfo = res.data;
                        // console.log(this.weatherInfo);
                        this.weatherIcon = this.weatherInfo.real.weather.info == "晴" ? "mdi-weather-sunny":
                                            this.weatherInfo.real.weather.info == "多云" ? "mdi-weather-partly-cloudy":
                                            this.weatherInfo.real.weather.info.indexOf("阴")>=0 ? "mdi-weather-cloudy":
                                            this.weatherInfo.real.weather.info == "雷阵雨" ? "mdi-weather-lightning":
                                            this.weatherInfo.real.weather.info == "雨夹雪" ? "weather-snowy-rainy":
                                            this.weatherInfo.real.weather.info == "雷电" ? "mdi-weather-lightning":
                                            this.weatherInfo.real.weather.info == "冰雹" ? "mdi-weather-hail":
                                            this.weatherInfo.real.weather.info == "台风" ? "mdi-weather-hurricane":
                                            this.weatherInfo.real.weather.info.indexOf("龙卷") ? "mdi-weather-tornado":
                                            this.weatherInfo.real.weather.info.indexOf("雾") ? "mdi-weather-fog":
                                            this.weatherInfo.real.weather.info.indexOf("暴雨")>=0 ? "mdi-weather-pouring":
                                            this.weatherInfo.real.weather.info.indexOf("雨")>=0 ? "mdi-weather-rainy":
                                            this.weatherInfo.real.weather.info.indexOf("暴雪")>=0 ? "mdi-weather-snowy-heavy":
                                            this.weatherInfo.real.weather.info.indexOf("雪")>=0 ? "mdi-weather-snowy":
                                            this.weatherInfo.real.weather.info.indexOf("风")>=0 ? "mdi-weather-windy": "mdi-weather-partly-cloudy";
                    })
                    // eslint-disable-next-line no-unused-vars
                    .catch((e) => {
                        // console.log('获取天气数据失败');
                        this.errorMsg.title = "获取天气数据失败"
                        this.errorMsg.content = e.response.data.error_msg
                        this.errorDialog = true
                    });

            })
            // eslint-disable-next-line no-unused-vars
            .catch((e) => {
                // console.log('获取天气数据失败');
                this.errorMsg.title = "获取天气数据失败"
                this.errorMsg.content = e.response.data.error_msg
                this.errorDialog = true
            });

        getAirportDetail(this.airport_id).then(res=>{
            // console.log(res)
            this.airport_info = res.data   
                    queryAirlines({
                        airport_id: this.airport_info.airport_name
                    }).then(res=>{
                        // console.log(res.data.airlines)
                        this.mapData = res.data.airlines
                        this.airport_name = this.airport_info.airport_name
                        this.$refs.map.updateMap()
                        
                    }).catch(err=>{
                        // console.log(err)
                        this.errorMsg.title = "获取航线失败"
                        this.errorMsg.content = err.response.data.error_msg
                        this.errorDialog = true
                    })
        }).catch(err=>{
            // console.log(err)
            this.errorMsg.title = "获取机场信息失败"
            this.errorMsg.content = err.response.data.error_msg
            this.errorDialog = true

        })

        // 获取准点率
        getAirportOntime({
            airport_id: this.airport_id
        }).then(res=>{
            this.ontime = res.data.on_time_rate*100
            this.$refs.ring.updateRing(this.ontime)
        }).catch(err=>{
            // console.log(err)
            this.errorMsg.title = "获取准点率失败"
            this.errorMsg.content = err.response.data.error_msg
            this.errorDialog = true
        })

        getAirportCpn({
            airport_id: this.airport_id
        }).then(res=>{
            this.companies = res.data.companies
            //console.log(this.companies)
            this.$refs.pie.updatePie(this.companies)
        }).catch(err=>{
            // console.log(err)
            this.errorMsg.title = "获取机场航司航班占比失败"
            this.errorMsg.content = err.response.data.error_msg
            this.errorDialog = true
        })

        getAirportFlow({
            airport_id: this.airport_id
        }).then(res=>{
            this.flight_flow = res.data.flight_flow
            //console.log(this.companies)
            this.$refs.mix.initChart(this.flight_flow)
        }).catch(err=>{
            // console.log(err)
            this.errorMsg.title = "获取机场日流量失败"
            this.errorMsg.content = err.response.data.error_msg
            this.errorDialog = true
        })

    },
    methods: {
        backHome(){
                this.$router.push({
                    path: '/',
                })
            }
    },
}

</script>

<style>
.background {
    /* background-size: contain; */
    background-color: #2B3648;
}
</style>