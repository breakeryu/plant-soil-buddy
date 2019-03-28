<template>
  <div class="hello">

    <h1>Scatter Chart Data of Soil Profile</h1>

    <h3>Soil Name : {{ soil_name }}</h3>
    <h3>Soil Location : {{ soil_location }}</h3>
    
    <scatter-chart :data="values" xtitle="Moist %" ytitle="Acidity pH" min="0"
        ></scatter-chart>
    <br>
    <button class="normal-btn exit-btn" v-on:click="goBack">Back</button>

  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'

export default {
  name: 'ScatterProof',
  components: {  },
  data () {
    return {
      soil_profile_id: 0,
      values: [],
      soil_name: '',
      soil_location: ''
    }
  },
  methods: {
    getData(selected) {
      if (selected <= 0) {
        return
      }
      
    },
    reset() {
      
      
    },
    goBack () {
      router.push("main")
    }


  },
  mounted(){
      this.soil_profile_id = this.$store.state.selected_soil_profile
      axios.post("/get_soil_profile", {
            'soil_profile_id': this.soil_profile_id
          })
            .then((response) => {
              this.soil_name = response.data['name']
              this.soil_location = response.data['location']
            })
      axios.post("/get_all_values_as_scatter", {
            'soil_profile_id': this.soil_profile_id
          })
            .then((response) => {

              this.values = response.data
                
            })

  }

}
</script>

<style scoped>
h1 {
  color: #42b983;
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
  width: 250px;
}
.submit-btn {
  background-color: blue;
  font-size: 18px;
  height: 55px;
}
.exit-btn, .stop {
  background-color: red;
}
</style>