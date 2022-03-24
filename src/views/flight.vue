<template>
    <v-app id="flight">
        <v-content class="grey lighten-2">
        <v-container class="mt-3" style="width: 80%;">
            <v-card>
                <v-carousel cycle>
                    <v-carousel-item
                        v-for="(item,i) in items"
                        :key="i"
                        :src="item.src"
                    ></v-carousel-item>
                </v-carousel>
                
                    <v-row>
                        <v-col :cols="1">
                        </v-col>
                        <v-col :cols="2">
                            <v-card flat="">
                                <v-card-title v-text="flghtInfo.flght_id">
                                </v-card-title>
                                <v-card-text>
                                    {{flghtInfo.company}} | {{flghtInfo.airplane}}
                                </v-card-text>
                            </v-card>
                        </v-col>
                        <v-col :cols="3">
                            <v-card flat="">
                                <v-timeline dense>
                                    <v-timeline-item
                                    color="pink"
                                    small
                                    >
                                        <v-row class="pt-1">
                                            <v-col>
                                                <strong>{{flghtInfo.depart_time}}</strong>
                                            </v-col>
                                            <v-col>
                                                <strong>{{flghtInfo.from}}</strong>
                                            </v-col>
                                        </v-row>
                                    </v-timeline-item>
                                    <v-timeline-item
                                    color="teal lighten-3"
                                    small
                                    >
                                        <v-row class="pt-1">
                                            <v-col>
                                                <strong>{{flghtInfo.arrive_time}}</strong>
                                            </v-col>
                                            <v-col>
                                                <strong>{{flghtInfo.to}}</strong>
                                            </v-col>
                                        </v-row>
                                    </v-timeline-item>
                                </v-timeline>
                            </v-card>
                        </v-col>

                        <v-col :cols="6">
                            <v-card flat="">
                                <Graph ref="graph" :nodes="nodes" :links="links"></Graph>
                            </v-card>
                        </v-col>
                    </v-row>

                    <v-row justify='center'>
                        <v-col :cols="10">
                            <v-card-title>
                                机票信息
                            </v-card-title>
                            <v-card-text>
                                <v-divider></v-divider>
                            </v-card-text>

                            <v-row justify='center'>
                                <v-col
                                    v-for="(ticket, i) in tickets"
                                    :key="i"
                                    cols="5"
                                >
                                        <v-card>
                                            <v-img
                                            class="white--text align-end"
                                            height="120px"
                                            src="../assets/tickets_head.jpeg"
                                            >
                                            <v-card-title >
                                                    {{ticket.flight_id}}
                                                <br/>
                                                    {{ticket.ticket_type}}
                                            </v-card-title>
                                            </v-img>
                                            <v-divider></v-divider>
                                            <v-card-text>
                                                <v-row>
                                                    <v-col>
                                                        <table>
                                                            <tr>
                                                            <td><b> 票价：</b></td> <td> ¥{{ ticket.price }} </td>
                                                            </tr>
                                                            <tr>
                                                            <td><b> 剩余票数：</b></td> <td> {{ ticket.left_tickets }} </td>
                                                            </tr>
                                                        </table>
                                                    </v-col>
                                                    <v-col cols="3" align-self="end">
                                                        <v-btn
                                                            outlined
                                                            rounded
                                                            text
                                                            @click="clickBuyTicket(ticket.ticket_type)"
                                                        >
                                                            购票
                                                        </v-btn>
                                                    </v-col>
                                                </v-row>
                                            </v-card-text>
                                        </v-card>
                                    </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                </v-col>
                            </v-row>
                        </v-col>
                    </v-row>
            </v-card>

            <v-btn
                fab
                bottom
                right
                fixed
                color="blue darken-2"
                dark
                @click="backHome"
            >
                <v-icon>mdi-home</v-icon>
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

        </v-container>
        </v-content>
    </v-app>
</template>
<script>
    import Graph from '@/components/Graph'
    import { getFlightDetail, getFlightWorker, buyTicket } from "@/api/core";
    export default {
        components: {
            Graph,
        },

        data() {
            return {
                flight_id: "", 
                flghtInfo: {
                    flight_id: "",
                    current_status: "",
                    company: "",
                    airplane: "",
                    depart_time: "",
                    from: "",
                    arrive_time: "",
                    to: "",
                    all_tickets: 0,
                    left_tickets: 0,
                    date: "",
                    eprice: 0,
                    cprice: 0,
                    ontime: true
                },

                errorDialog: false,
                errorMsg: {
                    title: "",
                    content: ""
                },

                snackbar: false,
                snackbarMsg: "",

                tickets: [],
                nodes: [],
                links: [],
                items: [
                    {
                        src: 'https://s3.ax1x.com/2020/12/18/rYZbD0.jpg',
                    },
                    {
                        src: 'https://s3.ax1x.com/2020/12/18/rYZogs.jpg',
                    },
                    {
                        src: 'https://s3.ax1x.com/2020/12/18/rYZTvn.jpg',
                    },
                    {
                        src: 'https://s3.ax1x.com/2020/12/18/rYZI3j.jpg',
                    },
                    {
                        src: 'https://s3.ax1x.com/2020/12/18/rYZHuq.jpg',
                    },
                    {
                        src: 'https://s3.ax1x.com/2020/12/18/rYZqbV.jpg',
                    },
                ],
            }
        },

        mounted(){
            this.flight_id = this.$route.query.flight_id ? this.$route.query.flight_id : null;
            getFlightDetail(this.flight_id).then(res=>{
                // console.log(res)
                this.flghtInfo = res.data
                this.tickets.push({
                        flight_id: this.flight_id,
                        ticket_type: "经济舱",
                        left_tickets: this.flghtInfo.left_e_tickets,
                        price: this.flghtInfo.eprice,
                    })
                this.tickets.push({
                        flight_id: this.flight_id,
                        ticket_type: "商务舱",
                        left_tickets: this.flghtInfo.left_c_tickets,
                        price: this.flghtInfo.cprice,
                    })
            }).catch(err=>{
                // console.log(err)
                this.errorMsg.title = "获取航班信息失败"
                this.errorMsg.content = err.response.data.error_msg
                this.errorDialog = true
            })

            let flight_nodes = {
                    name: this.flight_id,
                    is_flight: true,
                    info: this.flight_id
                }
            this.nodes.push(flight_nodes)

            getFlightWorker({
                    flight: this.flight_id
                }).then(res=>{
                // console.log(res)
                res.data.flights.map((value) =>{
                    // console.log(value)
                    let work_nodes = {
                        name: value.name,
                        is_flight: false,
                        info: {
                            work_time: value.fly_time,
                            company: value.company,
                            employ_time: value.emp_date,
                            job: value.pos
                        }
                    }
                    this.nodes.push(work_nodes)
                    let work_links = {
                        source: this.flight_id,
                        target: value.name,
                        relation: value.pos
                    }
                    this.links.push(work_links)
                })
                this.$refs.graph.updateGraph()
            }).catch(err=>{
                // console.log(err)
                this.errorMsg.title = "获取航班工作人员信息失败"
                this.errorMsg.content = err.response.data.error_msg
                this.errorDialog = true
            })
        },

        methods: {
            backHome(){
                this.$router.push({
                    path: '/',
                })
            },
            
            clickBuyTicket(ticket_type){
                buyTicket({
                    flight_id: this.flight_id,
                    seat_id: ticket_type == "经济舱"? this.flghtInfo.left_e_tickets : this.flghtInfo.left_c_tickets,
                    ticket_type: ticket_type,
                    gate: "-1",
                    price: ticket_type == "经济舱"? this.flghtInfo.eprice : this.flghtInfo.cprice,
                    sale_time: new Date().toISOString().substr(0, 10),
                    detail: ""
                // eslint-disable-next-line no-unused-vars
                }).then(res=>{
                    // console.log(res)
                    this.snackbar = true
                    this.snackbarMsg = "购票成功"
                    getFlightDetail(this.flight_id).then(res=>{
                        this.tickets = []
                        this.tickets.push({
                                flight_id: this.flight_id,
                                ticket_type: "经济舱",
                                left_tickets: res.data.left_e_tickets,
                                price: res.data.eprice,
                            })
                        this.tickets.push({
                                flight_id: this.flight_id,
                                ticket_type: "商务舱",
                                left_tickets: res.data.left_c_tickets,
                                price: res.data.cprice,
                            })
                    }).catch(err=>{
                        // console.log(err)
                        this.errorMsg.title = "更新票务信息失败"
                        this.errorMsg.content = err.response.data.error_msg
                        this.errorDialog = true
                    })
                }).catch(err=>{
                    // console.log(err.response.data)
                    this.errorMsg.title = "购票失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true
                })
            }
            
        }
    }

</script>
<style>

</style>
