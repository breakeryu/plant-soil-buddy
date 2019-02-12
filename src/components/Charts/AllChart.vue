<template>
  <div>
    <a><div id="graph"></div></a>
  </div>
</template>

<script>
import axios from 'axios'
import vis from 'vis'

export default {
  name: 'AllChart',
  components: { vis },
  data () {
    return {
      container: null
    }
  },
  methods: {
    getData(selected) {
      if (selected <= 0) {
        return
      }


      axios.post("/get_all_values_as_scatter", {
        'soil_profile_id' : selected
      })
            .then((response) => {
              var data = new vis.DataSet();
              var graph = null;

              var sqrt = Math.sqrt;
              var pow = Math.pow;

              for (var d in response.data) {
                console.log(response.data[d].moist)
                var x = parseInt(response.data[d].moist);
                var z = parseFloat(response.data[d].acidity);
                var y = parseInt(response.data[d].fertility);

                var dist = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2));
                var range = sqrt(2) + dist;
                data.add({x:x, y:y, z:z, style:range});
              }

              console.log(data)

              var options = {
                width:  '600px',
                height: '600px',
                style: 'dot-size',
                showPerspective: false,
                showGrid: true,
                keepAspectRatio: true,
                verticalRatio: 1.0,
                legendLabel: 'value',
                cameraPosition: {
                  horizontal: -0.35,
                  vertical: 0.22,
                  distance: 3.0
                },
                valueMax: 100,
                valueMin: 0,
                dotSizeMinFraction: 0.5,
                dotSizeMaxFraction: 2.5,
                xLabel: 'Moist (\%)',
                yLabel: 'Fertility (\%)',
                zLabel: 'Acidity (pH)'
              };

              graph = new vis.Graph3d(this.container, data, options)
            })

    }


  },
  mounted(){
      this.container = document.getElementById('graph')

  }

}
</script>

<style scoped>
#graph {
  display: inline-block;
  width: 600px;
  height: 600px;
}
</style>