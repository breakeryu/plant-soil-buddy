<template>
  <div>
    <h1>{{ username }} : Delete Soil Profile</h1>

    <h3>Soil Name : {{ old_name }}</h3>
    <h3>Soil Location : {{ old_location }}</h3>

    <br>
    <h3>Are you sure do you want to delete this soil profile? This cannot be undone.</h3>

    <button id="trig-btn" class="normal-btn normal-btn soil-btn exit-btn" v-on:click="deleteSoil">Delete</button>
    <button id="trig-btn" class="normal-btn normal-btn soil-btn" v-on:click="cancel">Cancel</button>

    <loading :active.sync="action" 
        :can-cancel="false" 
        :is-full-page="true"></loading>
    
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'

import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/vue-loading.css'

export default {
  name: 'DeleteSoilProfile',
  components: { 
    Loading
  },
  data () {
    return {
      username: '',
      old_name: '',
      old_location: '',
      soil_profile_id: 0,
      soil_profile: [],
      action: false
    }
  },
  methods: {
    deleteSoil() {
      this.action = true
      axios.post("/delete_soil_profile", {
        'soil_profile_id' : this.soil_profile_id
      })
            .then((response) => {
              this.$notify({
                  group: 'notify',
                  title: 'Delete Soil Profile',
                  text: response.data
                })
              router.push('main')
            })
            .catch((error) => {
            this.action = false
          if (error.response.status >= 400 && error.response.status < 500) {
            this.$notify({
              group: 'notify',
              title: 'Error',
              text: error.response.data
            })
          } else {
            this.$notify({
              group: 'notify',
              title: 'Error',
              text: 'Internal Server Error'
            })
          }
        })
    },
    cancel() {
      router.push('main')
    }


  },
  mounted(){
      this.username = this.$store.state.authUser
      this.soil_profile_id = this.$store.state.selected_soil_profile

      axios.post("/get_soil_profile", {
            'soil_profile_id': this.soil_profile_id
          })
            .then((response) => {
              this.soil_profile = response.data

              this.old_name = this.soil_profile.name
              this.old_location = this.soil_profile.location
            })
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
.exit-btn {
  background-color: red;
}
input, .normal-btn {
  width: 200px;
}
.soil-btn {
  margin-left: 10px;
  margin-right: 10px;
}
</style>