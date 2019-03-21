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
      <button class="normal-btn normal-btn soil-btn" v-on:click="soilProfileAdd" >Add</button>
      <button class="normal-btn normal-btn soil-btn" v-on:click="soilProfileEdit" :disabled="selected == 0">Edit</button>
      <button class="normal-btn normal-btn soil-btn exit-btn" v-on:click="soilProfileClear" :disabled="selected == 0">Reset</button>
      <button class="normal-btn normal-btn soil-btn exit-btn" v-on:click="soilProfileDelete" :disabled="selected == 0">Delete</button> 
    </p>

    <p>
      <button class="normal-btn normal-btn soil-btn exit-btn" v-on:click="soilProfileDebugLifeCycle(0)" v-if="debug" :disabled="selected == 0">Annual Debug</button> 
      <button class="normal-btn normal-btn soil-btn exit-btn" v-on:click="soilProfileDebugLifeCycle(1)" v-if="debug" :disabled="selected == 0">Biennial Debug</button> 
      <button class="normal-btn normal-btn soil-btn exit-btn" v-on:click="soilProfileDebugLifeCycle(2)" v-if="debug" :disabled="selected == 0">Perennial Debug</button> 
    </p>
<a href="#" class="tooltip" v-on:click="soilProfileHint">What is this?
      </a>
    
      <hr>
      <h1><u>Sensor Recording Statistics</u></h1>
      <br>
      <h4> Total Records of Soil Profile : {{ n_records }}</h4>

      <button class="normal-btn update-btn" v-on:click="goToScatterPlot" :disabled="selected == 0"">View Recorded Data Scatter Plot</button>

    <br><hr>
 
    <h1><u>Recommendation</u></h1>
    <br>
    <h2><u>Analysis</u></h2>
    <button class="normal-btn update-btn" v-on:click="analysisRecordsForRecommendation" :disabled="selected == 0"">Update Recommendation</button>
    <br>
    <plant-recommender ref="plant_rec"></plant-recommender>

  <hr>

  <h1><u>Search For Desired Plants</u></h1>
    <br>
    
    <plant-searcher ref="plant_search"></plant-searcher>

  <hr>

  <h1><u>User Management</u></h1>
  <br>
  <div id="userinfo">
    <h3>Username: {{ username }}</h3>
    <h3>Email: {{ email }}</h3>
    </div>
    <br v-if="is_staff">
    <button class="staff-btn normal-btn" v-if="is_staff" v-on:click="toAdmin">Update Knowledge Base (Admin Only)</button>
    <br>
    <button class="staff-btn normal-btn" v-if="is_staff" :disabled="debug" v-on:click="enableDebugging">Enable Debug Soil Profile (Admin Only)</button>
    <br>
    <button class="user-btn normal-btn" v-on:click="emailChange">Change E-mail</button><br>
    <br>
    <button class="user-btn normal-btn" v-on:click="pwdChange">Change Password</button><br>
    <br>
    <button class="logout-btn normal-btn exit-btn" v-on:click="doLogout">Logout</button><br>

  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'
import PlantRecommender from '@/components/Charts/PlantRecommender'
import PlantSearcher from '@/components/Charts/PlantSearcher'

export default {
  name: 'Welcome',
  components: {
    PlantRecommender,
    PlantSearcher
  },
  data () {
    return {
      username: '',
      email: '',
      is_staff: false,
      status_msg: 'Unknown',
      status_color: 'red',
      msg: 'Welcome,',
      btn_note: 'Make sure the sensors are all attached to the soil before clicking "Start Sensors" for the best accuracy of plant recommendation.',
      timer_running: false,
      timer: null,
      time: 6,
      n_records: 0,
      btn_text: "Start Sensors",
      port: 'COM8',
      soil_profiles : [],
      selected: 0,
      timer_connection: null,
      time_connection: 4,
      current_moist: '-',
      current_acidity: '-',
      debug: false
    }
  },
  methods: {
    toAdmin() {
      router.push("admindata")
    },
    pwdChange() {
      router.push("changepwd")
    },
    emailChange() {
      router.push("changeemail")
    },
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
    enableDebugging() {
      this.debug = true

      this.$notify({
          group: 'notify',
          title: 'Enable Debug',
          text: 'Enabled'
        })
    },
    soilProfileDebugLifeCycle(cycle_id) {
        axios.post("/debug_frequency", {
            'soil_profile_id': this.selected,
            'life_cycle_id': cycle_id
          })
            .then((response) => {
                this.$notify({
                  group: 'notify',
                  title: 'Debug',
                  text: 'Soil frequency of every records of this soil profile has changed for the life cycle.'
                })
            })
    },
    soilProfileHint() {
      this.$notify({
          group: 'notify',
          title: 'What is Soil Profile?',
          text: 'This is the storage of the recorded soil quality data specific to each soil chunk you record.'
        })
      this.$notify({
          group: 'notify',
          title: 'What is Soil Profile?',
          text: 'However, do not record more than 2 different soil chunks for one profile, otherwise the plant recommendation will be inaccurate.'
        })

    },
    goToScatterPlot() {
      if (this.selected <= 0) {
        this.$notify({
          group: 'notify',
          title: 'Soil Profile not selected',
          text: 'Please select your soil profile first.'
        })
        return
      }

      if (this.timer_running) {
        this.$notify({
          group: 'notify',
          title: 'Conflict error',
          text: 'You are currently recording.'
        })
        return
      }
      router.push('scatterchart')
    },
    snapReset() {
      axios.get("/snap_reset")
            .then((response) => {
              this.current_data = response.data
            })
    },
    getTotalNumberOfRecords() {
      axios.post("/get_total_records_per_soil", {
            'soil_profile_id': this.selected
          })
            .then((response) => {

              this.n_records = parseInt(response.data)
                
            })
    },
    analysisRecordsForRecommendation() {
      this.$refs.plant_rec.reset()
      this.$refs.plant_rec.getData(this.selected) //Where the fun begins
    },
    doLogout() {
    	this.$store.commit('updateToken', '')
    	this.$store.commit("setAuthUser", {authUser: '', isAuthenticated: false})
      this.$store.state.selected_soil_profile = 0
    	router.push('/')
    },
    reloadGraph(selected) {
      this.$store.state.selected_soil_profile = selected
      
      this.$refs.plant_rec.getDataWithoutUpdating(selected)
      this.getTotalNumberOfRecords()
      
    }
  },
  mounted(){
    this.username = this.$store.state.authUser
    this.selected = this.$store.state.selected_soil_profile

    axios.post("/get_soil_profiles", {
            'username': this.username
          })
            .then((response) => {
              this.soil_profiles = response.data
            })

    axios.post("/user_info", {
            'username': this.username
          })
            .then((response) => {
              if (response.data['email'] != '') {
                this.email = response.data['email']
              } else {
                this.email = '-'
              }
              
              var staff = response.data['is_staff']
              if (staff == 'True') {
                this.is_staff = true
              } else {
                this.is_staff = false
              }
            })

    this.reloadGraph(this.selected)
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
.user-btn {
  margin-bottom: 10px;
}
.logout-btn {
  margin-top: 20px;
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
  width: 300px;
  text-align: left;
}
#userinfo {
  display: inline-block;
  width: 300px;
  text-align: left;
}
.staff-btn, .update-btn {
  height: 60px;
}
</style>
