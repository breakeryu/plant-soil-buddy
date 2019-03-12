<template>
  <div class="hello">
    <h1 id="greeting">{{ msg }} {{ username }}!</h1>  
      <hr>

      <h1><u>Soil Data Record Management</u></h1> 
      <br>
      <h3> Soil Profile : <select v-model="selected" v-on:change="reloadGraph(selected)" :disabled="timer_running">
        <option v-for="soil_profile in soil_profiles" v-bind:value="soil_profile.id"> {{ soil_profile.name }}, at {{ soil_profile.location }}</option>
      </select> </h3>
      
      <p>
      <button class="normal-btn normal-btn soil-btn" v-on:click="soilProfileAdd" :disabled="timer_running">Add</button>
      <button class="normal-btn normal-btn soil-btn" v-on:click="soilProfileEdit" :disabled="timer_running || selected == 0">Edit</button>
      <button class="normal-btn normal-btn soil-btn exit-btn" v-on:click="soilProfileClear" :disabled="timer_running || selected == 0">Clear</button>
      <button class="normal-btn normal-btn soil-btn exit-btn" v-on:click="soilProfileDelete" :disabled="timer_running || selected == 0">Delete</button> 
    </p>
<a href="#" class="tooltip" v-on:click="soilProfileHint">What is this?
      </a>
    
      <hr>
      <h1><u>Sensor Recording Monitor</u></h1> 
      <br>
      <h2><u>Device Management</u></h2>
      <h3>Device Status : <a v-bind:style="{ color: status_color }">{{ status_msg }}</a></h3>
    <h3>Arduino Sensors USB Port Name : <input v-model="port" placeholder="Check in Device Manager" :disabled="timer_running"></h3>
    <button class="normal-btn submit-btn" v-on:click="recheckConnection" :disabled="timer_running">Re-check Connection</button><br>

    <h2><u>Current Sensor Records</u></h2>
    <div id="monitorvalues">
    <h3>Moist: &nbsp;&nbsp;&nbsp;&nbsp;{{ current_moist }}</h3>
    <h3>Acidity: &nbsp;&nbsp;&nbsp;&nbsp;{{ current_acidity }}</h3>
    <h4> Record snap time : &nbsp;&nbsp;&nbsp;&nbsp;{{ time }} seconds</h4>
    </div>
    <br>

    <h2><u>Main Control</u></h2>
    <p>
    <button id="trig-btn" class="normal-btn" v-on:click="triggerSensor" v-bind:class="{ stop: timer_running }" :disabled='status_msg != "Connected" || selected == 0'>{{ btn_text }}</button>  
    <h4> {{ btn_note }} </h4>
  </p>
  
  <br>
  
    

    <br><hr>
    <h1><u>Recommendation</u></h1>
    <br>
    <plant-recommender ref="plant_rec"></plant-recommender>

    <h2><u>Data Display</u></h2>

    <!--<all-chart ref="all_ch"></all-chart>-->

    <br><hr>
  <!--<fertility-chart ref="fertility_ch"></fertility-chart><hr>-->
  <h1><u>User Management</u></h1>
  <br>
    <button class="normal-btn exit-btn" v-on:click="doLogout">Logout</button><br>
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'
//import AllChart from '@/components/Charts/AllChart'
//import MoistChart from '@/components/Charts/MoistChart'
//import AcidityChart from '@/components/Charts/AcidityChart'
import PlantRecommender from '@/components/Charts/PlantRecommender'

export default {
  name: 'Welcome',
  components: {
    //AllChart,
    //MoistChart,
    //AcidityChart,
    //FertilityChart,
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
      time_connection: 4,
      current_moist: '-',
      current_acidity: '-'
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
    soilProfileHint() {
        alert('This is the storage of the recorded soil quality data specific to each soil chunk you record.')
        alert('However, do not record more than 2 different soil chunks for one profile, otherwise the plant recommendation will be inaccurate.')
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
                  //this.$refs.moist_ch.getData(this.selected)
                  axios.get("/get_moist_as_value")
                    .then((response) => {
                      if (response.data >= 0)  {
                        this.current_moist = response.data.toString() + ' %'
                      }
                    })
                  //this.$refs.acidity_ch.getData(this.selected)
                  axios.get("/get_acidity_as_value")
                    .then((response) => {
                      if (response.data >= 0)  {
                        this.current_acidity = response.data.toString() + ' pH'
                      }
                    })

                  this.$store.state.selected_soil_profile = this.selected
                } else {
                  this.status_msg = "Disconnected"
                  this.status_color = 'red'
                  this.triggerSensor()
                }
            })
    },
    startSensor() {
      //this.$refs.moist_ch.triggerStartStop()
      //this.$refs.acidity_ch.triggerStartStop()

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
      //this.$refs.moist_ch.triggerStartStop()
      //this.$refs.acidity_ch.triggerStartStop()

      this.btn_text = "Start Sensors"
      this.timer_running = false
      this.time = 6
      clearInterval(this.timer)
      this.timer = null

      //this.$refs.moist_ch.current_data = 0
      //this.$refs.acidity_ch.current_data = 7
      //this.$refs.fertility_ch.current_data = 0

      //this.recheckConnection()

    },
    triggerSensor() {
      if (this.selected <= 0) {
        return
      }

      if (this.timer_running) {
        this.stopSensor()
        this.$refs.plant_rec.getData(this.selected) //Where the fun begins
        //this.$refs.all_ch.getData(this.selected)
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
                  //this.$refs.all_ch.reset()

                } else {
                  this.status_color = 'red'
                }
            })

        
      }
    },
    doLogout() {
    	this.$store.commit('updateToken', '')
    	this.$store.commit("setAuthUser", {authUser: '', isAuthenticated: false})
      this.$store.state.selected_soil_profile = 0
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
      //this.$refs.all_ch.getData(selected)
      //this.$refs.moist_ch.getData(selected)
      //this.$refs.acidity_ch.getData(selected)

      this.$store.state.selected_soil_profile = selected
      
      this.$refs.plant_rec.getDataWithoutUpdating(selected)
      
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
#greeting {
  color: #42b983; 
}
h1 {
  color: #0900ff;
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
.tooltiptext {
  visibility: hidden;
  width: 200px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 1px 0;

  /* Position the tooltip */
  position: absolute;
  z-index: 1;
  bottom: 100%;
  left: 50%;
  margin-left: -60px;
}
.tooltip:hover .tooltiptext {
  visibility: visible;
}
#monitorvalues {
  display: inline-block;
  width: 200px;
  text-align: left;
}
</style>
