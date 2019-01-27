<template>
  <div>
    <h1>Recommended Plants</h1>
      <p v-for="plant in plants_list" :key="plant.id">{{ plant.name }}</p>
      <p v-if="empty">-None-</p>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'PlantRecommender',
  data () {
    return {
      plants_list: [],
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