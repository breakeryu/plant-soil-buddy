<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <form class="form-regis" v-on:submit.prevent="register">
      <h3>Username</h3>
      <input v-model="username" type="text" name="username"><br>
      <h3>Password</h3>
      <input v-model="password" type="password" name="password"><br>
      <h3>Confirm Password</h3>
      <input v-model="confirm_password" type="password" name="password"><br><br>
      <button class="normal-btn submit-btn" type="submit">Register</button>
    </form>
    <br>
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
      msg: 'Registeration'
    }
  },
  methods: {
    register () {
      //alert(this.username)
      //alert(this.password)
      var self = this

      if (this.password != this.confirm_password) {
        alert('Password Failed')
        return
      }

      const input = {
        'username': this.username,
        'password' : this.password,
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
          alert('Failed')
          router.push("/regis")
        }
        return req
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
}
.submit-btn {
  background-color: blue;
}
input, .normal-btn {
  width: 200px;
}
</style>
