import { createMemoryHistory, createRouter } from 'vue-router'

import mainPage from './components/Pages/MainPage.vue'
import addBugPage from './components/Pages/AddBug.vue'
import editBugPage from './components/Pages/EditBug.vue'

const routes = [
  { path: '/', component: mainPage },
  { path: '/addbug', component: addBugPage },
  { path: '/editBug/:id', component: editBugPage}
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router