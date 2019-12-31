var loginVue = new Vue({
  el: '#loginVue',
  data: {
    username: '',
    password: '',
    remember: false,
    submitting: false,
    errors: Array()
  },
  template: `
    <form class="form-signin" method="POST" id="login-form" @submit="validateForm" novalidate="true">
      <h1 class="h3 mb-3 font-weight-normal">Please sign in</h1>
      <label for="inputUsername" class="sr-only">Username</label>
      <input type="text" v-model="username" id="inputUsername" class="form-control mb-2" name="username" placeholder="Username" required autofocus>
      <label for="inputPassword" class="sr-only">Password</label>
      <input type="password" v-model="password" id="inputPassword" class="form-control" name="password" placeholder="Password" required>
      <div class="checkbox mb-3">
        <label>
          <input type="checkbox" name="remember-me" value="remember-me" v-model="remember"> Remember me
        </label>
      </div>
      <button class="btn btn-lg btn-outline-danger btn-block" type="submit">Sign in</button>
      <div class="alert alert-danger mt-2" v-if="errors.length">
        <ul>
          <li v-for="error in errors">{{ error }}</li>
        </ul>
      </div>
    </form>
  `,
  methods: {
    validateForm: function(e) {
      e.preventDefault()
      console.log('Validate Form')
      this.errors = Array()
      if (this.username == 'undefined' || this.username.trim() == '') {
        this.errors.push('Username is invalid.')
      }
      if (this.password == 'undefined' || this.password.trim() == '') {
        this.errors.push('Password is invalid.')
      }

      if (this.errors.length) {
        return false
      }

      this.submitForm()
    },
    submitForm: function() {
      console.log('Submit Form')
      this.submitting = true
      data = {
        username: this.username,
        password: sha256(this.password),
        remember: this.remember
      }
      axios.post(location.href, data).then((response) => {
        location.href = '/'
      }).catch((err) => {
        console.log(err)
        this.errors.push(err.response.data)
        this.submitting = false
      })
    }
  }
})
