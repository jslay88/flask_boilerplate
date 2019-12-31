const usersStore = {
  state: {
    items: [],
    page: 1,
    perPage: 25,
    total: 0,
    loading: false
  },
  mutations: {
    ingestUserPage (state, userPage) {
      state.items = userPage.items
      state.page = userPage.page
      state.perPage = userPage.per_page
      state.total = userPage.total
    }
  },
  actions: {
    getUserPage ({ commit, state }, pageNumber) {
      console.log('Getting User Page', pageNumber)
      axios.get('/api/v1/user', {
        params: {
          page: pageNumber,
          per_page: state.perPage
        }
      })
      .then((resp) => {
        commit('ingestUserPage', resp.data)
      })
      .catch((err) => {
        console.warn('There was an error getting the User Page', err)
      })
    }
  },
  getters: {}
}

const tokensStore = {
  state: {
    items: [],
    page: 1,
    perPage: 30,
    total: 0
  },
  mutations: {
    ingestTokenPage (state, tokenPage) {
      state.items = tokenPage.items
      state.page = tokenPage.page
      state.perPage = tokenPage.per_page
      state.total = tokenPage.total
    }
  },
  actions: {
    getTokenPage ({ commit, state}, pageNumber) {
      console.log('Getting Token Page', pageNumber)
      axios.get('/api/v1/token', {
        params: {
          page: pageNumber,
          per_page: state.perPage
        }
      })
      .then((resp) => {
        commit('ingestTokenPage', resp.data)
      })
      .catch((err) => {
        console.warn('There was an error getting the Token Page', err)
      })
    }
  },
  getters: {}
}

const store = new Vuex.Store({
  modules: {
    users: usersStore,
    tokens: tokensStore
  }
})

appVue = new Vue({
  el: '#appVue',
  data: {
    promises: Array(),
    currentPage: 'index',
    pageLoading: true,
    currentPage: 'home'
  },
  template: `
    <div class="h-100">
      <div class="container-fluid h-100">
        <div class="row h-100">
          <nav class="col-1 col-md-2 bg-light mt-4 mt-sm-auto sidebar h-100">
            <div class="sidebar-sticky">
              <ul class="nav flex-column">
                <li class="nav-item">
                  <a v-bind:class="[currentPage == 'home' ? 'active' : '', 'nav-link']" @click="currentPage = 'home'" href="#">
                    <feather-icon name="home"></feather-icon>
                    <span class="d-none d-md-inline">Home</span>
                  </a>
                </li>
                <li class="nav-item">
                  <a v-bind:class="[currentPage == 'users' ? 'active' : '', 'nav-link']" @click="currentPage = 'users'" href="#">
                    <feather-icon name="users"></feather-icon>
                    <span class="d-none d-md-inline">Users</span>
                  </a>
                </li>
                <li class="nav-item">
                  <a v-bind:class="[currentPage == 'tokens' ? 'active' : '', 'nav-link']" @click="currentPage = 'tokens'" href="#">
                    <feather-icon name="key"></feather-icon>
                    <span class="d-none d-md-inline">My API Tokens</span>
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="/api/v1/">
                    <feather-icon name="file-text"></feather-icon>
                    <span class="d-none d-md-inline">API Documentation</span>
                  </a>
                </li>
              </ul>

              <footer class="footer d-none d-md-block mb-2">
                <div class="container text-center">
                  <span class="text-muted small">v1.0.0</span><br>
                  <span class="text-muted small">Built by jslay - 2020</span>
                </div>
              </footer>
            </div>


          </nav>
          <main role="main" class="col-md-10 ml-4 ml-sm-5 ml-md-auto col-lg-10 px-4 h-100">
            <transition-group name="fade" mode="out-in">
              <div class="pt-5 pt-sm-2 pb-3 h-100" key="pageView">
                <transition name="slide-fade" mode="out-in">
                  <home-page v-if="currentPage == 'home'" key="homePage"></home-page>
                  <users-page v-if="currentPage == 'users'" key="usersPage"></users-page>
                  <tokens-page v-if="currentPage == 'tokens'" key="tokensPage"></tokens-page>
                </transition>
              </div>
            </transition-group>
          </main>
        </div>
      </div>
    </div>
  `,
  mounted() {
    console.log('Vue App Mounted')
    this.pageLoading = false
  }
})
