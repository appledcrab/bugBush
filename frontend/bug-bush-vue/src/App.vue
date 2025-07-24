<script setup>
// import HelloWorld from './components/HelloWorld.vue'
import {ref,onMounted, computed} from 'vue'
import BugForm from './components/BugForm.vue'
import BugList from './components/BugList.vue'
import Header from './components/Header.vue'

import MainPage from './components/Pages/MainPage.vue'
import AddBug from './components/Pages/AddBug.vue'

const routes = {
  '/': MainPage,
  '/addBug': AddBug
}

// const currentPath = ref(window.location.hash)

// window.addEventListener('hashchange', () => {
//   currentPath.value = window.location.hash
// })

// const currentView = computed(() => {
//   return routes[currentPath.value.slice(1) || '/'] || NotFound
// })

// const bugs = ref([])
// const loadBugs = async () =>{
//   const res = await fetch('/api/bugs')
//   console.log(res)
//   bugs.value = await res.json()
// }

// onMounted(loadBugs)
</script>

<template>
  <Header/>
  <main class=" bg-green-50 min-h-screen -z-1">
    
    <!-- <BugForm @bug-added="loadBugs"/>
    <BugList :bugs="bugs"/> --> 
    <RouterView></RouterView>
  </main>
</template>

<!-- <style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style> -->

