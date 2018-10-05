import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import Router from 'vue-router'
import Home from '@/components/Home'

require('firebase')

Vue.use(Router)
Vue.use(BootstrapVue)

export default new Router({
  routes: [{
    path: '/home',
    name: 'Home',
    component: Home
  }]
})
