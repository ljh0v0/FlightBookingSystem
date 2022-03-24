<template>
  <v-app id="manager">
    <v-app-bar 
        app
    >
        <v-app-bar-nav-icon></v-app-bar-nav-icon>
        <v-toolbar-title>Manager</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn
            icon
            @click="backHome"
        >
            <v-icon>
                mdi-home
            </v-icon>
        </v-btn>
    </v-app-bar>

    <v-navigation-drawer
        permanent
        dark
        color="#2B3648"
        app
    >
    <v-list-item>
        <v-list-item-content>
            <v-list-item-title class="title">
                管理端
            </v-list-item-title>
            <v-list-item-subtitle>
                一心向航
            </v-list-item-subtitle>
            </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list
            nav
        >
            <v-list-item
                v-for="item in menus"
                :key="item.title"
                link
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
    </v-navigation-drawer>

    <v-content class="grey lighten-2" app>
        <v-container>
            <v-row>
                <v-col>
                    <v-card
                        min-height="70vh"
                    >
                        <router-view></router-view>
                    </v-card>
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
                        { title: '用户管理', icon: 'mdi-account-box-multiple' },
                        { title: '航班管理', icon: 'mdi-airplane' },
                ],
            }
        },

        methods: {
            backHome(){
                this.$router.push({
                    path: '/',
                })
            },

            changeMenu(title){
                if(title == '用户管理'){
                    this.$router.push({
                        path: '/manager/users_table',
                    })
                }else if (title == '航班管理'){
                    this.$router.push({
                        path: '/manager/flights_table',
                    })
                }
            },
        }
    }

</script>
<style>

</style>