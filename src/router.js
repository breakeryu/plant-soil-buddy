import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeSection from '@/components/HomeSection'
import LoginForm from '@/components/LoginForm'
import RegisForm from '@/components/RegisForm'
import MainSection from '@/components/MainSection'
import AddSoilProfile from '@/components/SoilProfile/AddSoilProfile'
import EditSoilProfile from '@/components/SoilProfile/EditSoilProfile'
import ClearSoilProfile from '@/components/SoilProfile/ClearSoilProfile'
import DeleteSoilProfile from '@/components/SoilProfile/DeleteSoilProfile'
import PlantInfo from '@/components/PlantInfo'
import AdminDatabase from '@/components/AdminDatabase'
import PasswordChangeForm from '@/components/PasswordChangeForm'
import ScatterProof from '@/components/Charts/ScatterProof'

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
    },
    {
      path: '/addsoil',
      component: AddSoilProfile
    },
    {
      path: '/editsoil',
      component: EditSoilProfile
    },
    {
      path: '/clearsoil',
      component: ClearSoilProfile
    },
    {
      path: '/deletesoil',
      component: DeleteSoilProfile
    },
    {
      path: '/plantinfo',
      component: PlantInfo
    },
    {
      path: '/admindata',
      component: AdminDatabase
    },
    {
      path: '/changepwd',
      component: PasswordChangeForm
    },
    {
      path: '/scatterchart',
      component: ScatterProof
    }
  ]
})
