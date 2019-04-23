<template>
  <div>
    <h2><u>Recommended Plants and Soil Types</u></h2>

    <div class="plant-list">
      <h3 v-for="plant in plants_list" :key="plant.id"><a href="#" class="plant" v-on:click="showPlantInfo(plant.id)">{{ plant.name }}</a>, <a class="soil">{{ plant.soil_type }} Soil</a></h3>
      <h3 v-if="!showing_results">-Results are not shown while recording-</h3>
      <h3 id="loading" v-if="loading && showing_results">Analyzing...</h3>
      <h3 class="warning" v-if="failed && showing_results">{{ failed_msg }}</h3>
      <h3 class="warning" v-if="empty && showing_results">-None-</h3>
      <h3 id="unused" v-if="unused && showing_results">This Soil Profile haven't yet been used or analyzed.</h3>
    </div>

    <p>You can click on the plant name for more informations.</p>
    <p><a href="#" class="tooltip" v-on:click="soilHint">What are each soil type means?
      </a></p>
      

      <br>
      <h2><u>Recommended NPK to analyze fertilizer</u></h2>
      <div id="npk">
      <h3>N (Nitrogen) to fill : <a class="nutrient">{{ n_lvl }}</a></h3>
      <h3>P (Phosphorus) to fill : <a class="nutrient">{{ p_lvl }}</a></h3>
      <h3>K (Potassium) to fill : <a class="nutrient">{{ k_lvl }}</a></h3>
      </div>
      <br>
      <p><a href="#" class="tooltip" v-on:click="npkHint">What do they mean?
      </a></p>
      

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
      loading: false,
      unused: false,
      failed: false,
      failed_msg: '',
      good_avg_moist: 0.0,
      good_avg_acidity: 7.0,
      most_frequency: 0.1,
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

      this.empty = false
      this.unused = false
      this.loading = true
      this.failed = false
      this.showing_results = true
      
      axios.post("/get_good_moist_ph_values", {
        'soil_profile_id': selected
      })
            .then((response) => {
              this.good_avg_moist = parseFloat(response.data['avg_good_moist'])
              this.good_avg_acidity = parseFloat(response.data['avg_good_acidity'])
              this.most_frequency = parseFloat(response.data['most_frequency'])

              axios.post("/get_recommendations", {
                'soil_profile_id': selected,
                'good_avg_moist': this.good_avg_moist,
                'good_avg_acidity': this.good_avg_acidity,
                'most_frequency': this.most_frequency
              })
                    .then((response) => {
                      this.getDataWithoutUpdating(selected)
                    })


            })
            .catch((error) => {
          if (error.response.status >= 400 && error.response.status < 500) {
            this.failed = true
            this.loading = false
            this.failed_msg = error.response.data
          } else {
            this.failed = true
            this.loading = false
            this.failed_msg = 'Internal Server Error'
          }
        })
            
      
    },
    getDataWithoutUpdating(selected) {
      if (selected <= 0) {
        return
      }
      this.failed = false
      axios.post("/load_latest_plants_recommendation", {
                'soil_profile_id': selected
              })
                    .then((response) => {
                      if (response.data == 'None') {
                          this.unused = true
                          this.empty = false
                          this.plants_list = []
                      } else {
                        this.plants_list = response.data
                        if (this.plants_list.length <= 0) {
                          this.empty = true
                          this.unused = false
                        } else {
                          this.empty = false
                          this.unused = false
                        }
                      }
                      
                      this.showing_results = true

                      this.loading = false
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
      this.empty = false
      this.unused = false
      this.failed = false
      this.n_lvl = 'Unknown'
      this.p_lvl = 'Unknown'
      this.k_lvl = 'Unknown'
    },
    showPlantInfo(plant_id){
      this.$store.state.selected_plant = plant_id
      router.push('plantinfo')
    },
    soilHint() {
      this.$notify({
          group: 'notify',
          title: 'What does Sandy Soil mean?',
          text: 'It is a soil that can only carry water for a short time. (Click to Dismiss)',
          duration: -1
        })
      this.$notify({
          group: 'notify',
          title: 'What does Loam Soil mean?',
          text: 'It is a soil that can carry water for an average time. (Click to Dismiss)',
          duration: -1
        })
      this.$notify({
          group: 'notify',
          title: 'What does Clay Soil mean?',
          text: 'It is a soil that can carry water for a really long time. (Click to Dismiss)',
          duration: -1
        })

    },
    npkHint() {
      this.$notify({
          group: 'notify',
          title: 'What do Recommended NPK to analyze fertilizer mean?',
          text: 'This shows the discretized amount of N, P, and K elements to fill into the soil via fertilizer. If one of them shows as low, you may do not even need to fill it at all. If all of them shows as low, then the soil may have perfect acidity. (Click to dismiss)',
          duration: -1
        })

    }
  },
  mounted(){
      
  }
}
</script>

<style scoped>
.warning {
  color: red;
}
.plant {
  color: #01890c; /* Lush Green */
}
.soil {
  color: #703104; /* Dirt Brown */
}
.tooltip {
  color: blue;
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