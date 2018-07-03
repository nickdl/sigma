<template>
  <div class="container mb-4">
    <div class="row justify-content-center">
      <div class="col-8 col-lg-2 mt-4">
        <img class="img-fluid" src="../assets/sigma.png" alt="">
      </div>
    </div>
    <div class="row justify-content-center">
      <div class="col-10 col-lg-4">
        <div>
          <div
            class="text-danger my-2"
            v-bind:style="{ visibility: error ? 'visible' : 'hidden' }"
          >{{ error ? error : 'Empty' }}</div>
          <div class="form-group">
            <label for="Username">Username</label>
            <input
              v-model="username"
              type="text"
              class="form-control"
              id="Username"
              placeholder="Username"
              v-bind:class="{ 'is-invalid': !valid.username }"
            >
          </div>
          <div class="form-group">
            <label for="Password">Password</label>
            <input
              v-model="password"
              type="password"
              class="form-control"
              id="Password"
              placeholder="Password"
              v-bind:class="{ 'is-invalid': !valid.password }"
            >
          </div>
          <button class="btn btn-primary btn-block mt-5" @click="submit(username, password)">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import router from '@/router'

export default {
  name: 'Login',
  data () {
    return {
      username: '',
      password: '',
      error: '',
      valid: {
        username: this.username !== '',
        password: this.password !== ''
      }
    }
  },
  methods: {
    submit (username, password) {
      if (!this.username) {
        this.valid.username = false
      }
      if (!this.password) {
        this.valid.password = false
      }
      this.error = ''
      if (this.username && this.password) {
        this.valid.username = true
        this.valid.password = true
        this.$api.login(username, password).then(() => {
          router.push({ path: '/' })
        }).catch(e => {
          this.error = e.message
        })
      }
    }
  }
}
</script>
