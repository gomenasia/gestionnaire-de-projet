const upDateCheckboxes = () =>{
    //change le status des taches
    const inputElems = document.querySelectorAll('input[type="checkbox"]');
    inputElems.forEach(checkboxe => {
        checkboxe.addEventListener("click", async (e) => {
            e.stopPropagation();

            const taskId = checkboxe.dataset.taskId; 
            
            fetch(`/api/task/${taskId}/status`,{
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'},
                body: JSON.stringify({status:checkboxe.checked})
            })
            .then((response) => response.json())
            .then((data)=>{
                console.log(data)
                if(data.success) {
                    const progressBar = document.getElementById(data.parent_id);
                    progressBar.setAttribute("aria-valuenow", data.progress)
                    progressBar.style.setProperty('--progress', data.progress + "%")
                    localStorage.setItem(`progress-${data.parent_id}`,data.progress)

                }else{
                    checkbox.checked = !checkbox.checked;
                }
            })
            .catch((error) =>{
                console.error("Erreur:",error)
                checkbox.checked = !checkbox.checked;
            })
        })
    });
}


//garder les details ouvert
const upDateDetails = ()=>{
    document.querySelectorAll('details').forEach(details => {
    const btn = details.querySelector('.add-task-btn');
    if (!btn) return;
    const id = btn.dataset.itemId;

    // Restaure
    if (localStorage.getItem(`details-${id}`) === 'true') {
        details.open = true;
    }

    // Sauvegarde
    details.addEventListener('toggle', () => {
        localStorage.setItem(`details-${id}`, details.open);
        });
    });
}

const updateProgress = () =>{
    const progressbars = document.querySelectorAll(".progressbar")

    progressbars.forEach(progressBar =>{
        const taks_id= progressBar.getAttribute('id')

        if(localStorage.getItem(`progress-${taks_id}`) !== null){
            const progress = localStorage.getItem(`progress-${taks_id}`)
            progressBar.setAttribute("aria-valuenow", progress)
            progressBar.style.setProperty('--progress', progress + "%")
        }
    })
    
}

//progressBar
const enableProgressbar = () => {
    const progressbars = document.querySelectorAll(".progressbar")
    progressbars.forEach(bar =>{
        bar.setAttribute("role", "progressbar")
        bar.setAttribute("aria-valuenow", 0)
        bar.setAttribute("aria-live", "polite")
    })
}

upDateCheckboxes();
upDateDetails();
enableProgressbar();
updateProgress();




