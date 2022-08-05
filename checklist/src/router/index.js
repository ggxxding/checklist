import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Hello from '@/components/Hello'
import testt from '@/components/testt'
import error from '@/components/error'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/ttest',
      name: 'test',
      component: testt
    },
    {
      path: '/error',
      name: 'error',
      component: error
    },
  ],
  mode: 'history'
})
