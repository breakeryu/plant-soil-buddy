<template>
  <div class="hello">
    <a><div id="graph"></div></a>
    

  </div>
</template>

<script>
import axios from 'axios'
import vis from 'vis'

export default {
  name: 'ScatterProof',
  components: { vis },
  data () {
    return {
      soil_profile_id: 0,
      container: null,
      color: [],
      options: {
                sort: false,
                sampling:false,
                style:'points',
                drawPoints: {
                    enabled: true,
                    size: 6,
                    style: 'circle' // square, circle
                },
                defaultGroup: 'Scatterplot',
                width: '350px',
                height: '350px',
                xLabel: 'Moist (\%)',
                yLabel: 'Acidity (pH)'
              },
      clusters_count: [0,0,0,0,0,0,0,0,0,0],
      good_cluster: 0
    }
  },
  methods: {
    getData(selected) {
      if (selected <= 0) {
        return
      }


      

    },
    reset() {
      this.clusters_count = [0,0,0,0,0,0,0,0,0,0]
      this.good_cluster = 0

      this.container.innerHTML = "";
      
    }


  },
  mounted(){
      this.soil_profile_id = this.$store.state.selected_soil_profile
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

      axios.post("/get_all_values_as_scatter", {
        'soil_profile_id' : this.soil_profile_id
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
                var y = parseFloat(response.data[d].acidity);

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
                data.add({x:x, y:y, style:style});
                this.clusters_count[cluster_group]++;
              }



              if (response.data.length > 0) {
                graph = new vis.Graph2d(this.container, data, this.options)
              }

            })

  }

}
</script>

<style scoped>
#graph {
  display: inline-block; /*set center */
  width: 350px;
  height: 350px;
  border-style: inset;
}
</style>