// /assets/password_reset.js

import { apiRequest } from "/assets/api.js";

const usernameInput = document.getElementById("username");
const emailInput = document.getElementById("email");
const resetMessage = document.getElementById("resetMessage");
const resetSuccess = document.getElementById("resetSuccess");
const submitUserBtn = document.getElementById("submitUser");
const exitResetBtn = document.getElementById("exitReset");

const overlay = document.getElementById("overlay");
const newPassInput = document.getElementById("newPass");
const confirmPassInput = document.getElementById("confirmPass");
const passMessage = document.getElementById("passMessage");
const passSuccess = document.getElementById("passSuccess");
const submitPassBtn = document.getElementById("submitPass");
const exitSubmenuBtn = document.getElementById("exitSubmenu");

const helpBtn = document.getElementById("helpBtn");
const helpPanel = document.getElementById("helpPanel");

let verifiedUserId = null;


// Verify user using backend route
async function verifyUser(username, email) {
    return await apiRequest("/password/verify", "POST", {
        username,
        email
    });
}


// Update password using backend route
async function updatePassword(userId, newPassword) {
    return await apiRequest(`/password/reset/${userId}`, "POST", {
        password: newPassword
    });
}


// Open submenu after username/email submit
submitUserBtn.addEventListener("click", async () => {
    resetMessage.textContent = "";
    resetSuccess.textContent = "";

    const username = usernameInput.value.trim();
    const email = emailInput.value.trim();

    if (!username || !email) {
        resetMessage.textContent = "Username and Email are required.";
        return;
    }

    try {
        const result = await verifyUser(username, email);

        if (!result || result.success === false) {
            resetMessage.textContent = "No account found with that username and email.";
            return;
        }

        verifiedUserId = result.user_id;

        resetSuccess.textContent = "Account verified. Please enter a new password.";
        overlay.classList.add("open");

    } catch (err) {
        resetMessage.textContent = "Unable to verify account.";
    }
});


// Exit main reset
exitResetBtn.addEventListener("click", () => {
    window.location.href = "/assets/login.html";
});


// Exit submenu
exitSubmenuBtn.addEventListener("click", () => {
    overlay.classList.remove("open");
    passMessage.textContent = "";
    passSuccess.textContent = "";
    newPassInput.value = "";
    confirmPassInput.value = "";
});


// Help panel toggle
helpBtn.addEventListener("click", () => {
    helpPanel.classList.toggle("open");
});


// Password requirement check
function validatePasswordRequirements(password) {
    const missing = [];

    if (password.length < 8) missing.push("at least 8 characters");
    if (!/[0-9]/.test(password)) missing.push("at least one number");
    if (!/[!@#$%^&*()_\-+={}[\]|:;"'<>,.?/`~]/.test(password))
        missing.push("at least one symbol (e.g., # or $)");

    return missing;
}


// Submit new password
submitPassBtn.addEventListener("click", async () => {
    passMessage.textContent = "";
    passSuccess.textContent = "";

    const newPass = newPassInput.value;
    const confirmPass = confirmPassInput.value;

    if (!newPass || !confirmPass) {
        passMessage.textContent = "Both password fields are required.";
        return;
    }

    if (newPass !== confirmPass) {
        passMessage.textContent = "Passwords do not match.";
        return;
    }

    const missing = validatePasswordRequirements(newPass);
    if (missing.length > 0) {
        passMessage.textContent = "Password is missing: " + missing.join(", ") + ".";
        return;
    }

    if (!verifiedUserId) {
        passMessage.textContent = "User verification missing.";
        return;
    }

    try {
        const result = await updatePassword(verifiedUserId, newPass);

        if (!result || result.success === false) {
            passMessage.textContent = "Failed to update password.";
            return;
        }

        passSuccess.textContent = "Password updated successfully. Redirecting to login...";
        setTimeout(() => {
            window.location.href = "/assets/login.html";
        }, 1200);

    } catch (err) {
        passMessage.textContent = "An error occurred while updating password.";
    }
});