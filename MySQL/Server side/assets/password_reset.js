import { apiRequest } from "/assets/api.js";

const submitUser = document.getElementById("submitUser");
const exitReset = document.getElementById("exitReset");
const overlay = document.getElementById("overlay");
const submitPass = document.getElementById("submitPass");
const exitSubmenu = document.getElementById("exitSubmenu");

let currentUserId = null;

// STEP 1 — Verify username + email
submitUser.addEventListener("click", async () => {
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const msg = document.getElementById("resetMessage");

    msg.textContent = "";

    if (!username || !email) {
        msg.textContent = "Please enter both username and email.";
        return;
    }

    try {
        const result = await apiRequest("/password/verify", "POST", { username, email });

        if (!result.success) {
            msg.textContent = "Username and email do not match.";
            return;
        }

        // Success → open submenu
        currentUserId = result.user_id;
        overlay.style.display = "flex";

    } catch (err) {
        msg.textContent = "Server error. Please try again.";
    }
});

// STEP 2 — Submit new password
submitPass.addEventListener("click", async () => {
    const newPass = document.getElementById("newPass").value;
    const confirmPass = document.getElementById("confirmPass").value;
    const msg = document.getElementById("passMessage");

    msg.textContent = "";

    if (!newPass || !confirmPass) {
        msg.textContent = "Please fill out both password fields.";
        return;
    }

    if (newPass !== confirmPass) {
        msg.textContent = "Passwords do not match.";
        return;
    }

    // ⭐ NEW: Match registration password rules
    if (newPass.length < 8) {
        msg.textContent = "Password must be at least 8 characters.";
        return;
    }

    try {
        const result = await apiRequest(`/password/reset/${currentUserId}`, "POST", { password: newPass });

        if (result.success) {
            msg.style.color = "darkgreen";
            msg.textContent = "Password changed successfully!";

            setTimeout(() => {
                window.location.href = "/assets/login.html";
            }, 1200);
        }

    } catch (err) {
        msg.textContent = "Server error. Please try again.";
    }
});

// EXIT BUTTONS
exitReset.addEventListener("click", () => {
    window.location.href = "/assets/login.html";
});

exitSubmenu.addEventListener("click", () => {
    overlay.style.display = "none";
});