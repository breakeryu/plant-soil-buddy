<template>
  <div>
    <h1>Plant Information</h1>

    <h3>Plant Name : {{ plant_name }}</h3>

    <hr>

    <h3>Minimum Moist Level : {{ min_moist }}</h3>
    <h3>Maximum Moist Level : {{ max_moist }}</h3>

    <hr>

    <h3>Minimum Acidity in pH : {{ min_ph }}</h3>
    <h3>Maximum Acidity in pH : {{ max_ph }}</h3>

    <hr>

    <h3>Plant Life Cycle : {{ life_cycle }}</h3>

    <button id="trig-btn" class="normal-btn normal-btn soil-btn submit-btn" v-on:click="goBack">Back</button>
    
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
      life_cycle: 'Unknown',
      moist_config: {'none':'Unknown', 'very_low':'0-20% (Very Low)','low':'21-40% (Low)', 'mid':'41-60% (Medium)', 'high':'61-80% (High)', 'very_high':'81-100% (Very High)'},
      lifecycle_config: {'none':'Unknown', 'annual': 'Annual - Short Lived, less than a year', 'biennial': 'Biennial - Live around 1-2 years', 'perennial': 'Perennial - Long Lived, more than 2 years'}
    }
  },
  methods: {
    goBack() {
      router.push('main')
    }


  },
  mounted(){
      this.plant_id = this.$store.state.selected_plant

      axios.post("/get_plant_info", {
            'plant_id': this.plant_id
          })
            .then((response) => {
              this.plant_data = response.data

              this.plant_name = this.plant_data.name
              this.min_moist = this.moist_config[this.plant_data.min_moist]
              this.max_moist = this.moist_config[this.plant_data.max_moist]
              this.min_ph = this.plant_data.min_ph
              this.max_ph = this.plant_data.max_ph
              this.life_cycle = this.lifecycle_config[this.plant_data.life_cycle]
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