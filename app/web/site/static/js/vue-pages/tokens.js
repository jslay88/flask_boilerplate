Vue.component('tokens-page', {
  template: `
    <div>
      <div>
        <div class="row mb-2">
          <h4 class="col-md-9 col-lg-10 text-danger">My API Tokens</h4>

          <div class="col-md-3 col-lg-2">
            <button @click="showModal('add')" class="btn btn-sm btn-outline-danger form-control">Add Token</button>
          </div>
        </div>

        <p class="small text-muted">Total: {{ totalTokens }}
        <div class="table-responsive">
          <table class="table table-hover table-striped table-sm">
            <thead>
              <tr>
                <th>Description</>
                <th>Active</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="token in tokens">
                <td>{{ token.description }}</td>
                <td>{{ token.active }}</td>
                <td><span v-if="token.active" @click="showModal('delete', token.id, token.description)"><feather-icon name="x-square" class="pointer text-danger"></feather-icon></span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="modal" ref="modal" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header" v-if="addToken">
              <h5 class="modal-title">Create API Token</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body" v-if="addToken">
              <transition name="slide-fade" mode="out-in">
                <div v-if="modalStep == 1" key="step1">
                  <p>Provide a meaningful description</p>
                  <input type="text" class="form-control" v-model="newTokenDescription" />
                </div>
                <div v-if="modalStep == 2" key="step2">
                  <div class="progress">
                    <div class="progress-bar progress-bar-striped progress-bar-animated bg-danger" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>
                  </div>
                </div>
                <div class="text-center" v-if="modalStep == 3" key="step3">
                  <p>Store this somewhere safe.</p>
                  <p>This is the only time you will be able to get this token.</p>
                  <pre>{{ newToken }}</pre>
                </div>
              </transition>
            </div>
            <div class="modal-body" v-if="deleteToken">
              <transition name="slide-fade" mode="out-in">
                <div v-if="modalStep == 1" key="step1">
                  <p>Are you sure you want to delete this token?</p>
                  <pre>{{ confirmTokenDescription }}</pre>
                </div>
                <div v-if="modalStep == 2" key="step2">
                  <div class="progress">
                    <div class="progress-bar progress-bar-striped progress-bar-animated bg-danger" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>
                  </div>
                </div>
              </transition>
            </div>
            <div class="modal-footer" v-if="addToken && (modalStep == 1 || modalStep == 3)">
              <div v-if="modalStep == 1">
                <button type="button" class="btn btn-outline-danger" @click="createToken" :disabled="newTokenDescription.trim() == ''">Create Token</button>
              </div>
              <div v-if="modalStep == 3">
                <button type="button" class="btn btn-outline-danger" @click="newToken = ''; newTokenDescription = ''; modalStep = 1;">Create Another Token</button>
              </div>
            </div>
            <div class="modal-footer" v-if="deleteToken && (modalStep == 1 || modalStep == 3)">
              <div v-if="modalStep == 1">
                <button type="button" class="btn btn-outline-danger" @click="confirmDeleteToken">DELETE</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  data: function() {
    return {
      addToken: false,
      deleteToken: false,
      newTokenDescription: '',
      modalStep: 1,
      newToken: '',
      tokenToDelete: null,
      confirmTokenDescription: ''
    }
  },
  beforeMount () {
    console.log('Token Page Initializing...')
    this.getTokenPage(store.state.tokens.page)
  },
  mounted () {
    $(this.$refs.modal).on('hidden.bs.modal', () => {
      this.addToken = false
      this.deleteToken = false
      this.newTokenDescription = ''
      this.modalStep = 1
      this.newToken = ''
      this.tokenToDelete = null
      this.confirmTokenDescription = ''
    })
  },
  computed: {
    tokens () {
      return store.state.tokens.items
    },
    totalTokens() {
      return store.state.tokens.total
    }
  },
  methods: {
    getTokenPage (pageNumber) {
      store.dispatch('getTokenPage', pageNumber)
    },
    showModal (method, tokenId, tokenDescription) {
      if (method == 'add') {
        this.addToken = true
        this.deleteToken = false
        $(this.$refs.modal).modal('show')
      }
      if (method == 'delete') {
        this.deleteToken = true
        this.addToken = false
        this.confirmTokenDescription = tokenDescription
        this.tokenToDelete = tokenId
        $(this.$refs.modal).modal('show')
      }
    },
    createToken () {
      console.log('Creating API Token...')
      this.modalStep == 2
      axios.post('/api/v1/token', {'description': this.newTokenDescription})
      .then((resp) => {
        this.newToken = resp.data.token
        this.getTokenPage(store.state.tokens.page)
        this.modalStep = 3
      })
      .catch((err) => {
        console.warn('There was an error creating the API Token.', err)
        this.newToken = 'There was an error. Contact Support.'
        this.modalStep = 3
      })
    },
    confirmDeleteToken () {
      console.log('Deleting Token...')
      this.modalStep = 2
      axios.delete('/api/v1/token/' + this.tokenToDelete)
      .then((resp) => {
        this.getTokenPage(store.state.tokens.page)
        $(this.$refs.modal).modal('hide')
      })
    }
  }
})
