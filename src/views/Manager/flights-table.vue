<template>
    <v-app id="user-info">
        <v-row justify='center'> 
            <v-col>
              <v-data-table
                :headers="headers"
                :items="flights"
                min-height="70vh"
            >
                <template v-slot:top>
                <v-toolbar
                    flat
                >
                    <v-toolbar-title>航班信息</v-toolbar-title>
                    <v-divider
                        class="mx-4"
                        inset
                        vertical
                    ></v-divider>
                    <v-spacer></v-spacer>
                    <v-dialog
                        v-model="dialogCreate"
                        max-width="500px"
                    >
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn
                            color="primary"
                            dark
                            class="mb-2"
                            v-bind="attrs"
                            v-on="on"
                        >
                            创建新航班
                        </v-btn>
                    </template>
                    <v-card>
                        <v-card-title>
                        <span class="headline">创建航班</span>
                        </v-card-title>

                        <v-card-text>
                            <v-container>
                                <v-form ref="form" lazy-validation style="margin-top: 10px; margin-bottom: 10px;">
                                    <v-row>
                                        <v-col>
                                            <v-text-field
                                                label="航班号"
                                                outlined
                                                v-model="newFlightInfo.flight_id"
                                                :rules="[v => !!v || '请输入航班号']"
                                            ></v-text-field>
                                        </v-col>
                                        <v-col>
                                            <v-select
                                                label="航班状态"
                                                outlined
                                                v-model="newFlightInfo.current_status"
                                                :items="status"
                                                menu-props="auto"
                                                :rules="[v => !!v || '请选择航班状态']"
                                            ></v-select>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <v-select
                                                label="所属航空公司"
                                                outlined
                                                v-model="newFlightInfo.company"
                                                :items="companies"
                                                menu-props="auto"
                                                :rules="[v => !!v || '请选择航空公司']"
                                            ></v-select>
                                        </v-col>
                                        <v-col>
                                            <v-text-field
                                                label="飞机编号"
                                                outlined
                                                v-model="newFlightInfo.airplane"
                                                :rules="[v => !!v || '请填写飞机编号']"
                                            ></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <v-text-field
                                                label="航线编号"
                                                outlined
                                                v-model="newFlightInfo.airline"
                                                :rules="[v => !!v || '请填写航线编号']"
                                            ></v-text-field>
                                        </v-col>
                                        <v-col>
                                            <v-text-field
                                                label="出发日期"
                                                outlined
                                                v-model="newFlightInfo.date"
                                                :rules="[v => !!v || '请填写出发日期']"
                                            ></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <v-select
                                                label="出发机场"
                                                outlined
                                                v-model="newFlightInfo.from"
                                                :items="airports"
                                                menu-props="auto"
                                                :rules="[v => !!v || '请选择出发机场']"
                                            ></v-select>
                                        </v-col>
                                        <v-col>
                                            <v-text-field
                                                label="出发时间"
                                                outlined
                                                v-model="newFlightInfo.depart_time"
                                                :rules="[v => !!v || '请填写出发时间']"
                                            ></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <v-select
                                                label="到达机场"
                                                outlined
                                                v-model="newFlightInfo.to"
                                                :items="airports"
                                                menu-props="auto"
                                                :rules="[v => !!v || '请选择到达机场']"
                                            ></v-select>
                                        </v-col>
                                        <v-col>
                                            <v-text-field
                                                label="到达时间"
                                                outlined
                                                v-model="newFlightInfo.arrive_time"
                                                :rules="[v => !!v || '请填写到达时间']"
                                            ></v-text-field>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <v-text-field
                                                label="剩余票数"
                                                outlined
                                                v-model="newFlightInfo.left_tickets"
                                                :rules="[v => !!v || '请填写剩余票数']"
                                            ></v-text-field>
                                        </v-col>
                                        <v-col>
                                            <v-radio-group
                                            label="是否准点"
                                            v-model="newFlightInfo.ontime"
                                            row
                                            >
                                            <v-radio
                                                label="是"
                                                :value="true"
                                            ></v-radio>
                                            <v-radio
                                                label="否"
                                                :value="false"
                                            ></v-radio>
                                            </v-radio-group>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                             <v-text-field
                                                label="经济舱票价"
                                                outlined
                                                v-model="newFlightInfo.eprice"
                                                :rules="[v => !!v || '请输入经济舱票价']"
                                            ></v-text-field>
                                        </v-col>
                                        <v-col>
                                            <v-text-field
                                                label="商务舱票价"
                                                outlined
                                                v-model="newFlightInfo.cprice"
                                                :rules="[v => !!v || '请输入商务舱票价']"
                                            ></v-text-field>
                                        </v-col>
                                    </v-row>
                                </v-form>
                            </v-container>
                        </v-card-text>

                        <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="blue darken-1"
                            text
                            @click="dialogCreate  = false"
                        >
                            取消
                        </v-btn>
                        <v-btn
                            color="blue darken-1"
                            text
                            @click="createNewFlight"
                        >
                            创建
                        </v-btn>
                        </v-card-actions>
                    </v-card>
                    </v-dialog>
                </v-toolbar>
                </template>

                <template v-slot:item.ontime="{ item }">
                <v-chip
                    :color="item.ontime ? 'green' : 'red'"
                    dark
                >
                    {{ item.ontime ? '是' : '否' }}
                </v-chip>
                </template>

                <template v-slot:item.actions="{ item }">
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                            <v-icon
                                small
                                v-bind="attrs"
                                v-on="on"
                                class="mr-2"
                                @click="editFlight(item)"
                            >
                                mdi-pencil
                            </v-icon>
                        </template>
                        <span>修改航班信息</span>
                    </v-tooltip>
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                            <v-icon
                                small
                                v-bind="attrs"
                                v-on="on"
                                @click="deleteFlight(item)"
                            >
                                mdi-delete
                            </v-icon>
                        </template>
                        <span>删除航班</span>
                    </v-tooltip>
                </template>
            </v-data-table>
            </v-col>

            <v-dialog
                v-model="dialogEdit"
                max-width="500px"
            >
                <v-card>
                    <v-card-title>
                    <span class="headline">修改航班信息</span>
                    </v-card-title>

                    <v-card-text>
                        <v-container>
                            <v-form ref="edit" lazy-validation style="margin-top: 10px; margin-bottom: 10px;">
                                <v-text-field
                                    label="航班号"
                                    outlined
                                    v-model="editFlightInfo.flight_id"
                                    readonly
                                ></v-text-field>
                                <v-select
                                    label="航班状态"
                                    outlined
                                    v-model="editFlightInfo.current_status"
                                    :items="status"
                                    menu-props="auto"
                                ></v-select>
                                <v-text-field
                                    label="出发日期"
                                    outlined
                                    v-model="editFlightInfo.date"
                                ></v-text-field>
                                <v-text-field
                                    label="出发时间"
                                    outlined
                                    v-model="editFlightInfo.depart_time"
                                ></v-text-field>
                                <v-text-field
                                    label="到达时间"
                                    outlined
                                    v-model="editFlightInfo.arrive_time"
                                ></v-text-field>
                                <v-radio-group
                                label="是否准点"
                                v-model="editFlightInfo.ontime"
                                row
                                >
                                <v-radio
                                    label="是"
                                    :value="true"
                                ></v-radio>
                                <v-radio
                                    label="否"
                                    :value="false"
                                ></v-radio>
                                </v-radio-group>
                                    <v-text-field
                                    label="经济舱票价"
                                    outlined
                                    v-model="editFlightInfo.eprice"
                                ></v-text-field>
                                <v-text-field
                                    label="商务舱票价"
                                    outlined
                                    v-model="editFlightInfo.cprice"
                                ></v-text-field>
                            </v-form>
                        </v-container>
                    </v-card-text>

                    <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="blue darken-1"
                        text
                        @click="dialogEdit = false"
                    >
                        取消
                    </v-btn>
                    <v-btn
                        color="blue darken-1"
                        text
                        @click="submitModify"
                    >
                        修改
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

        </v-row>
    </v-app>
</template>
<script>
    import { queryFlight, queryAirport, queryCompany, addFlight, deleteFlight, modifyFlight } from "@/api/core";
    export default {
        data() {
            return {
                headers: [
                    { text: '航班号', value: 'flight_id' },
                    { text: '出发日期', value: 'date' },
                    { text: '航班状态', value: 'current_status' },
                    { text: '预计起飞时间', value: 'depart_time' },
                    { text: '预计到达时间', value: 'arrive_time' },
                    { text: '是否准点', value: 'ontime' },
                    { text: '经济舱票价', value: 'eprice' },
                    { text: '商务舱票价', value: 'cprice' },
                    { text: 'Actions', value: 'actions', sortable: false 
                }],
                flights: [],

                dialogCreate: false,
                newFlightInfo:{
                    flight_id: "",
                    current_status: "",
                    company: "",
                    airplane: "",
                    depart_time: "",
                    from: "",
                    arrive_time: "",
                    to: "",
                    left_tickets: "",

                    airline : "",
                    ontime: true,
                    date: "",
                    eprice: 0,
                    cprice: 0
                },

                dialogEdit: false,
                editFlightInfo: {
                    flight_id: "",
                    current_status: "",
                    company: "",
                    airplane: "",
                    depart_time: "",
                    from: "",
                    arrive_time: "",
                    to: "",
                    left_tickets: "",

                    airline : "",
                    ontime: true,
                    date: "",
                    eprice: 0,
                    cprice: 0
                },

                status : ["等待", "检票中","晚点","飞行中","已到达","失联"],
                companies: [],
                airports: [],

                errorDialog: false,
                errorMsg: {
                    title: "",
                    content: ""
                },

                snackbar: false,
                snackbarMsg: "",

            }
        },

        mounted(){
            queryFlight().then(res=>{
                this.flights = res.data.flights

            }).catch(err=>{
                // console.log(err)
                this.errorMsg.title = "获取航班信息失败"
                this.errorMsg.content = err.response.data.error_msg
                this.errorDialog = true
            })

            queryCompany().then(res=>{
                // console.log(res)
                var cpnData = res.data.companies
                cpnData.map((value) => {
                    this.companies.push(value.acro_name)
                })
                // console.log(this.cities)

            }).catch(err=>{
                // console.log(err)
                this.errorMsg.title = "获取航空公司失败"
                this.errorMsg.content = err.response.data.error_msg
                this.errorDialog = true
            })

            queryAirport().then(res=>{
                // console.log(res)
                var Data = res.data.airports
                Data.map((value) => {
                    this.airports.push(value.airport_name)
                })
                // console.log(this.cities)

            }).catch(err=>{
                // console.log(err)
                this.errorMsg.title = "获取机场信息失败"
                this.errorMsg.content = err.response.data.error_msg
                this.errorDialog = true
            })
        },

        methods: {
            updateTable(){
                queryFlight().then(res=>{
                    this.flights = res.data.flights

                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "获取航班信息失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true
                })
            },

            createNewFlight(){
                this.newFlightInfo.eprice = Number(this.newFlightInfo.eprice)
                this.newFlightInfo.cprice = Number(this.newFlightInfo.cprice)
                // console.log(this.newFlightInfo)
                // eslint-disable-next-line no-unused-vars
                addFlight(this.newFlightInfo).then(res=>{
                    // console.log(res)
                    this.updateTable()
                    this.snackbar = true
                    this.snackbarMsg = "创建航班成功"
                    this.dialogCreate  = false
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "创建航班失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true
                })
            },

            deleteFlight(flight){
                // eslint-disable-next-line no-unused-vars
                deleteFlight(flight.flight_id).then(res=>{
                    // console.log(res)
                    this.updateTable()
                    this.snackbar = true
                    this.snackbarMsg = "删除航班成功"
                    this.dialogCreate  = false
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "删除航班失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true
                })
            },

            editFlight(flight){
                // console.log(flight)
                this.editFlightInfo = flight
                this.dialogEdit = true
            },

            submitModify(){
                var modifyInfo = {
                    current_status: this.editFlightInfo.current_status,
                    depart_time: this.editFlightInfo.depart_time,
                    arrive_time: this.editFlightInfo.arrive_time,
                    cprice: this.editFlightInfo.cprice,
                    eprice: this.editFlightInfo.eprice,
                    ontime: this.editFlightInfo.ontime
                }
                // eslint-disable-next-line no-unused-vars
                modifyFlight(this.editFlightInfo.flight_id, modifyInfo).then(res=>{
                    // console.log(res)
                    this.updateTable()
                    this.snackbar = true
                    this.snackbarMsg = "修改航班信息成功"
                    this.dialogEdit = false
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "修改航班信息失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.dialogEdit =  true
                })
            }
        }
    }

</script>
<style>

</style>