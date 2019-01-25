import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeSection from '@/components/HomeSection'
import LoginForm from '@/components/LoginForm'
import RegisForm from '@/components/RegisForm'
import MainSection from '@/components/MainSection'

Vue.use(VueRouter)

export default new VueRouter({
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeSection
    },
    {
      path: '/login',
      component: LoginForm
    },
    {
      path: '/regis',
      component: RegisForm
    },
    {
      path: '/main',
      component: MainSection
    }
  ]
})
