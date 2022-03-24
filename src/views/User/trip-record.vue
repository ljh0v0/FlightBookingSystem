<template>
    <v-app id="trip-record">
        <div style="margin-top: 40px; margin-bottom: 40px; margin-left:5%; width: 90%;">
            <v-row>  
                <v-col cols="4">
                    <v-select
                        label="已出行/未出行"
                        outlined
                        :items="type"
                        menu-props="auto"
                        v-model="trip_type"
                    ></v-select>
                </v-col>
            </v-row>
            <v-row justify='center'>
                <v-col
                    v-for="(record, i) in trip_reocrds"
                    :key="i"
                    cols="5"
                >
                        <v-card>
                            <v-img
                            class="white--text align-end"
                            height="120px"
                            src="../../assets/tickets_head.jpeg"
                            >
                            <v-card-text >
                                <v-row>
                                    <v-col align-self='center'>
                                        {{record.from}}
                                        <br/>
                                        {{record.depart_time}}
                                    </v-col>
                                    <v-col align-self='center'>
                                        ----
                                        <v-icon dark>
                                            mdi-send
                                        </v-icon>
                                    </v-col>
                                    <v-col align-self='center'>
                                        {{record.to}}
                                        <br/>
                                        {{record.arrive_time}}
                                    </v-col>
                                </v-row>
                            </v-card-text>
                            </v-img>
                            <v-divider></v-divider>
                            <v-card-text>
                                <v-row>
                                    <v-col>
                                        <table class="record-table">
                                            <tr>
                                            <td><b> 航班号 </b></td> <td> {{ record.flight_id }} </td>
                                            </tr>
                                            <tr>
                                            <td><b> 座位号 </b></td> <td> {{ record.seat_id }} </td>
                                            </tr>
                                            <tr>
                                            <td><b> 座位级别 </b></td> <td> {{ record.ticket_type }} </td>
                                            </tr>
                                            <tr>
                                            <td><b> 登机口 </b></td>  <td> {{ record.gate}} </td>
                                            </tr>
                                        </table>
                                    </v-col>
                                    <v-col cols="3" align-self="end">
                                        <v-btn
                                            outlined
                                            rounded
                                            text
                                            @click="deleteTicket(record.flight_id, record.seat_id)"
                                        >
                                            退票
                                        </v-btn>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </v-card>
                    </v-col>
            </v-row>
        </div>

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

        <v-snackbar
            v-model="snackbar"
            color="success"
            text
        >
            {{ snackbarMsg }}

                <v-btn
                    text
                    dark
                    @click="snackbar = false"
                >
                    Close
                </v-btn>
        </v-snackbar>

    </v-app>
</template>
<script>
    import { queryTicket, delTicket } from '@/api/core'
    export default {
        data() {
            return {
                type: ['已出行', '未出行'],
                trip_reocrds: [],
                trip_type: null,

                errorDialog: false,
                errorMsg: {
                    title: "",
                    content: ""
                },

                snackbar: false,
                snackbarMsg: "",
            }
        },

        mounted() {
            queryTicket().then(res=>{
                // console.log(res)
                this.trip_reocrds = res.data.airports
                this.trip_reocrds.map((value)=>{
                    value.gate = value.gate == -1 ? "尚无登机口信息" : res.data.airports.gate
                })
            }).catch(err=>{
                // console.log(err)
                this.errorMsg.title = "获取行程记录失败"
                this.errorMsg.content = err.response.data.error_msg
                this.errorDialog = true
            })
        },

        methods: {
            deleteTicket(flight_id, seat_id){
                delTicket({
                    flight_id: flight_id,
                    seat_id: seat_id
                // eslint-disable-next-line no-unused-vars
                }).then(res=>{
                    // console.log(res)
                    this.snackbar = true
                    this.snackbarMsg = "退票成功"
                    this.updateTicket()
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "退票失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true
                })
            },

            updateTicket(){
                queryTicket({
                    status: this.trip_type == null ? null :
                            this.trip_type == '已出行' ? 1 : 0
                }).then(res=>{
                    // console.log(res)
                    this.trip_reocrds = res.data.airports
                    this.trip_reocrds.map((value)=>{
                        value.gate = value.gate == -1 ? "尚无登机口信息" : res.data.airports.gate
                    })
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "获取行程记录失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true
                })
            }
        },

        watch: {
            trip_type(val){
                queryTicket({
                    status: val == '已出行' ? 1 : 0
                }).then(res=>{
                    // console.log(res)
                    this.trip_reocrds = res.data.airports
                    this.trip_reocrds.map((value)=>{
                        value.gate = value.gate == -1 ? "尚无登机口信息" : res.data.airports.gate
                    })
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "获取行程记录失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true
                })
            }
        }
    }

</script>
<style>

</style>