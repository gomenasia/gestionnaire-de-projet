document.addEventListener('DOMContentLoaded', () => {
    //garder les details ouvert
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

    const inputElems = document.querySelectorAll('input[type="checkbox"]');
    //change le status des taches
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
                if(data.success) {
                    location.reload();
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
});
