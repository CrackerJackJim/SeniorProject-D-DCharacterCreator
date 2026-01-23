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

    const list = data.characters
        .map(c => `<div class="char">${c.Name} (Level ${c.Level})</div>`)
        .join("");

    document.getElementById("charList").innerHTML = list;
});