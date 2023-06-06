import { createApp } from 'vue'
import App from './App.vue'

//引入ElementPlus组件
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

//引入VueRouter组件
import router from '@/router/index.js'

//引入vuex
import store from '@/store/index.js'

//引入axios
import axios from '@/plugins/axiosInstance.js'

//引入ElementPlus图标
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(ElementPlus)
app.use(router)
app.use(store)

app.mount('#app')

app.config.globalProperties.$axios = axios
