// script

const form = document.getElementById('bug-form')

// on change for the closed checkbox
const status_radios = document.querySelectorAll(".status");
const solution_fieldset = document.querySelector('.optional_solution');



// the function updates the solution fieldset visibility changes
function updateSolutionVisibility() {
    const checked = document.querySelector('input[name="status"][value="Closed"]:checked');
    // console.log(checked);
    solution_fieldset.style.display = checked ? 'block' : 'none';
}

status_radios.forEach(radio => {
    radio.addEventListener('change', updateSolutionVisibility);
});

// updating on load
updateSolutionVisibility();

// ---------------
// doing the bug tags. but its vanilla.
tags = [];
const addTagBtn = document.querySelector(".tag-btn");

addTagBtn.addEventListener('click', () =>{
    // on click, adding the tag in the input to the tags section 
    const tagsSection = document.getElementById("tags-section");
    const tagText = document.getElementById("tag-text");
    // console.log()
    const text = tagText.value.trim()
    if (text !== '' && !tags.includes(text)){
        const newTag = document.createElement('p');
        
        newTag.classList.add("tag")
        tags.push(text)
        newTag.innerText = text;
        newTag.addEventListener('click', () =>{
            // removing it from the list and from the document
            newTag.remove();
            tags.splice(tags.indexOf(newTag.innerText));
        })

        // now add it to the document
        tagsSection.appendChild(newTag);
        


    }else{
        alert("Please enter unique text for the tag.")
    }
    tagText.value='';
    // console.log(tags) //testing for printing the tags array
})


// random bug being added before each bug 
function randBug(){
    bugSelection = ['🐝','🐞','🐛','🐜','🪱'];
    const randNum = Math.floor(Math.random()* bugSelection.length);
    // console.log(randNum);
    return bugSelection[randNum];
}

// loadings bugs from the sqlite and putting it on a basic list in html
const list = document.getElementById('bug-list');

async function loadBugs() {
    const res = await fetch('/api/bugs')
    const bugs = await res.json();
    console.log(bugs)
    list.innerHTML = '';
    bugs.forEach(bug => {
        const li = document.createElement('li');
        li.innerHTML = `
        <h2>${randBug()} ${bug.title} </h2> (${bug.status}, ${bug.severity})
        <button class="edit-btn" data-id="${bug.id}">Edit</button>
        <div class="bug-details"> 
            <h4>Description</h4>
            <p>${bug.description}</p> 
            <h4>Solution</h4>
            <p>${bug.solution || "Not resolved yet"}</p>
        </div>`;
        

        list.appendChild(li);
    });
}
list.addEventListener('click', (e) => {
  if (e.target.classList.contains('edit-btn')) {
    const bugId = e.target.dataset.id;
    console.log(bugId)
    const bugItem = e.target.closest('li');
    toggleEditMode(bugItem, bugId);
  }
});

function toggleEditMode(bugItem, bugId) {
  // Replace static text with input fields
  const bugDetails = bugItem.querySelector('.bug-details');
  bugDetails.innerHTML = `
    <form class="edit-form" data-id="${bugId}">
      <label>Title: <input type="text" name="title" value="${bugItem.querySelector('h2').textContent}"></label>
      <label>Status: 
        <select name="status">
          <option value="open">Open</option>
          <option value="closed">Closed</option>
        </select>
      </label>
      <label>Description: <textarea name="description">${bugItem.querySelector('p:nth-of-type(1)').textContent}</textarea></label>
      <label>Solution: <textarea name="solution">${bugItem.querySelector('p:nth-of-type(2)').textContent}</textarea></label>
      <button type="submit">Save</button>
    </form>
  `;
}

// on submitting a bug with the form, adding it to the db

form.addEventListener('submit', async (e) => {

    
    const title = document.getElementById('title').value; 
    const description = document.getElementById('description').value;
    const severLvl = document.querySelector('input[name="severity"]:checked').value; 
    const status = document.querySelector('input[name="status"]:checked').value; 
    const solution = document.getElementById('solution').value;
    
   

    try {
        const response = await fetch('/api/bugs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                title, 
                description,
                severity: severLvl, 
                status,
                solution
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        // result will have the bug id which can be used to add tags tied to this bug in the tags table (make seperate function)
        console.log('Success:', result);
        loadBugs(); 
        
    } catch(error) {
        console.error('Fetch error:', error);
        alert('Failed to submit bug. See console for details.');
    }

    title.value = '';
    description.value = '';


});
loadBugs();

