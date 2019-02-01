<template>
  <div class="hello">
    <h1>{{ msg }} {{ username }}!</h1>  
    <h3> Device Status: {{ status_msg }}</h3>
    <p>
    <button id="trig-btn" class="normal-btn normal-btn" v-on:click="triggerSensor">{{ btn_text }}</button>  
  </p>
    <h4> {{ btn_note }} </h4><br><br>
    <plant-recommender ref="plant_rec"></plant-recommender>
    <br><br>
	<moist-chart ref="moist_ch"></moist-chart>
  <acidity-chart ref="acidity_ch"></acidity-chart>
  <fertility-chart ref="fertility_ch"></fertility-chart>
  
  <br><br>
    <button class="normal-btn exit-btn" v-on:click="doLogout">Logout</button><br>
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'
import MoistChart from '@/components/Charts/MoistChart'
import AcidityChart from '@/components/Charts/AcidityChart'
import FertilityChart from '@/components/Charts/FertilityChart'
import PlantRecommender from '@/components/PlantRecommender'

export default {
  name: 'Welcome',
  components: {
    MoistChart,
    AcidityChart,
    FertilityChart,
    PlantRecommender
  },
  data () {
    return {
      username: '',
      status_msg: 'Connected',
      msg: 'Welcome,',
      btn_note: 'Make sure the sensors are all attached to the soil before clicking "Start" for the best accuracy of plant recommendation.',
      timer_running: false,
      timer: null,
      time: 5,
      btn_text: "Start"
    }
  },
  methods: {
    snapReset() {
      axios.get("/snap_reset")
            .then((response) => {
              this.current_data = response.data
            })
    },
    readFromSensors() {
      this.$refs.moist_ch.getData()
      this.$refs.acidity_ch.getData()
      this.$refs.fertility_ch.getData()
    },
    startSensor() {
      this.snapReset()
      this.btn_text = "Stop"
      this.timer_running = true
      this.readFromSensors()
      if (!this.timer) {
          this.timer = setInterval( () => {
            if (this.time > 0) {
               this.time--
            } else {
               this.time = 5
               this.readFromSensors()
            }
          }, 1000 )
       }
    },
    stopSensor() {
      this.btn_text = "Start"
      this.timer_running = false
      this.time = 5
      clearInterval(this.timer)
      this.timer = null
    },
    triggerSensor() {
      if (this.timer_running) {
        this.$refs.plant_rec.getData()
        this.stopSensor()
        this.btn_note = 'Make sure the sensors are all attached to the soil before clicking "Start" for the best accuracy of plant recommendation.'
      } else {
        this.$refs.plant_rec.reset()
        this.startSensor()
        this.btn_note = 'Click "Stop" to see the result of the plant recommendation.'
      }
    },
    doLogout() {
    	this.$store.commit('updateToken', '')
    	this.$store.commit("setAuthUser", {authUser: '', isAuthenticated: false})
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
