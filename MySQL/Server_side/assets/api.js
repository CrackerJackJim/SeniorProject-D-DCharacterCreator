export const API_BASE = "http://127.0.0.1:8000/api";

export async function apiRequest(endpoint, method = "GET", body = null) {
    const options = {
        method,
        headers: { "Content-Type": "application/json" },
        cache: "no-store"   // FORCE FRESH RESPONSES
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const res = await fetch(`${API_BASE}${endpoint}`, options);

    let data = {};
    try {
        data = await res.json();
    } catch (_) {
        // If response isn't JSON, keep data as empty object
    }

    if (!res.ok) {
        // FastAPI validation errors (422)
        if (Array.isArray(data.detail)) {
            let msg = data.detail[0].msg;

            // Normalize email validation messages
            if (msg.toLowerCase().includes("email")) {
                msg = "Invalid Email Address";
            }

            throw new Error(msg);
        }

        // FastAPI string error
        if (typeof data.detail === "string") {
            let msg = data.detail;

            if (msg.toLowerCase().includes("email")) {
                msg = "Invalid Email Address";
            }

            throw new Error(msg);
        }

        throw new Error("Unknown API error");
    }

    return data;
}

export function registerUser(username, email, password) {
    return apiRequest("/register", "POST", { username, email, password });
}

export function loginUser(identifier, password) {
    return apiRequest("/login", "POST", { identifier, password });
}