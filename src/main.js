import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
import VueAwesomeSwiper from 'vue-awesome-swiper'
import 'swiper/dist/css/swiper.css'
import './assets/ttf/index.less'
import cookie from 'vue-cookie'
import { VueJsonp } from 'vue-jsonp'

const echarts = require('echarts/lib/echarts')
require('echarts/lib/chart/bar')
require('echarts/lib/chart/line');
require('echarts/lib/chart/bar');
require('echarts/lib/chart/radar')
require('echarts/lib/component/tooltip')
require('echarts/lib/component/title')
require('echarts/lib/component/legend')
require('echarts/lib/component/legendScroll')
Vue.prototype.$echarts = echarts

Vue.use(VueJsonp)

Vue.use(VueAwesomeSwiper)
Vue.use(mavonEditor)
Vue.config.productionTip = false

Vue.prototype.$cookie = cookie;

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
