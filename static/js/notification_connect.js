
(() => {
    // Charger socket.io depuis le CDN ou depuis Flask-SocketIO
    const socket = typeof window.io === "function"
        ? window.io({ transports: ["websocket", "polling"] })
        : null

    function showNotificationToast(message, type) {  //TODO ============= afiche les notification en pop up=============
        const toast = document.createElement("div");
        toast.className = `toast toast--${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 4000);
    }

    function updateNotificationBadge() {             // ============= compte le nombre de notif ============
        const badge = document.querySelector(".notif-badge");
        if (badge) {
            badge.textContent = parseInt(badge.textContent || 0) + 1;
            badge.style.display = "inline";
        }
    }

    const content_notifications = document.querySelector(".notification");
    const list_notification = document.querySelector(".notifications");

    if (content_notifications) {                          // ============= afiche la div notification =============
        content_notifications.addEventListener("click", () => {
            list_notification.classList.toggle("open")
            if (list_notification && list_notification.classList.contains("open")) {
                fetch(`/api/session`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        return response.json();
                    })
                    .then((data) => {
                        if (data.success) {
                            update_notif_display(data.user_id);
                        }
                    })
                    .catch((error) => {
                        console.error('Erreur lors de la récupération de la session:', error);
                    });
            }
        });
    }

    function update_notif_display(user_id) {         // ============= acualise la liste de notif =============
        fetch(`/api/notification/${user_id}`)
            .then(res => res.json())
            .then(notifs => {
            notifs.forEach(notif => {
                // Convertir UTC → heure locale du navigateur
                const date = new Date(notif.created_at);
                const local_time = new Intl.DateTimeFormat("fr-FR", {
                    dateStyle: "short",
                    timeStyle: "short",
                    timeZone: "Europe/Paris"
                }).format(date);

                list_notification.innerHTML += `
                <li class="notif-item ${notif.is_read ? '' : 'unread'}">
                    <p>${notif.message}</p>
                    <small>${local_time}</small>
                </li>
                `;
            });
        }); 
    }


    if (!socket) {
        // Pas de transport temps réel disponible: on garde le comportement UI (toggle) uniquement.
        return
    }

    socket.on("connect", () => {
        console.log("WebSocket connecté");
    });

    // Écouter les nouvelles notifications
    socket.on("new_notification", (data) => {
        showNotificationToast(data.message, data.type);
        updateNotificationBadge();  // incrémenter le compteur dans le menu

        fetch(`/api/session`)
            .then(response => response.json())
            .then((data) => {
                if(data.success){
                    update_notif_display(data.user_id)
                }
            })
    });
})()