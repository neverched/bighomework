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
					component: () => import('@/components/users/MainActivities.vue')
				},
				{
					name:'spaces',
					path:'spaces',
					component: () => import('@/components/users/MainSpaces.vue')
				},
				{
					name:'docs',
					path:'docs',
					component: () => import('@/components/users/MainDocs.vue')
				},
				{
					name:'issues',
					path:'issues',
					component: () => import('@/components/users/MainIssues.vue')
				},
				{
					name:'answers',
					path:'answers',
					component: () => import('@/components/users/MainAnswers.vue')
				},
				{
					name:'questions',
					path:'questions',
					component: () => import('@/components/users/MainQuestions.vue')
				},
				{
					name:'collections',
					path:'collections',
					component: () => import('@/components/users/MainCollections.vue')
				},
				{
					name:'following',
					path:'following/:type',
					component: () => import('@/components/users/MainFollowing.vue')
				},
			]
		},
		{
			name:'edit',
			path:'/users/:id/edit',
			component: () => import('@/views/user/EditView.vue')
		},
		{
			name:'settings',
			path:'/users/settings',
			component: () => import('@/views/user/ChangePWDView.vue')
		},
	]
})