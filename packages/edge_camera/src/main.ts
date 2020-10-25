import Vue from 'nativescript-vue'
import App from './components/App.vue'
import VueDevtools from 'nativescript-vue-devtools'
// import { CameraPlus } from '@nstudio/nativescript-camera-plus'

if(TNS_ENV !== 'production') {
  Vue.use(VueDevtools)
}
// Vue.registerElement('CameraPlus', CameraPlus);
// Vue.registerElement('CameraPlus', () => require('@nstudio/nativescript-camera-plus').CameraPlus);

import store from './store'

// Prints Vue logs when --env.production is *NOT* set while building
Vue.config.silent = (TNS_ENV === 'production')


new Vue({
  store,
  render: h => h('frame', [h(App)])
}).$start()
