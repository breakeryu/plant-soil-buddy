<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <h3 class="warning" v-if="failed">{{ failed_msg }}</h3>
    <form class="form-regis" v-on:submit.prevent="register">
      <h3>Username</h3>
      <h5 class="info">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</h5>
      <input v-model="username" type="text" name="username"><br>
      <h3>Password</h3>
      <h5 class="info">Your password can't be too similar to your other personal information.</h5>
      <h5 class="info">Your password must contain at least 8 characters.</h5>
      <h5 class="info">Your password can't be a commonly used password.</h5>
      <h5 class="info">Your password can't be entirely numeric.</h5>
      <input v-model="password" type="password" name="password"><br>
      <h3>Confirm Password</h3>
      <h5 class="info">Enter the same password as before, for verification.</h5>
      <input v-model="confirm_password" type="password" name="password"><br><br>
      <button class="normal-btn submit-btn" type="submit">Register</button>
    </form>
    <button class="normal-btn" v-on:click="toLogin">Login</button>
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'

export default {
  data () {
    return {
      username: '',
      password: '',
      confirm_password: '',
      msg: 'Registeration',
      failed: false,
      failed_msg: ''
    }
  },
  methods: {
    register () {
      //alert(this.username)
      //alert(this.password)
      var self = this

      const input = {
        'username': this.username,
        'password' : this.password,
        'confirm_password': this.confirm_password
      }
      //alert(input['name']);
      //alert(input['password']);

      axios.post('register', input).then(req =>{
        console.log(req.data)
            //alert(req.data.token);
            //self.type = req.data.type;
            
        if (req.data == 'Success'){
          alert('Success')
          router.push("/login")
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
    toLogin () {
      router.push("/login")
    },
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
</style>
