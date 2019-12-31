var firstRunVue = new Vue({
  el: '#firstRunVue',
  data: {
    stepTitle: 'Create First User',
  },
  template: `
  <div class="container mt-5">
    <h4 class="display-4">First Run</h4>
    <div class="card">
      <div class="card-header">
        First Run - {{ stepTitle }}
      </div>
      <div class="card-body">
        <create-account v-bind:successCallback="this.accountSuccessCallback">
        </create-account>
      </div>
    </div>
  </div>
  `,
  methods: {
    accountSuccessCallback: function() {
      location.href = '/'
    }
  }
})
