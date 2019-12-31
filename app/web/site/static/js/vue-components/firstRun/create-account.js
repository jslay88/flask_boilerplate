Vue.component('create-account', {
  props: ['successCallback', 'step', 'useAPI'],
  data: function() {
    return {
      username: '',
      password: '',
      secondPassword: '',
      errors: Array(),
      submitting: false,
    }
  } ,
  template: `
  <div>
    <form @submit="validateForm" novalidate="true" id="firstRunAccountForm" v-if="!submitting">
      <div class="form-group row justify-content-center">
        <label for="firstRunAccountUsername" class="col-sm-4 col-md-2 col-form-label">Username</label>
        <div class="col-sm-4">
          <input type="text" id="firstRunAccountUsername" class="form-control" v-model="username" name="username" required />
        </div>
      </div>
      <div class="form-group row justify-content-center">
        <label for="firstRunAccountPassword" class="col-sm-2 col-form-label">Password</label>
        <div class="col-sm-4">
          <input type="password" id="firstRunAccountPassword" class="form-control" v-model="password" name="password" required />
        </div>
      </div>
      <div class="form-group row justify-content-center">
        <label for="firstRunAccountSecondPassword" class="col-sm-2 col-form-label">Verify Password</label>
        <div class="col-sm-4">
          <input type="password" id="firstRunAccountSecondPassword" class="form-control" v-model="secondPassword" name="secondPassword" required />
        </div>
      </div>
      <div class="form-group row justify-content-center">
        <button class="btn btn-outline-danger col-sm-4">Submit</button>
      </div>
      <div class="form-group row justify-content-center">
        <div v-if="errors.length" class="alert alert-danger col-sm-6">
          <ul>
            <li v-for="error in errors">{{ error }}</li>
          </ul>
        </div>
      </div>
    </form>
    <h5 v-else class="text-center">Creating Account...</h5>
  </div>
  `,
  mounted() {
    this.resetForm()
    this.$on('resetForm', this.resetForm)
  },
  methods: {
    resetForm: function() {
      this.username = ''
      this.password = ''
      this.secondPassword = ''
      this.errors = Array()
      this.submitting = false
    },
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
      if (this.password != this.secondPassword) {
        this.errors.push('Passwords don\'t match.')
      }

      if (this.errors.length) {
        return false
      }

      this.submitForm()
    },
    submitForm: function() {
      console.log('Submit Form')
      this.submitting = true
      if (this.useAPI == true) {
        url = '/api/v1/user'
      } else {
        url = location.href
      }
      data = {
        step: this.step,
        username: this.username,
        password: sha256(this.password)
      }
      axios.post(url, data).then((response) => {
        this.successCallback()
      }).catch((err) => {
        console.log(err)
        this.errors.push(err.response.data)
        this.submitting = false
      })
    }
  }
})
