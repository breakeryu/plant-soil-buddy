<template>
  <div>
      <h2><u>Query Search for Desired Plant</u></h2>
      <h3>Query Word : <input v-model="query"></h3>
      <button class="normal-btn normal-btn soil-btn submit-btn" v-on:click="search">Search</button>
      <br>

    <h2><u>Search Results</u></h2>

    <div class="plant-list">
      <h3 v-for="plant in plants_list" :key="plant.id"><a href="#" class="plant" v-on:click="showPlantInfo(plant.id)">{{ plant.name }}</a></a></h3>
      <h3 v-if="!showing_results">-No results-</h3>
      <h3 id="loading" v-if="loading && showing_results">Searching...</h3>
      <h3 class="warning" v-if="failed && showing_results">{{ failed_msg }}</h3>
      <h3 class="warning" v-if="empty && showing_results">-None-</h3>
    </div>

    <p>You can click on the plant name for informations.</p>

      

  </div>
</template>

<script>
import axios from 'axios'

import router from '@/router'


export default {
  name: 'PlantSearcher',
  components: {  },
  data () {
    return {
      plants_list: [],
      showing_results: true,
      empty: true,
      loading: false,
      failed: false,
      failed_msg: '',
      query: ''
    }
  },
  methods: {
    search() {
      axios.post("/load_plant_search_results", {
        'query': this.query
      })
            .then((response) => {
              this.plants_list = response.data

              if (this.plants_list.length <= 0) {
                  this.empty = true
              } else {
                  this.empty = false
              }

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
.warning {
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
  height: 200px;
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
.soil-btn {
  margin-left: 10px;
  margin-right: 10px;
}
.submit-btn {
  background-color: blue;
}
#trig-btn {
  width: 350px;
  border: none;
  color: white;
  padding: 5px 12px;
  text-align: center;
  text-decoration: none;
  font-size: 20px;
  height: 60px;
}
input, .normal-btn {
  width: 200px;
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
.exit-btn, .stop {
  background-color: red;
}
</style>