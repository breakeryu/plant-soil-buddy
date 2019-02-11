<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <h3 class="warning" v-if="failed">{{ failed_msg }}</h3>
    <form class="form-signin" v-on:submit.prevent="doLogin">
      <h3>Username</h3>
      <input v-model="username" type="text" name="username"><br>
      <h3>Password</h3>
      <input v-model="password" type="password" name="password"><br><br>
      <button class="normal-btn submit-btn" type="submit">Login</button>
    </form>
    <button class="normal-btn" v-on:click="toRegis">Register</button>
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'

export default {
  data () {
    return {
      username: '',
      password: '',
      msg: 'Login',
      failed: false,
      failed_msg: ''
    }
  },
  methods: {
    doLogin () {
      //alert(this.username)
      //alert(this.password)
      var self = this

      const input = {
        'username': this.username,
        'password' : this.password
      }
      //alert(input['name']);
      //alert(input['password']);

      axios.post(this.$store.state.endpoints.obtainJWT, input).then((response) =>{
        //console.log(req.data)
           this.$store.commit('updateToken', response.data.token)
           /*
        if (req.data != 'None'){
          alert('Welcome!')
          router.push("/messages")
        } else {
          alert('Login Failed')
          console.log('Login Failed')
          router.push("/login")
        }
        return req*/
          const base = {
            baseURL: this.$store.state.endpoints.baseUrl,
            headers: {
            // Set your Authorization to 'JWT', not Bearer!!!
              Authorization: `JWT ${this.$store.state.jwt}`,
              'Content-Type': 'application/json'
            },
            xhrFields: {
                withCredentials: true
            }
          }

          const axiosInstance = axios.create(base)
          /*axiosInstance({
            url: "/user",
            method: "get",
            params: {}
          })*/
          axios.post("/user", {
            'username': this.username
          })
            .then((response) => {
              this.$store.commit("setAuthUser",
                {authUser: response.data, isAuthenticated: true}
              )
              router.push('main')
            })

        })
        .catch((error) => {
          if (error.response.status >= 400 && error.response.status < 500) {
            this.failed = true
            this.failed_msg = 'Invalid Username or Password'
          } else {
            this.failed = true
            this.failed_msg = 'Internal Server Error'
          }
        })

      
    },
    toRegis () {
      router.push("/regis")
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  color: #42b983;
}
input {
  height: 25px;
  border: 3px solid #555;
}
input:focus {
  background-color: lightblue;
}
.normal-btn {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  padding: 5px 12px;
  text-align: center;
  text-decoration: none;
  font-size: 16px;
  height: 35px;
  margin-left: 10px;
  margin-right: 10px;
  margin-bottom: 30px;
}
.submit-btn {
  background-color: blue;
  font-size: 18px;
  height: 55px;
}
.warning {
  color: red;
}
input, .normal-btn {
  width: 200px;
}
</style>
