<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <h3 class="warning" v-if="failed">{{ failed_msg }}</h3>
    <form class="form-regis" v-on:submit.prevent="changePassword">
      <h3>Old Password</h3>
      <h5 class="info">Required. For security confirmation.</h5>
      <input v-model="old_password" type="password" name="password"><br>
      <hr>
      <h3>New Password</h3>
      <h5 class="info">Your password can't be too similar to your other personal information.</h5>
      <h5 class="info">Your password must contain at least 8 characters.</h5>
      <h5 class="info">Your password can't be a commonly used password.</h5>
      <h5 class="info">Your password can't be entirely numeric.</h5>
      <input v-model="password" type="password" name="password"><br>
      <hr>
      <h3>Confirm New Password</h3>
      <h5 class="info">Enter the same password as before, for verification.</h5>
      <input v-model="confirm_password" type="password" name="password"><br><br>
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
      old_password: '',
      password: '',
      confirm_password: '',
      msg: 'Password Change',
      failed: false,
      failed_msg: ''
    }
  },
  methods: {
    changePassword () {
      //alert(this.username)
      //alert(this.password)
      var self = this

      const input = {
        'username': this.username,
        'old_password': this.old_password,
        'password' : this.password,
        'confirm_password': this.confirm_password
      }
      //alert(input['name']);
      //alert(input['password']);

      axios.post('change_password', input).then(req =>{
        console.log(req.data)
            //alert(req.data.token);
            //self.type = req.data.type;
            
        if (req.data == 'Success'){
          this.$notify({
                group: 'notify',
                title: 'Password Change',
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
