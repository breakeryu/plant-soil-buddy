<template>
  <div>
    <h1>Soil Acidity Level</h1>
    <h3>Current: <a v-if="recording">{{ current_data }} %</a><a v-if="!recording">-</a></h3>
    <h3>Average: {{ avg_data }} pH</h3>
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
      },
      recording: false
    }
  },
  methods: {
    triggerStartStop() {
      if (this.recording) {
        this.recording = false
      } else {
        this.recording = true
      }
    },
    getData(selected) {
      if (selected <= 0) {
        return
      }
      
      axios.get("/get_acidity_as_value")
            .then((response) => {
              if (response.data >= 0)  {
                this.current_data = response.data
              }
            })

      axios.post("/get_acidity_as_stats", {
        'soil_profile_id' : selected
      })
            .then((response) => {
              this.chart_data = response.data
            })

      axios.post("/get_average_acidity", {
        'soil_profile_id' : selected
      })
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