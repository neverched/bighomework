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
    {
        name: 'user',
        path: '/user/:id',
        component: () => import('../pages/User'),
        props($route){
            return {
                id:$route.params.id
            }
        }
    },
    {
        name: 'changePassword',
        path: '/changePassword',
        component: () => import('../pages/ChangePassword')
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
    }

];
const router = createRouter({
    history: createWebHistory(), 
    routes
})
 
export default router