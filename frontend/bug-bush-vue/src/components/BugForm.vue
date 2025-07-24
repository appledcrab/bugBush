<template >
  <h1 class="text-dark text-3xl font-bold" > Add Bug </h1>
  <div class="flex flex-row justify-center p-4 ">
    
    <form @submit.prevent="submitBug" class="z-1 bg-light p-4 rounded-md shadow-2xl mb-6 flex flex-col gap-4 w-full min-w-sm max-w-4xl border-3 border-dashed border-accent">
      <legend class="font-semibold text-dark">Select Bug Emoji:</legend>
        <div class="flex p-4 flex-row gap-10 justify-center text-3xl border border-primary rounded">
        <label class="emoji-option cursor-pointer flex flex-col items-center">
          <input type="radio" name="emoji" value="🐛" class="hidden peer" v-model="emoji"/>
          <p>🐛</p>
        </label>

        <label class="emoji-option cursor-pointer flex flex-col items-center">
          <input type="radio" name="emoji" value="🐜" class="hidden peer" v-model="emoji"/>
          <p>🐜</p>
        </label>

        <label class="emoji-option cursor-pointer flex flex-col items-center">
          <input type="radio" name="emoji" value="🪱" class="hidden peer" v-model="emoji"/>
          <p>🪱</p>
        </label>

        <label class="emoji-option cursor-pointer flex flex-col items-center">
          <input type="radio" name="emoji" value="🐞" class="hidden peer" v-model="emoji" />
          <p>🐞</p>
        </label>

        <label class="emoji-option cursor-pointer flex flex-col items-center">
          <input type="radio" name="emoji" value="🪲" class="hidden peer" v-model="emoji"/>
          <p>🪲</p>
        </label>
      </div>


      <legend class="font-semibold text-dark">Input Bug Name:</legend>
      <input v-model="title" type="text" placeholder="Bug title" required class="text-xl text-dark font-medium text-center p-2 border border-primary rounded" />
      <legend class="font-semibold text-dark">Input Tags</legend>
      <div class="border border-primary rounded p-3 flex flex-row gap-10">
        <div>
          <input ref="tagText" class="section-item tag-text border border-primary rounded p-2 m-2" type="text" placeholder="ex. Java" autocomplete="off" />
              <button type="button" class="bg-accent text-dark section-item tag-btn hover:cursor-pointer hover:bg-dark hover:text-accent p-4 rounded-full" @click="addTag">Add tag</button>
        </div>
        <div ref="tagsSection" class="flex flex-wrap content-center gap-4">

        </div>
      </div>
      <legend class="font-semibold text-dark">Input Bug Description:</legend>
      <textarea v-model="description" rows="4" placeholder="Ex. When depositing using the mobile app, double the money is shown in the bank account." class="text-xl p-2 border-dark border border-primary rounded"></textarea>
      
      
      <legend class=" font-semibold text-dark">Severity:</legend>
      <div class="flex p-4 flex-row gap-10 justify-center text-3xl border border-primary rounded">
          
          <label class="emoji-option"><input type="radio" value="Low" v-model="severity" class="hidden peer" /> 
            <p >🟢</p>
          </label>
          <label class="emoji-option"><input type="radio" value="Medium" v-model="severity" class="hidden peer" />
            <p >🟠</p>
             </label>
          <label class="emoji-option"><input type="radio" value="High" v-model="severity" class="hidden peer" />
            <p >🔴</p>
            </label>
        </div>
      
        <legend class="font-semibold text-dark">Status:</legend>
      <div class="flex p-4 flex-row gap-10 justify-center text-xl border border-primary rounded">
        
        <label><input @change="changeSolutionVisibility" type="radio" value="Open" v-model="status" /> Open</label>
        <label><input @change="changeSolutionVisibility" type="radio" value="Closed" v-model="status" /> Closed</label>
      </div>
      <div v-show="isSolutionVisible" ref="solutionSection" id="solution-section" class="flex flex-col">
          <legend class="font-semibold text-dark">Solution:</legend>
          <textarea v-model="solution" rows="4" placeholder="Ex. Variable added to the account in two different spots. Corrected the code to only add in one spot." class="text-xl p-2 border-dark border border-primary rounded"></textarea>
      </div>
      <button type="submit" id="tag-btn" class="bg-accent text-dark py-2 px-4 rounded hover:bg-primary hover:cursor-pointer">Add Bug</button>
    </form>
  </div>
  <div class="bush-background"></div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['bug-added'])


// Variables 
const title = ref('')
const description = ref('')
const severity = ref('Medium')
const status = ref('Open')
const emoji = ref('🐞') 
const solution = ref('')
const isSolutionVisible = ref(false)

let tags = []
const tagText = ref('')
const tagsSection = ref('')
const solutionSection = ref('')


// adds tag to the tagsSection and adds event listener that will KILL the tag if clicked.
// Addtionally, makes sure that there is only unique tags added
// Could change it so it uses a better way of telling them instead of just using default alert.
const addTag = () => {
  const text = tagText.value.value.trim()
  if (text !== '' && !tags.includes(text)) {
    const newTag = document.createElement('p')
    newTag.classList.add('tag')
    tags.push(text)
    newTag.innerText = text
    newTag.addEventListener('click', () => {
      newTag.remove()
      tags.splice(tags.indexOf(newTag.innerText), 1)
    })
    console.log("appending tag")
    tagsSection.value.appendChild(newTag)
  } else {
    alert('Please enter unique text for the tag.')
  }
  tagText.value.value = ''
}

// Changes based on the form status.
// closed shows it.
const changeSolutionVisibility = (event) => {
  isSolutionVisible.value = event.target.value === 'Closed'
}

const submitBug = async () => {
  await fetch('/api/bugs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: title.value,
      emoji: emoji.value,
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
  emoji.value = '🐞'
  tags = []

  emit('bug-added')
}


</script>

