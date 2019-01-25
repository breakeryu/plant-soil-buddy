<template>
  <div>
    <ve-line :data="chartData"></ve-line>
  </div>
</template>

<script>
import axios from 'axios'
import VeLine from 'v-charts/lib/line.common'
export default {
  name: 'Chart',
  components: { VeLine },
  data () {
    return {
      chartData: {
        columns: [],
        rows: [
        ]
      }
    }
  },
  mounted(){

    axios.get("/get-temp-stats")
            .then((response) => {
              this.chartData = response.data
            })
  }
}
</script>