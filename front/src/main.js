import { createApp } from 'vue'
import App from './App.vue'
import VTooltip from 'v-tooltip';
import router from '../router/index.js'


createApp(App).use(router).use(VTooltip).mount('#app')
