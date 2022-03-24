<template>
    <v-app id="user-info">
        <v-row justify='center'> 
            <v-col cols="8">
                <v-form ref="form" style="margin-top: 40px; margin-bottom: 40px; margin-left:5%; width: 90%;">
                    <v-text-field
                        label="身份证号"
                        v-model="userInfo.id"
                        :append-icon="showid ? 'mdi-eye' : 'mdi-eye-off'"
                            :type="showid ? 'text' : 'password'"
                            @click:append="showid  = !showid"
                    ></v-text-field>
                    <v-text-field
                        label="手机号"
                        v-model="userInfo.phone"
                        readonly
                    ></v-text-field>
                    <v-menu
                        ref="menu"
                        v-model="datePiker"
                        :close-on-content-click="false"
                        :return-value.sync="userInfo.birth"
                        transition="scale-transition"
                        offset-y
                        min-width="290px"
                    >
                        <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                            v-model="userInfo.birth"
                            label="出生日期"
                            prepend-icon="mdi-calendar"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                        ></v-text-field>
                        </template>
                        <v-date-picker
                        v-model="userInfo.birth"
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
                            @click="$refs.menu.save(userInfo.birth)"
                        >
                            OK
                        </v-btn>
                        </v-date-picker>
                    </v-menu>
                    <v-text-field
                        label="姓名"
                        v-model="userInfo.name"
                    ></v-text-field>
                    <v-radio-group
                    v-model="userInfo.sex"
                    row
                    >
                    <v-radio
                        label="男"
                        value="男"
                    ></v-radio>
                    <v-radio
                        label="女"
                        value="女"
                    ></v-radio>
                    </v-radio-group>
                    <v-text-field
                        label="常住地"
                        v-model="userInfo.upor"
                    ></v-text-field>
                    <v-btn
                    outlined
                    class="ma-2"
                    large
                    right
                    @click="modifyUser"
                    >
                        修改信息
                    </v-btn>
                    <v-btn
                    outlined
                    class="ma-2"
                    large
                    right
                    @click="updateUserInfo"
                    >
                        取消修改
                    </v-btn>
                </v-form>
            </v-col>
        </v-row>

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
    import { getMyInfo, modifyUser } from '@/api/core'
    export default {
        data() {
            return {
                userInfo: {
                    id: "",
                    sex: "",
                    birth: "",
                    upor: "",
                    name: "",
                    phone: "",
                    password: ""
                },

                showid: false,

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
            getMyInfo().then(res=>{
                // console.log(res)
                this.userInfo = res.data
                this.defaultUserInfo = res.data
            }).catch(err=>{
                // console.log(err)
                this.errorMsg.title = "获取用户信息失败"
                this.errorMsg.content = err.response.data.error_msg
                this.errorDialog = true
            })
        },

        methods: {
            modifyUser(){
                var modifyUserInfo = {
                    id: this.userInfo.id,
                    sex: this.userInfo.sex,
                    birth: this.userInfo.birth,
                    upor: this.userInfo.upor,
                    name: this.userInfo.name,
                    phone: null,
                    password: null
                }
                // eslint-disable-next-line no-unused-vars
                modifyUser(this.userInfo.phone, modifyUserInfo).then(res=>{
                    // console.log(res)
                    this.snackbar = true
                    this.snackbarMsg = "修改信息成功"
                    this.updateUserInfo()
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "获取用户信息失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true
                })
            },

            updateUserInfo(){
                getMyInfo().then(res=>{
                    // console.log(res)
                    this.userInfo = res.data
                    this.defaultUserInfo = res.data
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "获取用户信息失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true
                })
            }
        }
    }

</script>
<style>

</style>