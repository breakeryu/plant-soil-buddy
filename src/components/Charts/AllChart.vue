<template>
  <div>
    <a><div id="graph"></div></a>
    <p>
    <a v-for="i in 10"><a :style="{color: color[i-1]}" v-if="clusters_count[i-1] > 0">  [#{{ i }} &#9673; : {{ clusters_count[i-1] }}]  </a> </a>
    <p :style="{color: color[good_cluster-1]}" v-if="good_cluster > 0">The considered value group of &#9673; : #{{ good_cluster }}</p></p>
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
      color: [],
      clusters_count: [0,0,0,0,0,0,0,0,0,0],
      good_cluster: 0
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
              this.clusters_count = [0,0,0,0,0,0,0,0,0,0]
              this.good_cluster = 0

              var sqrt = Math.sqrt;
              var pow = Math.pow;

              for (var d in response.data) {
                var x = parseInt(response.data[d].moist);
                var z = parseFloat(response.data[d].acidity);
                var y = parseInt(response.data[d].fertility);

                var cluster_group = parseInt(response.data[d].cluster_group);
                var good = parseInt(response.data[d].good);

                var style = 0

                if (good == 1) {
                  style = this.color[cluster_group]
                  //style = '#00FF00' //Lime Green
                  this.good_cluster = cluster_group+1
                } else if (good == 0) {
                  style = this.color[cluster_group]
                } else {
                  style = '#FF0000' //Red
                }
                //var dist = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2));
                //var range = sqrt(2) + dist;
                data.add({x:x, y:y, z:z, style:style});
                this.clusters_count[cluster_group]++;
              }

              var options = {
                width:  '1000px',
                height: '600px',
                style: 'dot-color',
                showPerspective: false,
                showGrid: true,
                keepAspectRatio: true,
                verticalRatio: 1.0,
                legendLabel: 'cluster group',
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

              if (response.data.length > 0) {
                graph = new vis.Graph3d(this.container, data, options)
              }

            })

    }


  },
  mounted(){
      this.container = document.getElementById('graph')

      this.color[0] = '#000000' //Black
      this.color[1] = '#B22222' //Fire Brick
      this.color[2] = '#006400' //Dark Green
      this.color[3] = '#008B8B' //Dark Cyan
      this.color[4] = '#000080' //Navy
      this.color[5] = '#8B008B' //Dark Magneta
      this.color[6] = '#4B0082' //Indigo
      this.color[7] = '#C71585' //Medium Violet Red
      this.color[8] = '#800000' //Maroon
      this.color[9] = '#2F4F4F' //Dark Slate Grey

  }

}
</script>

<style scoped>
#graph {
  display: inline-block;
  width: 1000px;
  height: 600px;
  border-style: inset;
}
</style>