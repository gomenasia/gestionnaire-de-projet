(() => {
    const ticketList = document.querySelector(".ticket-list")
    if (!ticketList) {
        return
    }

    const isAuthenticated = document.querySelector(".form-message") !== null

    const socket = io({
        transports: ["websocket", "polling"]
    })

    // Ouvrir/fermer les discussions
    document.querySelectorAll(".btn-repondre").forEach(btn => {
        btn.addEventListener("click", () => {
            const channelId = btn.dataset.channelId
            const panel = document.querySelector(`#discussion-${channelId}`)
            if (!panel) {
                return
            }

            panel.classList.toggle("collapsed")

            if (!panel.classList.contains("collapsed")) {
                socket.emit("join", { channel_id: Number(channelId) })
            }
        })
    })

    // Envoi d'un message
    document.querySelectorAll(".form-message").forEach(form => {
        form.addEventListener("submit", (e) => {
            e.preventDefault()
            const channelId = form.dataset.channelId
            const input = form.querySelector("input[name='content']")

            if (!input) {
                return
            }

            const content = input.value.trim()
            if (!content) {
                return
            }

            socket.emit("send_message", {
                content,
                channel_id: Number(channelId)
            })
            input.value = ""
        })
    })

    // Réception d'un nouveau message
    socket.on("new_message", (msg) => {
        const panel = document.querySelector(`#discussion-${msg.channel_id}`)
        if (!panel) {
            return
        }

        const p = document.createElement("p")
        p.innerHTML = `<strong>${msg.author}</strong> : ${msg.content}`

        const form = panel.querySelector("form")
        if (form) {
            form.before(p)
            return
        }

        const notice = panel.querySelector(".message.warning")
        if (notice) {
            notice.before(p)
            return
        }

        panel.appendChild(p)
    })

    // Si non connecté, on n'envoie jamais de message, mais on laisse l'affichage en temps réel.
    if (!isAuthenticated) {
        return
    }
})()
