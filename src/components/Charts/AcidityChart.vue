<template>
  <div>
    <h1>Soil Acidity Level</h1>
    <h3>Current: {{ current_data }} pH</h3>
    <h3>Average for most recent 10 records: {{ avg_data }} pH</h3>
    <ve-line :data="chart_data"></ve-line>
  </div>
</template>

<script>
import axios from 'axios'
import VeLine from 'v-charts/lib/line.common'
export default {
  name: 'AcidityChart',
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
    getData() {
      axios.get("/get_acidity_as_value")
            .then((response) => {
              this.current_data = response.data
            })

      axios.get("/get_acidity_as_stats")
            .then((response) => {
              this.chart_data = response.data
            })

      axios.get("/get_average_acidity")
            .then((response) => {
              this.avg_data = response.data
            })
    }
  },
  mounted(){
/*
    axios.get("/get_acidity_as_value")
            .then((response) => {
              this.current_data = response.data
            })


    axios.get("/get_acidity_as_stats")
            .then((response) => {
              this.chart_data = response.data
            })\
        */
  }
}
</script>