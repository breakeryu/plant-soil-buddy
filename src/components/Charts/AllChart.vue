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
      container: null,
      color: []
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
                var x = parseInt(response.data[d].moist);
                var z = parseFloat(response.data[d].acidity);
                var y = parseInt(response.data[d].fertility);

                var cluster_group = parseInt(response.data[d].cluster_group);
                var good = parseInt(response.data[d].good);

                var style = 0

                /*
                  TO ADD

                  Telling each color its frequency, use color from back-end
                  This will look to makemore sense, as sometimes the chart colors weird 
                */
                if (good == 1) {
                  style = '#008000'
                } else if (good == 0) {
                  style = this.color[cluster_group]
                } else {
                  style = '#FF0000'
                }
                //var dist = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2));
                //var range = sqrt(2) + dist;
                data.add({x:x, y:y, z:z, style:style});
              }

              var options = {
                width:  '600px',
                height: '600px',
                style: 'dot-color',
                showPerspective: false,
                showGrid: true,
                keepAspectRatio: true,
                verticalRatio: 1.0,
                legendLabel: 'value',
                cameraPosition: {
                  horizontal: -0.35,
                  vertical: 0.22,
                  distance: 1.0
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

      this.color[0] = '#000000'
      this.color[1] = '#111111'
      this.color[2] = '#222222'
      this.color[3] = '#333333'
      this.color[4] = '#444444'
      this.color[5] = '#555555'
      this.color[6] = '#666666'
      this.color[7] = '#777777'
      this.color[8] = '#888888'
      this.color[9] = '#999999'
      this.color[10] = '#aaaaaa'
      this.color[11] = '#bbbbbb'
      this.color[12] = '#cccccc'
      this.color[13] = '#dddddd'

/*
      this.color[0] = '#808080'
      this.color[1] = '#000000'
      this.color[2] = '#FF0000'
      this.color[3] = '#008000'
      this.color[4] = '#00FFFF'
      this.color[5] = '#008080'
      this.color[6] = '#800080'
      this.color[7] = '#0000FF'
      this.color[8] = '#FF00FF'
      this.color[9] = '#000080'
      this.color[10] = '#00FF00'
      this.color[11] = '#808000'
      this.color[12] = '#FFFF00'
      this.color[13] = '#800000' */

      for (var i = 14; i < 1000; i++) {
        this.color[i] = '#'+Math.floor(Math.random()*16777215).toString(16)
      }

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