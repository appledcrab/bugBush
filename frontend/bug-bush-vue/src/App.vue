<script setup>
// import HelloWorld from './components/HelloWorld.vue'
import {ref,onMounted} from 'vue'
import BugForm from './components/BugForm.vue'
import BugList from './components/BugList.vue'
import Header from './components/Header.vue'

const bugs = ref([])
const loadBugs = async () =>{
  const res = await fetch('/api/bugs')
  console.log(res)
  bugs.value = await res.json()
}

onMounted(loadBugs)
</script>

<template>
  <Header/>
  <main class="p-8 bg-green-50 min-h-screen">
    
    <BugForm @bug-added="loadBugs"/>
    <BugList :bugs="bugs"/>
  <!-- <div>
    <a href="https://vite.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div>
  <HelloWorld msg="Vite + Vue" /> -->
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

