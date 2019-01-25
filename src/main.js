import Vue from 'vue'
import App from '@/App.vue'

//import store from '@/store' 
import router from '@/router'

import axios from 'axios'
import VueAxios from 'vue-axios'
import jwt_decode from 'jwt-decode'
import Vuex from 'vuex'
import VueTemperatureFilter from 'vue-temperature-filter'

Vue.use(Vuex);
Vue.use(VueAxios, axios);
Vue.use(VueTemperatureFilter, {
  showText: true
})

Vue.config.productionTip = false

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

// Vue.use(VueRouter)

const store = new Vuex.Store({
  state: {
    authUser: {},
    isAuthenticated: false,
    jwt: localStorage.getItem('token'),
    endpoints: {
      obtainJWT: 'http://127.0.0.1:8000/auth/obtain_token/',
      refreshJWT: 'http://127.0.0.1:8000/auth/refresh_token/',
      baseUrl: 'http://127.0.0.1:8000/'
    }
  },
  mutations: {
  	setAuthUser(state, {
      authUser,
      isAuthenticated
    }) {
      Vue.set(state, 'authUser', authUser)
      Vue.set(state, 'isAuthenticated', isAuthenticated)
    },
    updateToken(state, newToken){
      localStorage.setItem('token', newToken);
      state.jwt = newToken;
    },
    removeToken(state){
      localStorage.removeItem('token');
      state.jwt = null;
    }
  },
   actions:{
    obtainToken(username, password) {
      const payload = {
        username: username,
        password: password
      }
      axios.post(this.state.endpoints.obtainJWT, payload)
        .then((response)=>{
            this.commit('updateToken', response.data.token);
          })
        .catch((error)=>{
            console.log(error);
          })
    },
    refreshToken() {
      const payload = {
        token: this.state.jwt
      }
      axios.post(this.state.endpoints.refreshJWT, payload)
        .then((response)=>{
            this.commit('updateToken', response.data.token)
          })
        .catch((error)=>{
            console.log(error)
          })
    },
	 inspectToken(){
      const token = this.state.jwt;
      if(token){
        const decoded = jwt_decode(token);
        const exp = decoded.exp
        const orig_iat = decode.orig_iat
        if(exp - (Date.now()/1000) < 1800 && (Date.now()/1000) - orig_iat < 628200){
          this.dispatch('refreshToken')
        } else if (exp -(Date.now()/1000) < 1800){
          // DO NOTHING, DO NOT REFRESH          
        } else {
          // PROMPT USER TO RE-LOGIN, THIS ELSE CLAUSE COVERS THE CONDITION WHERE A TOKEN IS EXPIRED AS WELL
        }
      }
    }
  	}
  })

const vue = new Vue({
  router,
  store,
  render: h => h(App)
})

vue.$mount('#app')
