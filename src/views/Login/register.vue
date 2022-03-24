<template>
    <v-app id="user">
        <v-content class="register">
                <v-container>
                    <v-row justify='center'>
                        <v-col :cols="6">
                            <v-card>
                                <v-card-title>
                                    注册
                                </v-card-title>
                                <v-divider></v-divider>
                                <v-card-text>
                                    <v-form ref="form" lazy-validation style="margin-top: 10px; margin-bottom: 10px;">
                                        <v-text-field
                                            label="身份证号"
                                            outlined
                                            :counter="18"
                                            v-model="userInfo.id"
                                            :rules="userIdRules"
                                        ></v-text-field>
                                        <v-text-field
                                            label="手机号"
                                            outlined
                                            v-model="userInfo.phone"
                                            :rules="[v => !!v || '请输入手机号']"
                                            required
                                        ></v-text-field>
                                        <v-text-field
                                            label="密码"
                                            outlined
                                            v-model="userInfo.password"
                                            :rules="[v => !!v || '请输入密码']"
                                            required
                                            :append-icon="showpw1 ? 'mdi-eye' : 'mdi-eye-off'"
                                            :type="showpw1 ? 'text' : 'password'"
                                            @click:append="showpw1  = !showpw1"
                                        ></v-text-field>
                                        <v-text-field
                                            label="确认密码"
                                            outlined
                                            v-model="confirmPW"
                                            :rules="pwVerify"
                                            :append-icon="showpw2 ? 'mdi-eye' : 'mdi-eye-off'"
                                            :type="showpw2 ? 'text' : 'password'"
                                            @click:append="showpw2  = !showpw2"
                                        ></v-text-field>
                                        <v-text-field
                                            label="姓名"
                                            outlined
                                            v-model="userInfo.name"
                                            :rules="[v => !!v || '请填写姓名']"
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
                                                outlined
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
                                            label="常住地"
                                            outlined
                                            v-model="userInfo.upor"
                                            :rules="[v => !!v || '请填写常住地']"
                                        ></v-text-field>
                                        <v-btn
                                            outlined
                                            class="ma-2"
                                            large
                                            right
                                            @click="submitRegister"
                                        >
                                            注册
                                        </v-btn>
                                    </v-form>
                                </v-card-text>
                            </v-card>
                        </v-col>
                    </v-row>

                    <v-snackbar
                        v-model="validFail"
                        color="error"
                        text
                    >
                        {{ validErrormsg }}

                            <v-btn
                                text
                                dark
                                @click="validFail = false"
                            >
                                Close
                            </v-btn>
                    </v-snackbar>

                    <v-dialog
                        v-model="registerFail"
                        max-width="290"
                    >
                        <v-card>
                            <v-card-title class="headline">
                                注册失败
                            </v-card-title>
                            <v-card-text>{{errormsg}}</v-card-text>
                            <v-card-actions>
                            <v-spacer></v-spacer>
                                <v-btn
                                    color="red darken-2"
                                    text
                                    @click="registerFail = false"
                                >
                                    Close
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
            
            </v-container>
        </v-content>
    </v-app>
</template>
<script>
    import { register } from "@/api/login";
    export default {
        data() {
            return {
                datePiker:false,
                confirmPW: "",

                showpw1: false,
                showpw2: false,

                validFail: false,
                validErrormsg: "",

                registerFail: false,
                errormsg: "",

                userInfo:{
                    id: "",
                    phone: "",
                    password: "",
                    name: "",
                    sex: "男",
                    birth: new Date().toISOString().substr(0, 10),
                    upor: ""
                },
                userIdRules: [
                    v => !!v || '请填写身份证号',
                ],
                pwVerify: [
                    v => !!v || '请再次输入密码',
                ]
                
            }
        },


        methods: {
            submitRegister(){
                // console.log(this.userInfo)
                var valid = this.$refs.form.validate()
                if(valid){
                    if (this.confirmPW == this.userInfo.password){
                        // eslint-disable-next-line no-unused-vars
                        register(this.userInfo).then(res=>{
                            // console.log(res)
                            this.$router.push({
                                path: '/login',
                            })
                        }).catch(err=>{
                            // console.log(err)
                            this.errormsg = err.response.data.error_msg
                            this.registerFail = true
                        })
                    }else{
                        this.validErrormsg = "两次输入密码不匹配"
                        this.validFail = true
                        // console.log(validErrormsg)
                    }
                }else{
                    this.validErrormsg = "请将个人信息填写完整"
                    this.validFail = true
                    // console.log(validErrormsg)
                }
            }
        }
    }

</script>

<style>
.register{
    width: 100%;
    height: 100%;
    background-image: url('../../assets/plane.jpg');
    background-size: cover;
    background-position: center;
    position: relative;
}
</style>