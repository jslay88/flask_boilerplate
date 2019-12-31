Vue.component('feather-icon', {
  props: ['name', 'size', 'alignment'],
  template: `
    <i :data-feather="name" :style="style"></i>
  `,
  mounted() {
    feather.replace()
  },
  beforeDestroy() {
    feather.replace()
  },
  computed: {
    style () {
      rv = {}
      if (this.alignment) {
        rv['vertical-align'] = this.alignment
      }
      if (this.size == null) {
        rv.width = '16px'
        rv.height = '16px'
      } else {
        rv.width = this.size + 'px',
        rv.height = this.size + 'px'
      }
      return rv
    }
  }
})
