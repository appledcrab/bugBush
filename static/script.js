// script

const form = document.getElementById('bug-form')

// loadings bugs from the sqlite and putting it on a basic list in html
async function loadBugs() {
    const bugs = await fetch('/api/bugs')
    const list = document.getElementById('bug-list');
    list.innerHTML = '';
    bugs.forEach(bug => {
        const li = document.createElement('li');
        li.textContent = `${bug.title} - ${bug.description} (${bug.status}, ${bug.severity})`;
        list.appendChild(li);
    });
}

// on submitting a bug with the form, adding it to the db

form.addEventListener('submit', async (e) => {
    const title = document.getElementById('title')
    const description = document.getElementById('description').value;
    await fetch('/api/bugs', {
        method:'POST',
        headers: {'Content-Type': 'application/jason'},
        body: JSON.stringify({ 
            title, 
            description,
            status: 'Open',
            severity: 'Medium'
        })
    })
}) 

