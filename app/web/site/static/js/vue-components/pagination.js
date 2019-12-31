Vue.component('pagination', {
  template: `
    <div class="row m-0">
      <nav class="col-6 p-0">
        <ul class="pagination">
          <li class="page-item" v-if="page > 1">
            <a class="page-link text-danger" href="#" aria-label="Previous" @click="pageLoadCallback(page - 1)">
              <feather-icon name="arrow-left" size="12" alignment="middle"></feather-icon>
            </a>
          </li>
          <li class="page-item" v-if="page > 1">
            <a class="page-link text-danger" href="#" @click="pageLoadCallback(page - 1)">{{ page - 1 }}</a>
          </li>
          <li class="page-item"><a href="#" class="page-link text-secondary" @click="pageLoadCallback(page)">{{ page }}</a></li>
          <li class="page-item" v-if="page != pages">
            <a class="page-link text-danger" href="#" @click="pageLoadCallback(page + 1)">{{ page + 1 }}</a>
          </li>
          <li class="page-item" v-if="page != pages">
            <a class="page-link text-danger" href="#" aria-label="Next" @click="pageLoadCallback(page + 1)">
              <feather-icon name="arrow-right" size="12" alignment="middle"></feather-icon>
            </a>
          </li>
        </ul>
      </nav>

      <div class="col-6 p-0">
        <div class="btn-group float-right">
          <button type="button" class="btn btn-secondary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            Right-aligned menu
          </button>
          <div class="dropdown-menu dropdown-menu-right">
            <!-- Need to finish this -->
            <button class="dropdown-item" type="button">Action</button>
            <button class="dropdown-item" type="button">Another action</button>
            <button class="dropdown-item" type="button">Something else here</button>
          </div>
        </div>
      </div>

    </div>
  `,
  props: ['page', 'perPage', 'pages', 'loading', 'pageLoadCallback']
})
