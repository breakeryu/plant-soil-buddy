<template>
  <div>
    <h1>Soil Moist Level</h1>
    <h3>Current: {{ current_data }} %</h3>
    <h3>Average: {{ avg_data }} %</h3>
    <ve-line :data="chart_data"></ve-line>
  </div>
</template>

<script>
import axios from 'axios'
import VeLine from 'v-charts/lib/line.common'
export default {
  name: 'MoistChart',
  components: { VeLine },
  data () {
    return {
      current_data: 0,
      avg_data: 0,
      chart_data: {
        columns: [],
        rows: [
        ]
      }
    }
  },
  methods: {
    getData(selected) {
      axios.get("/get_moist_as_value")
            .then((response) => {
              if (response.data >= 0)  {
                this.current_data = response.data
              }
            })

      axios.post("/get_moist_as_stats", {
        'soil_profile_id' : selected
      })
            .then((response) => {
              this.chart_data = response.data
            })

      axios.post("/get_average_moist", {
        'soil_profile_id' : selected
      })
            .then((response) => {
              this.avg_data = response.data
            })
    }


  },
  mounted(){
/*
    axios.get("/get_moist_as_value")
            .then((response) => {
              this.current_data = response.data
            })


    axios.get("/get_moist_as_stats")
            .then((response) => {
              this.chart_data = response.data
            })
            */
  }
}
</script>