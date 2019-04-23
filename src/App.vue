<template>
  <div id="app">
    <img id="logo" src='@/assets/logo-plant-soil-buddy.png'>

    <vue-headful title="Plant Soil Buddy - Plant and Soil Recommender via Arduino Sensors"/>

    <router-view></router-view>
    <notifications group="notify" position="bottom center" />
    
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'
import AuthService from './auth/AuthService'

const API_URL = 'http://localhost:8000'
const auth = new AuthService()
export default {
  name: 'app',
  data () {
    this.handleAuthentication()
    this.authenticated = false

    auth.authNotifier.on('authChange', authState => {
      this.authenticated = authState.authenticated
    })

    return {
      authenticated: false,
      message: ''
    }
  },
  methods: {
    // this method calls the AuthService login() method
    login () {
      auth.login()
    },
    handleAuthentication () {
      auth.handleAuthentication()
    },
    logout () {
      auth.logout()
    },
    privateMessage () {
      const url = `${API_URL}/private`
      return axios.get(url, {headers: {Authorization: `Bearer ${AuthService.getAuthToken()}`}}).then((response) => {
        console.log(response.data)
        this.message = response.data || ''
      })
    }
  }

}
</script>

<style>
#title {
  font-size: 100px;
}
#logo {
  max-width: 100%
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
