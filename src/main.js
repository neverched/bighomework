import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import router from './router'
import axios from 'axios'
import store from './store'

const app = createApp(App)

app.use(ElementPlus)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(router)

axios.defaults.baseURL = 'http://localhost:8080/api/'
app.config.globalProperties.$http = axios

app.use(store)

app.mount('#app')
