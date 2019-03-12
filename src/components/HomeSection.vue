<template>
  <div class="hello">
    <h1>{{ msg }}</h1> 
<h3>Plant-Soil-Buddy is a web application that will gather the soil’s quality data.</h3>
<h4>And we have this system tells us what kinds of plants are suitable for the specific soil we are using.</h4>
<h4>As we could use this before we decide to invest in gardening.</h4>
<h4>This website requires <a class="item">Arduino Sensor Devices</a> to run the soil quality data records.</h4>
<br>
      <button class="normal-btn login-btn" v-on:click="toLogin">Login</button>

    <br>
    <button class="normal-btn" v-on:click="toRegis">Register</button>

    <br>
    <button class="normal-btn" v-on:click="toAdmin">Administrator</button>

    
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
    toAdmin() {
      router.push("/admindata")
    }

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
  margin-bottom: 30px;
}
.login-btn {
  font-size: 18px;
  height: 55px;
}
input, .normal-btn {
  width: 200px;
}
.item {
  color: blue;
}
</style>
