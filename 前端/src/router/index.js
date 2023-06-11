import {createRouter, createWebHistory} from 'vue-router'
import IndexEdit from '../views/IndexEdit.vue'
import UploadFileTest from '../views/UploadFileTest'
import ResourceEdit from '../views/ResourceEdit'
import QuestionEdit from '../views/QuestionEdit'
import NoticeEdit from '../views/NoticeEdit'
import IssueEdit from '../views/IssueEdit'
const routes = [
    {
        name: 'space',
        path: '/',
        component: () => import('../pages/Space'),
        children:[
            {
                name: 'house',
                path: '',
                component: () => import('../pages/space/House'),
            },
            {
                name: 'resource',
                path: 'resource',
                component: () => import('../pages/space/lists/ResourceList'),
            },
            {
                name: 'question',
                path: 'question',
                component: () => import('../pages/space/lists/QuestionList')
            },
            {
                name: 'exercise',
                path: 'exercise',
                component: () => import('../pages/space/lists/ExerciseList')
            },
            {
                name: 'notice',
                path: 'notice',
                component: () => import('../pages/space/lists/NoticeList')
            },
            {
                name: 'detail',
                path:'detail',
                component: () => import('../pages/space/Detail'),
                props($route){
                    return {
                        id:$route.query.id,
                        type:$route.query.type
                    }
                }
            },
            {
                path: 'about',
                name: 'about',
                component: IndexEdit
            },
            {
                path: 'resourceUpload',
                name: 'upload',
                // route level code-splitting
                // this generates a separate chunk (about.[hash].js) for this route
                // which is lazy-loaded when the route is visited.
                component: UploadFileTest
            },
            {
                path: 'resourceNew',
                name: 'ResourceEdit',
                // route level code-splitting
                // this generates a separate chunk (about.[hash].js) for this route
                // which is lazy-loaded when the route is visited.
                component: ResourceEdit
            },
            {
                path: 'questionNew',
                name: 'QuestionEdit',
                component: QuestionEdit
            },
            {
                path: 'noticeNew',
                name: 'NoticeEdit',
                component: NoticeEdit
            },
            {
                path: 'issueNew',
                name: 'IssueEdit',
                component: IssueEdit
            },
        ]
    },
    /* {
        name: 'user',
        path: '/user',
        component: () => import('../pages/User'),
        props($route){
            return {
                id:$route.query.id
            }
        }
    }, */
    {
        name: 'changePassword',
        path: '/changePassword',
        component: () => import('../views/user/ChangePWDView')
    },
    {
        name: 'search',
        path: '/search',
        component: () => import('../pages/Search'),
        props($route){
            return {
                firstInput:$route.query.input
            }
        }
    },
    //zjl_router_start
    {
        name:'sign_in',
        path:'/users/sign_in',
        component: () => import('@/views/user/SignInView.vue')
    },
    {
        name:'users',
        path:'/users/:id',
        component: () => import('@/views/user/UserView.vue'),
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
    //zjl_router_end
];
const router = createRouter({
    history: createWebHistory(), 
    routes
})
 
export default router