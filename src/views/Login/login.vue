<template>
    <v-app id="user">
        <div class="login">
            <div class="login-con">
                <v-card>
                    <v-card-title>
                        登录
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text>
                        <v-form style="margin-top: 10px; margin-bottom: 10px;">
                            <v-text-field
                                label="账号/手机号"
                                outlined
                                prepend-icon="mdi-account-box"
                                v-model="userInfo.username"
                            ></v-text-field>
                            <v-text-field
                                label="密码"
                                outlined
                                prepend-icon="mdi-lock"
                                v-model="userInfo.password"
                                :append-icon="showpw ? 'mdi-eye' : 'mdi-eye-off'"
                                :type="showpw ? 'text' : 'password'"
                                @click:append="showpw  = !showpw"
                            ></v-text-field>
                            <v-btn
                                outlined
                                class="ma-2"
                                large
                                right
                                @click="submitLogin"
                            >
                                登录
                            </v-btn>
                            <v-btn
                                outlined
                                class="ma-2"
                                large
                                right
                                @click="gotoRegister"
                            >
                                注册
                            </v-btn>
                        </v-form>
                    </v-card-text>
                </v-card>
            </div>

            <v-dialog
                v-model="loginFail"
                max-width="290"
            >
                <v-card>
                    <v-card-title class="headline">
                        登录失败
                    </v-card-title>
                    <v-card-text>{{errormsg}}</v-card-text>
                    <v-card-actions>
                    <v-spacer></v-spacer>
                        <v-btn
                            color="red darken-2"
                            text
                            @click="loginFail = false"
                        >
                            Close
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </div>
    </v-app>
</template>
<script>
    import { login } from "@/api/login";
    import { setToken } from "@/api/core";
    export default {
        data() {
            return {
                userInfo:{
                    username: "",
                    password: ""
                },

                loginFail: false,
                errormsg: "cuowu",

                showpw:false
            }
        },


        methods: {
            submitLogin(){
                // console.log(this.userInfo)
                login(this.userInfo).then(res=>{
                    // console.log(res)
                    this.$cookie.set('access-token', res.data.access_token, {expires: 7})
                    // console.log(this.$cookie.get('access-token'))
                    setToken();
                    this.$router.push({
                        path: '/',
                    })
                }).catch(err=>{
                    // console.log(err.response.data.error_msg)
                    this.errormsg = err.response.data.error_msg
                    this.loginFail = true
                })
            },

            gotoRegister(){
                this.$router.push({
                    path: '/register',
                })
            },
        }
    }

</script>

<style>
.login{
    width: 100%;
    height: 100%;
    background-image: url('../../assets/plane.jpg');
    background-size: cover;
    background-position: center;
    position: relative;
}

.login-con{
    position: absolute;
    right: 160px;
    top: 50%;
    transform: translateY(-60%);
    width: 320px;
}
</style>