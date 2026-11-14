import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/',
    component: () => import('../layout/MainLayout.vue'),
    redirect: '/home',
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('../views/Home.vue'),
        meta: { title: '选座预约' }
      },
      {
        path: 'my',
        name: 'MyReservations',
        component: () => import('../views/MyReservations.vue'),
        meta: { title: '我的预约' }
      },
      {
        path: 'notices',
        name: 'Notices',
        component: () => import('../views/Notices.vue'),
        meta: { title: '馆内公告' }
      },
      {
        path: 'notices/:id',
        name: 'NoticeDetail',
        component: () => import('../views/NoticeDetail.vue'),
        meta: { title: '公告详情' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/home'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 未登录时统一跳转到登录页，已登录时不再重复进入登录页
router.beforeEach((to) => {
  const userStore = useUserStore()
  document.title = to.meta.title
    ? `${to.meta.title} - 校园图书馆座位预约`
    : '校园图书馆座位预约'

  if (to.path === '/login') {
    return userStore.isLoggedIn ? '/home' : true
  }
  return userStore.isLoggedIn ? true : '/login'
})

export default router
