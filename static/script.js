// script

const form = document.getElementById('bug-form')

// on change for the closed checkbox
const status_radios = document.querySelectorAll(".status");
const solution_fieldset = document.querySelector('.optional_solution');

// the function updates the solution fieldset visibility changes
function updateSolutionVisibility(solution_element, edit = false) {
  let checked;
  if (edit) {
    checked = document.querySelector('input[name="edit-status"][value="Closed"]:checked');
  } else {
    checked = document.querySelector('input[name="status"][value="Closed"]:checked');
  }
  solution_element.style.display = checked ? 'block' : 'none';
}

status_radios.forEach(radio => {
    radio.addEventListener('change', () => updateSolutionVisibility(solution_fieldset));
});

// updating on load
updateSolutionVisibility(solution_fieldset);

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
            tags.splice(tags.indexOf(newTag.innerText), 1);
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
        <div class="bug-details">
        <h2>${randBug()} ${bug.title} </h2> (${bug.status}, ${bug.severity})
        <button class="edit-btn" data-id="${bug.id}">Edit</button>
        <div> 
            <h4>Description</h4>
            <p>${bug.description}</p> 
            <h4>Solution</h4>
            <p>${bug.solution || "Not resolved yet"}</p>
        </div>
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
  const bugDetails = bugItem.querySelector('.bug-details');
  const currentSolution = bugItem.querySelector('p:nth-of-type(2)').textContent;
  const isClosed = bugItem.textContent.includes('Closed');
  
  bugDetails.innerHTML = `
    <form class="bug-form" data-id="${bugId}">
      <fieldset>
        <legend>Bug name:</legend>
        <input class="edit_title" type="text" name="title" value="${bugItem.querySelector('h2').textContent.replace(/^[^\w]*/, '').trim()}" />
      </fieldset>
      
      <fieldset>
        <legend>Bug Description:</legend>
        <textarea name="description">${bugItem.querySelector('p:nth-of-type(1)').textContent}</textarea>
      </fieldset>
      
      <fieldset>
        <legend>Severity of Bug:</legend>
        <div class="severity-group">
          <label><input class="radio" type="radio" name="severity" value="Low" /> Low</label>
          <label><input class="radio" type="radio" name="severity" value="Medium" checked /> Medium</label>
          <label><input class="radio" type="radio" name="severity" value="High" /> High</label>
        </div>
      </fieldset>

      <fieldset>
        <legend>Status of Bug:</legend>
        <div class="status-group">
          <label><input class="edit-status" type="radio" name="edit-status" value="Open" ${!isClosed ? 'checked' : ''} /> Open</label>
          <label><input class="edit-status" type="radio" name="edit-status" value="Closed" ${isClosed ? 'checked' : ''} /> Closed</label>
        </div>
      </fieldset>

      <fieldset id="edit_solution">
        <legend>Solution:</legend>
        <textarea name="solution">${currentSolution === "Not resolved yet" ? "" : currentSolution}</textarea>
      </fieldset>
      
      <button class="edit-sbmt" type="submit">Save</button>
    </form>
  `;
  
  // Set up the edit form solution visibility
  const edit_solution = bugDetails.querySelector("#edit_solution");
  const edit_status_radios = bugDetails.querySelectorAll(".edit-status");
  
  // Update visibility initially
  updateSolutionVisibility(edit_solution, true);
  
  // Set up event listeners for edit form radios
  edit_status_radios.forEach(radio => {
    radio.addEventListener('change', () => updateSolutionVisibility(edit_solution, true));
  });

  // Set up form submission
  const editForm = bugDetails.querySelector('.bug-form');
  editForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    await editModeHelper(bugId);
  });
}

async function editModeHelper(bugId){
    const form = document.querySelector(`.bug-form[data-id="${bugId}"]`);
    const title = form.querySelector('input[name="title"]').value; 
    const description = form.querySelector('textarea[name="description"]').value;
    const severLvl = form.querySelector('input[name="severity"]:checked').value; 
    const status = form.querySelector('input[name="edit-status"]:checked').value; 
    const solution = form.querySelector('textarea[name="solution"]').value;

    try {
        const response = await fetch(`/api/bugs/${bugId}`, {
            method: 'PUT',
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

        loadBugs();
    } catch(error) {
        console.error('Error updating bug:', error);
    }
}

// on submitting a bug with the form, adding it to the db
form.addEventListener('submit', async (e) => {
    e.preventDefault();
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
        console.log('Success:', result);
        loadBugs(); 
        
        // Reset form
        form.reset();
        document.getElementById('tags-section').innerHTML = '';
        tags = [];
    } catch(error) {
        console.error('Fetch error:', error);
        alert('Failed to submit bug. See console for details.');
    }
});

loadBugs();