import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import IndexEdit from '../views/IndexEdit.vue'
import UploadFileTest from '../views/UploadFileTest'
import ResourceEdit from '../views/ResourceEdit'
import QuestionEdit from '../views/QuestionEdit'
import NoticeEdit from '../views/NoticeEdit'
import IssueEdit from '../views/IssueEdit'
import Test from '../views/Test'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: IndexEdit
  },
  {
    path: '/resourceUpload',
    name: 'upload',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: UploadFileTest
  },
  {
    path: '/resourceNew',
    name: 'ResourceEdit',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: ResourceEdit
  },
  {
    path: '/questionNnew',
    name: 'QuestionEdit',
    component: QuestionEdit
  },
  {
    path: '/noticeNew',
    name: 'NoticeEdit',
    component: NoticeEdit
  },
  {
    path: '/issueNew',
    name: 'IssueEdit',
    component: IssueEdit
  },
  {
    path: '/test',
    name: 'Test',
    component: Test
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
