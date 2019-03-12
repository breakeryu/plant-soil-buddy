<template>
  <div>
    <h1>Admin Database Management</h1>

    <button class="normal-btn" v-on:click="pushPHtoNPKdata">Data pH to NPK Push</button>

    <br>
    <button class="normal-btn" v-on:click="pushPlantsData">Data Plants Push</button>

    <br>
    <button class="normal-btn" v-on:click="pushSoilTypesData">Data Soil Types Push</button>
    
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'

export default {
  name: 'AddSoilProfile',
  components: { 
  },
  data () {
    return {
      plant_id: 0,
      plant_name: '',
      min_moist: 'Unknown',
      max_moist: 'Unknown',
      min_ph: 'Unknown',
      max_ph: 'Unknown',
      moist_config: {'none':'Unknown', 'very_low':'0-20% (Very Low)','low':'21-40% (Low)', 'mid':'41-60% (Medium)', 'high':'61-80% (High)', 'very_high':'81-100% (Very High)'}
    }
  },
  methods: {
    pushPHtoNPKdata() {
      axios.get("/push_ph_to_npk_into_database")
            .then((response) => {

            })
    },
    pushPlantsData() {
      axios.get("/push_plants_into_database")
            .then((response) => {

            })
    },
    pushSoilTypesData() {
      axios.get("/push_soil_types_into_database")
            .then((response) => {

            })
    }


  },
  mounted(){
      
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