<template>
  <div>
    <h2><u>Recommended Plants and Soil Types</u></h2>
      <h3 v-for="plant in plants_list" :key="plant.id">= <a class="plant">{{ plant.name }}</a>, {{ plant.soil_type }} Soil =</h3>
      <h3 v-if="!showing_results">-Results are not shown while recording-</h3>
      <h3 id="none" v-if="empty && showing_results">-None-</h3>
      <br>
      <h2><u>Recommended NPK to analyze fertilizer</u></h2>

      <h3>N (Nitrogen) to fill : {{ n_lvl }}</h3>
      <h3>P (Phosphorus) to fill : {{ p_lvl }}</h3>
      <h3>K (Potassium) to fill : {{ k_lvl }}</h3>
      <br>
  </div>
</template>

<script>
import axios from 'axios'

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
      n_lvl: 'none',
      p_lvl: 'none',
      k_lvl: 'none'
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
              this.n_lvl = response.data['n_lvl']
              this.p_lvl = response.data['p_lvl']
              this.k_lvl = response.data['k_lvl']

            })
            
      
    },
    reset() {
      this.showing_results = false
      this.plants_list = []
      this.empty = true
      this.n_lvl = 'none'
      this.p_lvl = 'none'
      this.k_lvl = 'none'
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
  color: blue;
}
#graph {
  display: inline-block;
  width: 600px;
  height: 600px;
}
</style>