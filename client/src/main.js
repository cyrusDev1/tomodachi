import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { plugin, defaultConfig } from '@formkit/vue'
import '@formkit/themes/genesis'
import './assets/main.css'
import Notifications from '@kyvg/vue3-notification'

const app = createApp(App)

app.use(router)
app.use(plugin, defaultConfig)
app.use(Notifications)
app.mount('#app')
