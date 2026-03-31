import { registerUser, loginUser } from "./api.js";

console.log("LOGIN JS LOADED");

// -----------------------------------------------------
// LOGIN
// -----------------------------------------------------
const loginBtn = document.getElementById("loginBtn");
if (loginBtn) {
    loginBtn.addEventListener("click", async () => {
        const identifier = document.getElementById("identifier").value;
        const password = document.getElementById("password").value;
        const error = document.getElementById("error");

        error.textContent = "";

        try {
            const res = await loginUser(identifier, password);

            localStorage.setItem("user", JSON.stringify(res));

            window.location.href = "/assets/characters.html";
        } catch (err) {
            error.textContent = err.message || "Login failed";
        }
    });
}

// -----------------------------------------------------
// REGISTER
// -----------------------------------------------------
const registerBtn = document.getElementById("registerBtn");
if (registerBtn) {
    registerBtn.addEventListener("click", async () => {
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const error = document.getElementById("error");
        const success = document.getElementById("success");

        error.textContent = "";
        success.textContent = "";

        try {
            const res = await registerUser(username, email, password);

            success.textContent = "Account created! Redirecting...";
            setTimeout(() => {
                window.location.href = "/assets/login.html";
            }, 1000);
        } catch (err) {
            error.textContent = err.message || "Registration failed";
        }
    });
}

// -----------------------------------------------------
// GUEST LOGIN
// -----------------------------------------------------
const guestBtn = document.getElementById("guestBtn");
if (guestBtn) {
    guestBtn.addEventListener("click", () => {
        const guestUser = {
            id: "guest-" + Date.now(),
            username: "Guest",
            email: null,
            guest: true
        };

        localStorage.setItem("user", JSON.stringify(guestUser));

        window.location.href = "/assets/characters.html";
    });
}