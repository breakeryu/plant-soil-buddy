<template>
  <div>
    <h1>Admin Database Management</h1>

    <button class="normal-btn push" v-on:click="pushPHtoNPKdata" :disabled="pushing">Data pH to NPK Push</button>

    <br>
    <button class="normal-btn push" v-on:click="pushPlantsData" :disabled="pushing">Data Plants Push</button>

    <br>
    <button class="normal-btn push" v-on:click="pushSoilTypesData" :disabled="pushing">Data Soil Types Push</button>

    <br><br>
    <button class="normal-btn exit-btn push" v-on:click="goBack" :disabled="pushing">Back</button><br>
    
    <loading :active.sync="pushing" 
        :can-cancel="false" 
        :is-full-page="true"></loading>

  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'
import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

export default {
  name: 'AdminDatabase',
  components: { 
    Loading
  },
  data () {
    return {
      pushing: false
    }
  },
  methods: {
    pushPHtoNPKdata() {
      this.pushing = true
      axios.get("/push_ph_to_npk_into_database")
            .then((response) => {
                this.pushing = false
                this.$notify({
                  group: 'notify',
                  title: 'Knowledge Base Update',
                  text: 'Done.'
                })
            })
    },
    pushPlantsData() {
      this.pushing = true
      axios.get("/push_plants_into_database")
            .then((response) => {
                this.pushing = false
                this.$notify({
                  group: 'notify',
                  title: 'Knowledge Base Update',
                  text: 'Done.'
                })
            })
    },
    pushSoilTypesData() {
      this.pushing = true
      axios.get("/push_soil_types_into_database")
            .then((response) => {
                this.pushing = false
                this.$notify({
                  group: 'notify',
                  title: 'Knowledge Base Update',
                  text: 'Done.'
                })
            })
    },
    goBack() {
      router.push("main")
    }


  },
  mounted(){

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  color: #42b983;
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
.submit-btn {
  background-color: blue;
}
input, .normal-btn {
  width: 200px;
}
.soil-btn {
  margin-left: 10px;
  margin-right: 10px;
}
.warning {
  color: red;
}
.exit-btn {
  background-color: red;
}
button:disabled, .push:disabled {
  background-color: grey;
}
</style>