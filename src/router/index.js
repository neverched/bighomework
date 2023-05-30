import {createRouter, createWebHistory} from 'vue-router'
const routes = [
    {
        name: 'resource',
        path: '/resource',
        component: () => import('../pages/ResourceList'),
    },
    {
        name: 'question',
        path: '/question',
        component: () => import('../pages/QuestionList')
    },
    {
        name: 'exercise',
        path: '/exercise',
        component: () => import('../pages/ExerciseList')
    },
    {
        name: 'notice',
        path: '/notice',
        component: () => import('../pages/NoticeList')
    },
    {
        name: 'detail',
        path:'/detail/:id',
        component: () => import('../pages/Detail'),
        props($route){
            return {
                id:$route.params.id
            }
        }
    },

];
const router = createRouter({
    history: createWebHistory(), 
    routes
})
 
export default router