import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import axios from '@/plugins/axiosInstance'
import 'element-plus/dist/index.css'
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
// VuePress主题以及样式（这里也可以选择github主题）
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js';
import '@kangc/v-md-editor/lib/theme/style/vuepress.css';
import router from './router/index'

import { createPinia } from 'pinia';
import { createPersistedStatePlugin } from 'pinia-plugin-persistedstate-2';
import localforage from 'localforage';
import 'normalize.css/normalize.css';
import 'bytemd/dist/index.css';
import 'github-markdown-css/github-markdown.css';
import 'highlight.js/styles/vs.css';
import 'katex/dist/katex.css';
import './styles/style.less';
import '@kangc/v-md-editor/lib/style/preview.css';
// VuePress主题以及样式（这里也可以选择github主题）--VuePress主题代码呈黑色背景，github呈白色背景

// Prism
import Prism from 'prismjs';
// 代码高亮
import 'prismjs/components/prism-json';
import vuexStore from './store/index.js';

VMdPreview.use(vuepressTheme, {
  Prism,
});

const app = createApp(App)
const store = createPinia();
app.use(ElementPlus)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(router)
app.use(VMdPreview);
// axios.defaults.baseURL = 'http://localhost:8080/api/'
app.config.globalProperties.$http = axios

app.use(store)
app.use(vuexStore)
app.mount('#app')
