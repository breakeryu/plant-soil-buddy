<template>
  <div>
    <h1>Recommended Plants</h1>
      <h3 v-for="plant in plants_list" :key="plant.id">= <a class="plant">{{ plant.name }}</a> =</h3>
      <h3 v-if="!showing_results">-Results are not shown while recording-</h3>
      <h3 id="none" v-if="empty && showing_results">-None-</h3>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'PlantRecommender',
  data () {
    return {
      plants_list: [],
      showing_results: true,
      empty: true
    }
  },
  methods: {
    getData(selected) {
      if (selected <= 0) {
        return
      }
      
      axios.post("/get_recommended_plants", {
        'soil_profile_id' : selected
      })
            .then((response) => {
              this.plants_list = response.data
              if (this.plants_list.length <= 0) {
                this.empty = true
              } else {
                this.empty = false
              }
            })
      this.showing_results = true
    },
    reset() {
      this.showing_results = false
      this.plants_list = []
      this.empty = true
    }
  },
  mounted(){
/*
    axios.get("/get_recommended_plants")
            .then((response) => {
              this.plants_list = response.data
            })
            */
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
</style>