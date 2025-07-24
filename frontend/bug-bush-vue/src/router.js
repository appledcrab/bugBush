import { createMemoryHistory, createRouter } from 'vue-router'

import mainPage from './components/Pages/MainPage.vue'
import addBugPage from './components/Pages/AddBug.vue'

const routes = [
  { path: '/', component: mainPage },
  { path: '/addbug', component: addBugPage },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router