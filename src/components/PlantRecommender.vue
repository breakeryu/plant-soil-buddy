<template>
  <div>
    <h1>Recommended Plants</h1>
      <p v-for="plant in plants_list" :key="plant.id">{{ plant.name }}</p>
      <p v-if="!showing_results">-N/A-</p>
      <p v-if="empty && showing_results">-None-</p>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'PlantRecommender',
  data () {
    return {
      plants_list: [],
      showing_results: false,
      empty: true
    }
  },
  methods: {
    getData() {
      axios.get("/get_recommended_plants")
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