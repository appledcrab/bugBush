// script

const form = document.getElementById('bug-form')

// on change for the closed checkbox
const status_radios = document.querySelectorAll(".status");
const solution_fieldset = document.querySelector('.optional_solution');



// the function updates the solution fieldset visibility changes
function updateSolutionVisibility() {
    const checked = document.querySelector('input[name="status"][value="closed"]:checked');
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
async function loadBugs() {
    const res = await fetch('/api/bugs')
    const bugs = await res.json();
    const list = document.getElementById('bug-list');
    console.log(bugs)
    list.innerHTML = '';
    bugs.forEach(bug => {
        const li = document.createElement('li');
        li.textContent = `${randBug()} ${bug.title} - ${bug.description} (${bug.status}, ${bug.severity})`;
        list.appendChild(li);
    });
}

// on submitting a bug with the form, adding it to the db

form.addEventListener('submit', async (e) => {

    
    const title = document.getElementById('title').value; 
    const description = document.getElementById('description').value;
    const severLvl = document.querySelector('input[name="severity"]:checked').value; 
    const status = document.querySelector('input[name="status"]:checked').value; 
    
   

    try {
        const response = await fetch('/api/bugs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                title, 
                description,
                severity: severLvl, 
                status
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
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

