<template>
    <v-app id="user">
            <v-app-bar
            app
            color="#2B3648"
            dark
            >
                <v-container class="py-0 fill-height">
                    <v-toolbar-title>用户中心</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn
                        icon
                        @click="backHome"
                    >
                        <v-icon>
                            mdi-home
                        </v-icon>
                    </v-btn>
                </v-container>
            </v-app-bar>

            <v-content class="grey lighten-2">
                <v-container>
                    <v-row>
                        <v-col cols="2">
                        <v-sheet rounded="lg">
                            <v-list color="transparent">
                                <v-list-item
                                v-for="item in menus"
                                :key="item.title"
                                @click="changeMenu(item.title)"
                                >
                                <v-list-item-icon>
                                    <v-icon>{{ item.icon }}</v-icon>
                                </v-list-item-icon>

                                <v-list-item-content>
                                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                                </v-list-item-content>
                                </v-list-item>
                            </v-list>
                        </v-sheet>
                        </v-col>

                        <v-col>
                            <v-sheet
                            min-height="70vh"
                            rounded="lg"
                            >
                                <router-view></router-view>
                            </v-sheet>
                        </v-col>
                    </v-row>
                </v-container>
            </v-content>
        
    </v-app>
</template>
<script>
    export default {
        data() {
            return {
                menus: [
                        { title: '个人信息', icon: 'mdi-account-details' },
                        { title: '行程记录', icon: 'mdi-calendar-text' },
                ],
            }
        },

        computed: {
        },

        methods: {
            changeMenu(title){
                if(title == '个人信息'){
                    this.$router.push({
                        path: '/user/user_info',
                    })
                }else if(title == '行程记录'){
                    this.$router.push({
                        path: '/user/trip_record',
                    })
                }
            },

            backHome(){
                this.$router.push({
                    path: '/',
                })
            }
        }
    }

</script>
<style>

</style>