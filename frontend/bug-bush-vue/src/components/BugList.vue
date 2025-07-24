<template>
  <ul class="space-y-2">
    <li v-for="bug in bugs" :key="bug.id" class="bg-white border p-3 rounded shadow">
      <div>
        <h2 class="font-bold">{{ bug.emoji }} {{ bug.title }} </h2>
        <p class="text-sm text-gray-700">{{ bug.description }}</p>
        <p class="text-sm mt-1">
          <span class="font-semibold">Status:</span> {{ bug.status }} |
          <span class="font-semibold">Severity:</span> {{ bug.severity }}
        </p>
      </div>
      <div>
        <!-- Edit and quick delete button -->
         <!-- edit will go to page very similar to add bug button that will also have option of deletion -->
        <!-- delete should probably come with a confirm delete and a checkbox to never ask again -> add to todo list -->
        <p @click="deleteBug(bug.id)" class="text-red-500 font-semibold hover:cursor-pointer">DELETE</p>
      </div>
    </li>
  </ul>
</template>

<script setup>

import {ref,onMounted, computed} from 'vue'

const bugs = ref([]) //learnt: makes variable reactive and updating
const loadBugs = async () =>{
  const res = await fetch('/api/bugs')
  console.log(res)
  bugs.value = await res.json()
}

const deleteBug = async(bugId) =>{
  const res = await fetch(`/api/bugs/${bugId}`,{
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' }
  }

  )

  // Learnt: FLask needs a valid HTTP response. every route handler in flask needs to return a response
   if (res.ok) {
    bugs.value = bugs.value.filter(bug => bug.id !== bugId)
  } else {
    console.error('Failed to delete bug:', res.statusText)
  }
}

onMounted(loadBugs)
</script>
