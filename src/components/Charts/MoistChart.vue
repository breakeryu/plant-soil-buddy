<template>
  <div>
    <h1>Moist Level</h1>
    <h3>Current: {{ current_data }} %</h3>
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
      chart_data: {
        columns: [],
        rows: [
        ]
      }
    }
  },
  mounted(){

    axios.get("/get_moist_as_value")
            .then((response) => {
              this.current_data = response.data
            })


    axios.get("/get_moist_as_stats")
            .then((response) => {
              this.chart_data = response.data
            })
  }
}
</script>