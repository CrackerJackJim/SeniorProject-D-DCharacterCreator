export const API_BASE = "http://127.0.0.1:8000/api";

export async function apiRequest(endpoint, method = "GET", body = null) {
    const options = {
        method,
        headers: { "Content-Type": "application/json" }
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const res = await fetch(`${API_BASE}${endpoint}`, options);
    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
        throw new Error(data.detail || "Unknown API error");
    }

    return data;
}

export function registerUser(username, email, password) {
    return apiRequest("/register", "POST", { username, email, password });
}

export function loginUser(identifier, password) {
    return apiRequest("/login", "POST", { identifier, password });
}