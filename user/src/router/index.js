// 该文件专门用于创建整个应用的路由器
import { createRouter,createWebHashHistory } from 'vue-router'
//引入组件
import SignInView from '@/views/user/SignInView'

//创建并暴露一个路由器
export default createRouter({
  history: createWebHashHistory(),
	routes:[
		{
			path:'/users/sign_in',
			component:SignInView
		}
	]
})