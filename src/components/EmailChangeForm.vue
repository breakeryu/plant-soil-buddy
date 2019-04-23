<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <h3>User: {{ username }}</h3>
    <hr>
    <h3 class="warning" v-if="failed">{{ failed_msg }}</h3>
    <form class="form-regis" v-on:submit.prevent="changeEmail">
      <h3>New Email</h3>
      <h5 class="info">Can be either blank, or have text that contains '@'' and '.'' in order.</h5>
      <input v-model="email" type="text" name="email"><br>
      <hr>
      <button class="normal-btn submit-btn" type="submit">Change</button>
    </form>
    <button class="normal-btn exit-btn" v-on:click="goBack">Back</button>
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'

export default {
  data () {
    return {
      username: '',
      email: '',
      msg: 'E-mail Change',
      failed: false,
      failed_msg: ''
    }
  },
  methods: {
    changeEmail () {
      var self = this

      const input = {
        'username': this.username,
        'email': this.email
      }

      axios.post('change_email', input).then(req =>{
        console.log(req.data)
            
        if (req.data == 'Success'){
          this.$notify({
                group: 'notify',
                title: 'E-mail Change',
                text: 'Success'
          })
          router.push("main")
        } else {
          this.failed = true
          this.failed_msg = req.data
        }
        return req
      })
      .catch((error) => {
          if (error.response.status >= 400 && error.response.status < 500) {
            this.failed = true
            this.failed_msg = error.response.data
          } else {
            this.failed = true
            this.failed_msg = 'Internal Server Error'
          }
        })
    },
    goBack () {
      router.push("main")
    },
  },
  mounted(){
      this.username = this.$store.state.authUser
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
  margin-left: 10px;
  margin-right: 10px;
  margin-bottom: 30px;
}
.submit-btn {
  background-color: blue;
  font-size: 18px;
  height: 55px;
}
.warning {
  color: red;
}
.info {
  color: blue;
}
input, .normal-btn {
  width: 200px;
}
.exit-btn, .stop {
  background-color: red;
}
</style>
