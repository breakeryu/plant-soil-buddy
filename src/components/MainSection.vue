<template>
  <div class="hello">
    <h1>{{ msg }} {{ username }}!</h1>  

    <h2> Device Status: <a v-bind:style="{ color: status_color }">{{ status_msg }}</a></h2>
    <h3>Arduino Sensors USB Port Name : <input v-model="port" placeholder="Check in Device Manager" :disabled="timer_running"></h3>
    <button class="normal-btn submit-btn" v-on:click="recheckConnection" :disabled="timer_running">Re-check Connection</button><br>
    <p>
      <hr>

      <h3> Soil Profile : <select v-model="selected" v-on:change="reloadGraph(selected)" :disabled="timer_running">
        <option v-for="soil_profile in soil_profiles" v-bind:value="soil_profile.id"> {{ soil_profile.name }}, at {{ soil_profile.location }}</option>
      </select> </h3>
      <p>
      <button class="normal-btn normal-btn soil-btn" v-on:click="soilProfileAdd" :disabled="timer_running">Add</button>
      <button class="normal-btn normal-btn soil-btn" v-on:click="soilProfileEdit" :disabled="timer_running || selected == 0">Edit</button>
      <button class="normal-btn normal-btn soil-btn exit-btn" v-on:click="soilProfileClear" :disabled="timer_running || selected == 0">Clear</button>
      <button class="normal-btn normal-btn soil-btn exit-btn" v-on:click="soilProfileDelete" :disabled="timer_running || selected == 0">Delete</button> 
    </p>

      <hr><br><br>
    <button id="trig-btn" class="normal-btn" v-on:click="triggerSensor" v-bind:class="{ stop: timer_running }" :disabled='status_msg != "Connected" || selected == 0'>{{ btn_text }}</button>  
  </p>
    <h4> {{ btn_note }} </h4>
    <h4> Record snap time : {{ time }} </h4>

    <br><hr>

    <plant-recommender ref="plant_rec"></plant-recommender>

    <br><hr>
	<moist-chart ref="moist_ch"></moist-chart><hr>
  <acidity-chart ref="acidity_ch"></acidity-chart><hr>
  <fertility-chart ref="fertility_ch"></fertility-chart><hr>
  
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
      status_msg: 'Unknown',
      status_color: 'red',
      msg: 'Welcome,',
      btn_note: 'Make sure the sensors are all attached to the soil before clicking "Start Sensors" for the best accuracy of plant recommendation.',
      timer_running: false,
      timer: null,
      time: 6,
      btn_text: "Start Sensors",
      port: 'COM8',
      soil_profiles : [],
      selected: 0,
      timer_connection: null,
      time_connection: 4
    }
  },
  methods: {
    soilProfileAdd() {
        router.push('addsoil')
    },
    soilProfileEdit() {
        router.push('editsoil')
    },
    soilProfileClear() {
        router.push('clearsoil')
    },
    soilProfileDelete() {
        router.push('deletesoil')
    },
    snapReset() {
      axios.get("/snap_reset")
            .then((response) => {
              this.current_data = response.data
            })
    },
    readFromSensors() {
      axios.post("/get_all_values", {
            'port': this.port,
            'soil_profile_id': this.selected
          })
            .then((response) => {

              if (response.data > 0) {
                  this.$refs.moist_ch.getData(this.selected)
                  this.$refs.acidity_ch.getData(this.selected)
                  this.$refs.fertility_ch.getData(this.selected)
                  this.$store.state.selected_soil_profile = this.selected
                } else {
                  this.status_msg = "Disconnected"
                  this.status_color = 'red'
                  this.triggerSensor()
                }
            })
    },
    startSensor() {
      this.$refs.moist_ch.triggerStartStop()
      this.$refs.acidity_ch.triggerStartStop()
      this.$refs.fertility_ch.triggerStartStop()

      this.snapReset()
      this.btn_text = "Stop Sensors"
      this.timer_running = true
      this.readFromSensors()
      if (!this.timer) {
          this.timer = setInterval( () => {
            if (this.time > 0) {
               this.time--
            } else {
               this.time = 6
               this.readFromSensors()
            }
          }, 1000 )
       }
    },
    stopSensor() {
      this.$refs.moist_ch.triggerStartStop()
      this.$refs.acidity_ch.triggerStartStop()
      this.$refs.fertility_ch.triggerStartStop()

      this.btn_text = "Start Sensors"
      this.timer_running = false
      this.time = 6
      clearInterval(this.timer)
      this.timer = null

      this.$refs.moist_ch.current_data = 0
      this.$refs.acidity_ch.current_data = 7
      this.$refs.fertility_ch.current_data = 0

      //this.recheckConnection()

    },
    triggerSensor() {
      if (this.selected <= 0) {
        return
      }

      if (this.timer_running) {
        this.$refs.plant_rec.getData(this.selected)
        this.stopSensor()
        this.btn_note = 'Make sure the sensors are all attached to the soil before clicking "Start Sensors" for the best accuracy of plant recommendation.'
        this.connection_timer_idle_enable()
      } else {
        axios.post("/get_connection_status", {
            'port': this.port
          })
            .then((response) => {
              this.status_msg = response.data

              if (this.status_msg == 'Connected') {
                  this.status_color = 'green'
                  this.connection_timer_idle_disable()
                  this.startSensor()
                  this.btn_note = 'Click "Stop Sensors" to see the result of the plant recommendation.'

                  this.$refs.plant_rec.reset()

                } else {
                  this.status_color = 'red'
                }
            })

        
      }
    },
    doLogout() {
    	this.$store.commit('updateToken', '')
    	this.$store.commit("setAuthUser", {authUser: '', isAuthenticated: false})
    	router.push('/')
    },
    recheckConnection() {
      axios.post("/get_connection_status", {
            'port': this.port
          })
            .then((response) => {
              this.status_msg = response.data

              if (this.status_msg == 'Connected') {
                this.status_color = 'green'
              } else {
                this.status_color = 'red'
              }
            })
    },
    reloadGraph(selected) {
      this.$refs.moist_ch.getData(selected)
      this.$refs.acidity_ch.getData(selected)
      this.$refs.fertility_ch.getData(selected)
      this.$store.state.selected_soil_profile = selected
      
      this.$refs.plant_rec.getData(selected)
      
    },
    connection_timer_idle_enable() {
      if (!this.timer_connection) {
          this.timer_connection = setInterval( () => {
            if (this.time_connection > 0) {
               this.time_connection--
            } else {
               this.time_connection = 4
               this.recheckConnection()
            }
          }, 1000 )
       }
    },
    connection_timer_idle_disable() {
      this.time_connection = 4
      clearInterval(this.timer_connection)
      this.timer_connection = null
    }
  },
  mounted(){
    this.username = this.$store.state.authUser
    this.selected = this.$store.state.selected_soil_profile
    this.recheckConnection()

    axios.post("/get_soil_profiles", {
            'username': this.username
          })
            .then((response) => {
              this.soil_profiles = response.data
            })

    this.reloadGraph(this.selected)

    this.connection_timer_idle_enable()
    
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
#trig-btn {
  width: 350px;
  border: none;
  color: white;
  padding: 5px 12px;
  text-align: center;
  text-decoration: none;
  font-size: 20px;
  height: 60px;
}
.submit-btn {
  background-color: blue;
}
.exit-btn, .stop {
	background-color: red;
}
input, .normal-btn {
  width: 200px;
}
.soil-btn {
  margin-left: 10px;
  margin-right: 10px;
}
select {
  height: 45px;
  border: 3px solid #555;
  font-size: 16px;
}
button:disabled, #trig-btn:disabled {
  background-color: grey;
}
</style>
