<template>
  <div>
    <h1>Recommended Plants : {{ plants_list.plants }} </h1>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'PlantRecommender',
  data () {
    return {
      plants_list: {
        plants: []
      }
    }
  },
  mounted(){

    axios.get("/get-recommended-plants")
            .then((response) => {
              this.plants_list = response.data
            })
  }
}
</script>