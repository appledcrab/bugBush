<template>
  <ul class="space-y-2">
    <li v-for="bug in bugs" :key="bug.id" class="bg-white border p-3 rounded shadow">
      <h2 class="font-bold">{{ bug.title }}</h2>
      <p class="text-sm text-gray-700">{{ bug.description }}</p>
      <p class="text-sm mt-1">
        <span class="font-semibold">Status:</span> {{ bug.status }} |
        <span class="font-semibold">Severity:</span> {{ bug.severity }}
      </p>
    </li>
  </ul>
</template>

<script setup>
defineProps({
  bugs: Array
})
</script>
