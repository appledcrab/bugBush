<template>
  <h1 class="text-dark text-3xl font-bold" > 🐞 Add Bug 🐞</h1>
  <div class=" flex flex-row justify-center p-4 ">
    
    <form @submit.prevent="submitBug" class="bg-light p-4 rounded-md shadow mb-6 flex flex-col gap-4 w-full min-w-sm max-w-4xl border-3 border-dashed border-dark">
      <legend class="font-semibold text-dark">Select Bug Emoji:</legend>
        <div class="flex p-4 flex-row gap-10 justify-center text-3xl border border-primary rounded">
        <label class="cursor-pointer flex flex-col items-center">
          <input type="radio" name="test" value="bug" class="hidden peer" />
          <p class="transition peer-checked:border rounded p-1 peer-checked:scale-175 peer-checked:border-dark">🐛</p>
        </label>

        <label class="cursor-pointer flex flex-col items-center">
          <input type="radio" name="test" value="ant" class="hidden peer" />
          <p class="transition peer-checked:border rounded p-1 peer-checked:scale-175 peer-checked:border-dark">🐜</p>
        </label>

        <label class="cursor-pointer flex flex-col items-center">
          <input type="radio" name="test" value="worm" class="hidden peer" />
          <p class="transition peer-checked:border rounded p-1 peer-checked:scale-175 peer-checked:border-dark">🪱</p>
        </label>

        <label class="cursor-pointer flex flex-col items-center">
          <input type="radio" name="test" value="ladybug" class="hidden peer" />
          <p class="transition peer-checked:border rounded p-1 peer-checked:scale-175 peer-checked:border-dark">🐞</p>
        </label>

        <label class="cursor-pointer flex flex-col items-center">
          <input type="radio" name="test" value="beetle" class="hidden peer" />
          <p class="transition peer-checked:border rounded p-1 peer-checked:scale-175 peer-checked:border-dark">🪲</p>
        </label>
      </div>


      <legend class="font-semibold text-dark">Input Bug Name:</legend>
      <input v-model="title" type="text" placeholder="Bug title" required class="text-xl text-dark font-medium text-center p-2 border border-primary rounded" />
      <legend class="font-semibold text-dark">Input Bug Description:</legend>
      <textarea v-model="description" rows="4" placeholder="Bug description" class="text-xl p-2 border-dark border border-primary rounded"></textarea>
      
      
      <legend class="font-semibold text-dark">Severity:</legend>
      <div class="flex p-4 flex-row gap-10 justify-center text-3xl border border-primary rounded">
          
          <label><input type="radio" value="Low" v-model="severity" class="hidden peer" /> 
            <p class="transition peer-checked:border rounded p-1 peer-checked:scale-175 peer-checked:border-dark">🟢</p>
          </label>
          <label><input type="radio" value="Medium" v-model="severity" class="hidden peer" />
            <p class="transition peer-checked:border rounded p-1 peer-checked:scale-175 peer-checked:border-dark">🟠</p>
             </label>
          <label><input type="radio" value="High" v-model="severity" class="hidden peer" />
            <p class="transition peer-checked:border rounded p-1 peer-checked:scale-175 peer-checked:border-dark">🔴</p>
            </label>
        </div>
      
        <legend class="font-semibold text-dark">Status:</legend>
      <div class="flex p-4 flex-row gap-10 justify-center text-xl border border-primary rounded">
        
        <label><input type="radio" value="Open" v-model="status" /> Open</label>
        <label><input type="radio" value="Closed" v-model="status" /> Closed</label>
      </div>
      <button type="submit" class="bg-dark text-white py-2 px-4 rounded hover:bg-green-800 hover:cursor-pointer">Add Bug</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['bug-added'])

const title = ref('')
const description = ref('')
const severity = ref('Medium')
const status = ref('Open')

const submitBug = async () => {
  await fetch('/api/bugs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: title.value,
      description: description.value,
      severity: severity.value,
      status: status.value
    })
  })

  // Clear form
  title.value = ''
  description.value = ''
  severity.value = 'Medium'
  status.value = 'Open'

  emit('bug-added')
}
</script>
