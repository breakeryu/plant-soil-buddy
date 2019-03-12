<template>
  <div>
    <h2><u>Recommended Plants and Soil Types</u></h2>

    <div class="plant-list">
      <h3 v-for="plant in plants_list" :key="plant.id"><a href="#" class="plant" v-on:click="showPlantInfo(plant.id)">{{ plant.name }}</a>, <a class="soil">{{ plant.soil_type }} Soil</a></h3>
      <h3 v-if="!showing_results">-Results are not shown while recording-</h3>
      <h3 id="none" v-if="empty && showing_results">-None-</h3>
    </div>

      <br>
      <h2><u>Recommended NPK to analyze fertilizer</u></h2>
      <div id="npk">
      <h3>N (Nitrogen) to fill : &nbsp;&nbsp;&nbsp;&nbsp;<a class="nutrient">{{ n_lvl }}</a></h3>
      <h3>P (Phosphorus) to fill : &nbsp;&nbsp;&nbsp;&nbsp;<a class="nutrient">{{ p_lvl }}</a></h3>
      <h3>K (Potassium) to fill : &nbsp;&nbsp;&nbsp;&nbsp;<a class="nutrient">{{ k_lvl }}</a></h3>
      </div>
      <br>
  </div>
</template>

<script>
import axios from 'axios'

import router from '@/router'

export default {
  name: 'PlantRecommender',
  components: {  },
  data () {
    return {
      plants_list: [],
      showing_results: true,
      empty: true,
      good_avg_moist: 0.0,
      good_avg_acidity: 7.0,
      n_lvl: 'Unknown',
      p_lvl: 'Unknown',
      k_lvl: 'Unknown',
      lvl_config: {'none':'Unknown', 'low':'Low', 'mid':'Medium', 'high':'High'}
    }
  },
  methods: {
    getData(selected) {
      if (selected <= 0) {
        return
      }
      
      axios.post("/get_good_moist_ph_values", {
        'soil_profile_id': selected
      })
            .then((response) => {
              this.good_avg_moist = parseFloat(response.data['avg_good_moist'])
              this.good_avg_acidity = parseFloat(response.data['avg_good_acidity'])

              axios.post("/get_recommendations", {
                'soil_profile_id': selected,
                'good_avg_moist': this.good_avg_moist,
                'good_avg_acidity': this.good_avg_acidity
              })
                    .then((response) => {
                      this.getDataWithoutUpdating(selected)
                    })


            })
            
      this.showing_results = true
    },
    getDataWithoutUpdating(selected) {
      if (selected <= 0) {
        return
      }

      axios.post("/load_latest_plants_recommendation", {
                'soil_profile_id': selected
              })
                    .then((response) => {
                      this.plants_list = response.data
                      if (this.plants_list.length <= 0) {
                        this.empty = true
                      } else {
                        this.empty = false
                      }
                      this.showing_results = true
                    })
      
      axios.post("/load_latest_npk_recommendation", {
        'soil_profile_id': selected
      })
            .then((response) => {
              this.n_lvl = this.lvl_config[response.data['n_lvl']]
              this.p_lvl = this.lvl_config[response.data['p_lvl']]
              this.k_lvl = this.lvl_config[response.data['k_lvl']]

            })
            
      
    },
    reset() {
      this.showing_results = false
      this.plants_list = []
      this.empty = true
      this.n_lvl = 'Unknown'
      this.p_lvl = 'Unknown'
      this.k_lvl = 'Unknown'
    },
    showPlantInfo(plant_id){
      //console.log(name)
      this.$store.state.selected_plant = plant_id
      router.push('plantinfo')
    }
  },
  mounted(){
      
  }
}
</script>

<style scoped>
#none {
  color: red;
}
.plant {
  color: #01890c; /* Lush Green */
}
.soil {
  color: #703104; /* Dirt Brown */
}
#graph {
  display: inline-block;
  width: 600px;
  height: 600px;
}
.plant-list {
  display: inline-block;
  width: 300px;
  height: 300px;
  overflow-y: auto;
  border-style: inset;
  text-align: left;
}
#npk {
  display: inline-block;
  width: 300px;
  text-align: left;
}
.nutrient {
  text-align: right;
}
</style>