<template>
    <v-app id="user-info">
        <v-row justify='center'> 
            <v-col>
              <v-data-table
                :headers="headers"
                :items="users"
                min-height="70vh"
            >
                <template v-slot:top>
                <v-toolbar
                    flat
                >
                    <v-toolbar-title>用户信息</v-toolbar-title>
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
                            创建新用户
                        </v-btn>
                    </template>
                    <v-card>
                        <v-card-title>
                        <span class="headline">创建用户</span>
                        </v-card-title>

                        <v-card-text>
                            <v-container>
                                <v-form ref="form" lazy-validation style="margin-top: 10px; margin-bottom: 10px;">
                                    <v-text-field
                                        label="身份证号"
                                        outlined
                                        :counter="18"
                                        v-model="newUserInfo.id"
                                        :rules="[v => !!v || '请输入身份证号']"
                                    ></v-text-field>
                                    <v-text-field
                                        label="手机号"
                                        outlined
                                        v-model="newUserInfo.phone"
                                        :rules="[v => !!v || '请输入手机号']"
                                        required
                                    ></v-text-field>
                                    <v-text-field
                                        label="密码"
                                        outlined
                                        v-model="newUserInfo.password"
                                        :rules="[v => !!v || '请输入密码']"
                                        required
                                    ></v-text-field>
                                    <v-text-field
                                        label="姓名"
                                        outlined
                                        v-model="newUserInfo.name"
                                        :rules="[v => !!v || '请填写姓名']"
                                    ></v-text-field>
                                    <v-radio-group
                                    v-model="newUserInfo.sex"
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
                                    <v-menu
                                        ref="menu"
                                        v-model="datePiker"
                                        :close-on-content-click="false"
                                        :return-value.sync="newUserInfo.birth"
                                        transition="scale-transition"
                                        offset-y
                                        min-width="290px"
                                    >
                                        <template v-slot:activator="{ on, attrs }">
                                        <v-text-field
                                            v-model="newUserInfo.birth"
                                            label="出生日期"
                                            prepend-icon="mdi-calendar"
                                            readonly
                                            outlined
                                            v-bind="attrs"
                                            v-on="on"
                                        ></v-text-field>
                                        </template>
                                        <v-date-picker
                                        v-model="newUserInfo.birth"
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
                                            @click="$refs.menu.save(newUserInfo.birth)"
                                        >
                                            OK
                                        </v-btn>
                                        </v-date-picker>
                                    </v-menu>
                                    <v-text-field
                                        label="常住地"
                                        outlined
                                        v-model="newUserInfo.upor"
                                        :rules="[v => !!v || '请填写常住地']"
                                    ></v-text-field>
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
                            @click="createNewUser"
                        >
                            创建
                        </v-btn>
                        </v-card-actions>
                    </v-card>
                    </v-dialog>
                </v-toolbar>
                </template>
                <template v-slot:item.actions="{ item }">
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-icon
                            small
                            class="mr-2"
                            v-bind="attrs"
                            v-on="on"
                            @click="addManager(item)"
                        >
                            mdi-account-star
                        </v-icon>
                    </template>
                    <span>添加管理员权限</span>
                </v-tooltip>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                        <v-icon
                            small
                            v-bind="attrs"
                            v-on="on"
                            @click="deleteUser(item)"
                        >
                            mdi-delete
                        </v-icon>
                    </template>
                    <span>删除用户</span>
                </v-tooltip>
                </template>
            </v-data-table>
            </v-col>

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
    import { getUsers, deleteUser, addManager } from "@/api/core";
    import { register } from "@/api/login";
    export default {
        data() {
            return {
                headers: [
                    { text: '姓名', value: 'name' },
                    { text: '手机号', value: 'phone' },
                    { text: '身份证号', value: 'id' },
                    { text: '性别', value: 'sex' },
                    { text: '生日', value: 'birth' },
                    { text: '常住地', value: 'upor' },
                    { text: 'Actions', value: 'actions', sortable: false 
                }],
                users: [],

                dialogCreate: false,
                datePiker:false,
                newUserInfo:{
                    id: "",
                    phone: "",
                    password: "",
                    name: "",
                    sex: "男",
                    birth: new Date().toISOString().substr(0, 10),
                    upor: ""
                },

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
            getUsers().then(res=>{
                this.users = res.data.userInfo

            }).catch(err=>{
                // console.log(err)
                this.errorMsg.title = "获取用户信息失败"
                this.errorMsg.content = err.response.data.error_msg
                this.errorDialog = true
            })
        },

        methods: {
            updateTable(){
                getUsers().then(res=>{
                    this.users = res.data.userInfo

                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "获取用户信息失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true
                })
            },

            createNewUser(){
                // eslint-disable-next-line no-unused-vars
                register(this.newUserInfo).then(res=>{
                    // console.log(res)
                    this.updateTable()
                    this.snackbar = true
                    this.snackbarMsg = "创建用户成功"
                    this.dialogCreate  = false
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "创建用户失败"
                    this.errorMsg.content = err.response.data.error_msg
                    this.errorDialog = true
                })
            },

            addManager(user){
                addManager({
                    "phone": user.phone
                // eslint-disable-next-line no-unused-vars
                }).then(res=>{
                    // console.log(res)
                    this.snackbar = true
                    this.snackbarMsg = "添加管理员权限成功"
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "添加管理员权限失败"
                    this.errorMsg.content = err.response.data.error_msg
                })
            },

            deleteUser(user){
                // console.log(user.phone)
                // eslint-disable-next-line no-unused-vars
                deleteUser(user.phone).then(res=>{
                    // console.log(res)
                    this.updateTable()
                    this.snackbar = true
                    this.snackbarMsg = "删除用户成功"
                }).catch(err=>{
                    // console.log(err)
                    this.errorMsg.title = "删除用户失败"
                    this.errorMsg.content = err.response.data.error_msg
                })
            }
        }
    }

</script>
<style>

</style>