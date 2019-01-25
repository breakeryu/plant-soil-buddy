<template>
  <div class="hello">
    <h1>{{ msg }}</h1>  
<br><br><br>
      <button class="normal-btn" v-on:click="toLogin">Login</button>

    <br><br>
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
      msg: 'Welcome, Login to continue!'
    }
  },
  methods: {
    toLogin () {
      router.push("/login")
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
}
input, .normal-btn {
  width: 200px;
}
</style>
