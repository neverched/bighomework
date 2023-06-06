// 该文件专门用于创建整个应用的路由器
import { createRouter,createWebHashHistory } from 'vue-router'

//创建并暴露一个路由器
export default createRouter({
  history: createWebHashHistory(),
	routes:[
		{
			name:'sign_in',
			path:'/users/sign_in',
			component: () => import('@/views/user/SignInView.vue')
		},
		{
			name:'users',
			path:'/users/:id(\\d+)',
			component: () => import('@/views/user/UserView.vue'),
			props:true,
			children: [
				{
					name:'activities',
					path:'activities',
				},
				{
					name:'spaces',
					path:'spaces',
				},
				{
					name:'docs',
					path:'docs',
				},
				{
					name:'issues',
					path:'issues',
				},
				{
					name:'answers',
					path:'answers',
				},
				{
					name:'questions',
					path:'questions',
				},
				{
					name:'collections',
					path:'collections',
				},
				{
					name:'following',
					path:'following',
				},
			]
		},
		{
			name:'edit',
			path:'/users/edit',
		},
		{
			name:'settings',
			path:'/users/settings',
			children: [
				{
					name:'password',
					path:'password',
				}
			]
		},
	]
})