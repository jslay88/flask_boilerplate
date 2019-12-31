Vue.component('users-page', {
  template: `
  <div>
      <div key="table">
        <div class="row mb-2">
          <h4 class="col-md-9 col-lg-10 text-danger">Users</h4>

          <div class="col-md-3 col-lg-2">
            <button @click="showModal" class="btn btn-sm btn-outline-danger form-control">Add User</button>
          </div>
        </div>

        <p class="small text-muted">Total: {{ totalUsers }}
        <div class="table-responsive">
          <table class="table table-hover table-striped table-sm">
            <thead>
              <tr>
                <th>Username</>
                <th>Active</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users">
                <td>{{ user.username }}</span></td>
                <td>{{ user.active }}</td>
                <td></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="modal" ref="modal" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add User</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body container-fluid">
              <create-account ref="createAccountForm" :useAPI="true" :successCallback="hideModal"></create-account>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  data: function() {
    return {
      addUser: false,
    }
  },
  beforeMount () {
    console.log('User Page Initializing...')
    this.getUserPage(store.state.users.page)
  },
  mounted () {
    $(this.$refs.modal).on('hidden.bs.modal', () => {
      this.getUserPage(store.state.users.page)
      this.$refs.createAccountForm.resetForm()
    })
  },
  computed: {
    users () {
      return store.state.users.items
    },
    totalUsers() {
      return store.state.users.total
    }
  },
  methods: {
    getUserPage (pageNumber) {
      store.dispatch('getUserPage', pageNumber)
    },
    showModal () {
      $(this.$refs.modal).modal('show')
    },
    hideModal () {
      $(this.$refs.modal).modal('hide')
    }
  }
})
