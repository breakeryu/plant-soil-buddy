<template>
  <div>
    <h1>{{ username }} : Edit Soil Profile</h1>

    <h3 class="warning" v-if="failed">{{ failed_msg }}</h3>

    <h3>Soil Name : {{ old_name }}</h3>
    <h3>To : <input v-model="name"></h3>
    <h3>Soil Location : {{ old_location }}</h3>
    <h3>To : <input v-model="location"></h3>

    <button id="trig-btn" class="normal-btn normal-btn soil-btn submit-btn" v-on:click="edit">Edit</button>
    <button id="trig-btn" class="normal-btn normal-btn soil-btn" v-on:click="cancel">Cancel</button>
    
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'

export default {
  name: 'EditSoilProfile',
  components: { 
  },
  data () {
    return {
      username: '',
      old_name: '',
      old_location: '',
      name: '',
      location: '',
      soil_profile_id: 0,
      soil_profile: [],
      failed: false,
      failed_msg: ''
    }
  },
  methods: {
    edit() {
      axios.post("/edit_soil_profile", {
        'soil_profile_id' : this.soil_profile_id,
        'name': this.name,
        'location': this.location
      })
            .then((response) => {
              alert(response.data)
              router.push('main')
            })
            .catch((error) => {
          if (error.response.status >= 400 && error.response.status < 500) {
            this.failed = true
            this.failed_msg = error.response.data
          } else {
            this.failed = true
            this.failed_msg = 'Internal Server Error'
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
.submit-btn {
  background-color: blue;
}
input, .normal-btn {
  width: 200px;
}
.soil-btn {
  margin-left: 10px;
  margin-right: 10px;
}
.warning {
  color: red;
}
</style>