document.addEventListener('DOMContentLoaded', () => {
    const dialog = document.getElementById('task-dialog');
    let currentItemId = null;

    document.querySelectorAll('.add-task-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            currentItemId = btn.dataset.itemId;
            dialog.showModal();
        });
    });

    document.getElementById('modal-cancel-btn').addEventListener('click', () => {
        dialog.close();
    });

    dialog.addEventListener('click', (e) => {
        if (e.target === dialog) dialog.close();
    });

    document.getElementById('modal-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const response = await fetch(`/api/task?parent_id=${currentItemId}`, {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            dialog.close();
            location.reload();
        }
    });
});
