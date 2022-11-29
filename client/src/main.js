import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { plugin, defaultConfig } from '@formkit/vue'
import '@formkit/themes/genesis'
import { FormKitSchema } from '@formkit/vue'

import './assets/main.css'
import Notifications from '@kyvg/vue3-notification'
import {Tabs, Tab} from 'vue3-tabs-component';

const app = createApp(App)

app.use(router)
app.use(plugin, defaultConfig)
app.use(Notifications)


import firebase from "firebase";
const firebaseConfig = {
  apiKey: "AIzaSyBe4lvj0ht4Rt4P4ILnJMsDMSIktA6Otqo",
  authDomain: "tomodachi-62b11.firebaseapp.com",
  projectId: "tomodachi-62b11",
  storageBucket: "tomodachi-62b11.appspot.com",
  messagingSenderId: "616234127121",
  appId: "1:616234127121:web:d72698d03399c59c5086b0",
  measurementId: "G-5R8DVKWLM3"
};

firebase.initializeApp(firebaseConfig);

app.component('tabs', Tabs)
.component('tab', Tab).mount('#app') 
