document.addEventListener("DOMContentLoaded", async () => {
    const account_id = localStorage.getItem("account_id");

    if (!account_id) {
        document.getElementById("charList").innerText =
            "You must log in first.";
        return;
    }

    const data = await apiGet(`/characters/list/${account_id}`);

    if (!data.characters || data.characters.length === 0) {
        document.getElementById("charList").innerText =
            "No characters found.";
        return;
    }

    // ---------------------------------------------------------
    // BUILD CHARACTER CARDS (UPDATED TEMPLATE)
    // ---------------------------------------------------------
    const list = data.characters
        .map(c => `
            <div class="character-card" data-id="${c.CharacterID}">
                <h2>${c.Name}</h2>

                <div class="character-info">
                    Level: ${c.Level}<br>
                    Race ID: ${c.RaceID}<br>
                    Class ID: ${c.ClassID}
                </div>

                <div class="card-buttons">
                    <a href="/character-sheet?id=${c.CharacterID}" class="card-btn open-btn">Open</a>
                    <button class="card-btn delete-btn" data-id="${c.CharacterID}">Delete</button>
                </div>
            </div>
        `)
        .join("");

    document.getElementById("charList").innerHTML = list;
});


// ---------------------------------------------------------
// CREATE NEW CHARACTER POPUP LOGIC
// ---------------------------------------------------------

document.getElementById("createCharacterButton").addEventListener("click", () => {
    document.getElementById("createCharacterOverlay").style.display = "flex";
});

document.getElementById("createCharacterCancel").addEventListener("click", () => {
    document.getElementById("createCharacterOverlay").style.display = "none";
});

document.getElementById("createCharacterConfirm").addEventListener("click", () => {
    const name = document.getElementById("charNameInput").value.trim();
    const charClass = document.getElementById("charClassSelect").value;
    const race = document.getElementById("charRaceSelect").value;
    const background = document.getElementById("charBackgroundSelect").value;

    if (!name || !charClass || !race || !background) {
        alert("Please fill out all fields.");
        return;
    }

    console.log("New Character:", { name, charClass, race, background });

    document.getElementById("createCharacterOverlay").style.display = "none";

    window.location.href = "/character-creation";
});


// ---------------------------------------------------------
// DELETE CHARACTER LOGIC
// ---------------------------------------------------------

document.addEventListener("click", async (e) => {
    if (e.target.classList.contains("delete-btn")) {
        e.stopPropagation();

        const charId = e.target.dataset.id;

        const confirmDelete = confirm(
            "Are you sure you want to delete this character? This cannot be undone."
        );

        if (!confirmDelete) return;

        try {
            const result = await apiRequest(`/characters/${charId}/delete`, "DELETE");

            if (result.success) {
                const card = document.querySelector(`.character-card[data-id="${charId}"]`);
                if (card) card.remove();
            }
        } catch (err) {
            console.error("Delete failed:", err);
            alert("Failed to delete character.");
        }
    }
});