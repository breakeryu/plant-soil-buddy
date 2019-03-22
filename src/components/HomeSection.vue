<template>
  <div class="hello">
    <h1>{{ msg }}</h1> 
<h3><a class="item">Plant-Soil-Buddy</a> is a web app that <a class="item"><u>tells us what kinds of plants and nutrients are suitable for the specific soil</u></a> we are using.</h3>
<h3>For this web can tell the plants and nutrients, it requires the <a class="item">Arduino Sensor Monitor Program</a> to run the soil quality data recording.</h3>
<h3>We can use this before we <u>decide to invest in gardening in resourceful long-term</u>.</h3>

<br>
      <button class="normal-btn login-btn" v-on:click="toLogin">Login</button>

    <br>
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
