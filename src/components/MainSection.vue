<template>
  <div class="hello">
    <h1>{{ msg }} {{ username }}!</h1>  
    <h3> Device Status: {{ status_msg }}</h3>
    <p>
    <button class="normal-btn normal-btn">Start</button>  
    <button class="normal-btn normal-btn exit-btn">Stop</button>
  </p>
    <h4> Make sure the sensors are all attached to the soil before clicking "Start" for the best accuracy. </h4>
	<moist-chart></moist-chart>
  <acidity-chart></acidity-chart>
  <fertility-chart></fertility-chart>
    <button class="normal-btn exit-btn" v-on:click="doLogout">Logout</button>
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'
import MoistChart from '@/components/Charts/MoistChart'
import AcidityChart from '@/components/Charts/AcidityChart'
import FertilityChart from '@/components/Charts/FertilityChart'

export default {
  name: 'Welcome',
  components: {
    MoistChart,
    AcidityChart,
    FertilityChart
  },
  data () {
    return {
      username: '',
      status_msg: 'Disconnected',
      msg: 'Welcome,'
    }
  },
  methods: {
    doLogout() {
    	this.$store.commit('updateToken', '')
    	this.$store.commit("setAuthUser",
                {authUser: '', isAuthenticated: false}
              )
    	router.push('/')
    }
  },
  mounted(){
    this.username = this.$store.state.authUser

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
.exit-btn {
	background-color: red;
}
input, .normal-btn {
  width: 200px;
}
</style>
