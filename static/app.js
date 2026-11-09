const API = "";

let accessToken = null;


// Display messages
function showMessage(message) {
    document.getElementById("message").textContent = message;
}


// Register
async function register() {

    const username = document.getElementById("reg-username").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;

    const response = await fetch(`${API}/auth/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username,
            email,
            password
        })
    });

    const data = await response.json();

    if (!response.ok) {
        showMessage(data.detail || "Registration failed");
        return;
    }

    showMessage("Registration successful. Please log in.");
}


// Login
async function login() {

    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email,
            password
        })
    });

    const data = await response.json();

    if (!response.ok) {
        showMessage(data.detail || "Login failed");
        return;
    }

    accessToken = data.access_token;

    document.getElementById("auth-section").hidden = true;
    document.getElementById("notes-section").hidden = false;

    showMessage("Login successful!");

    loadNotes();
}


// Common authenticated request headers
function authHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${accessToken}`
    };
}


// Load notes
async function loadNotes() {

    const response = await fetch(`${API}/notes/`, {
        headers: authHeaders()
    });

    const data = await response.json();

    if (!response.ok) {
        showMessage(data.detail || "Could not load notes");
        return;
    }

    const notesList = document.getElementById("notes-list");

    notesList.replaceChildren();

    data.forEach(note => {

        const card = document.createElement("div");
        card.className = "note";

        const title = document.createElement("h3");
        title.textContent = note.title;

        const content = document.createElement("p");
        content.textContent = note.content;

        const deleteButton = document.createElement("button");
        deleteButton.className = "delete-btn";
        deleteButton.textContent = "Delete";
        deleteButton.addEventListener("click", () => deleteNote(note.id));

        card.append(title, content, deleteButton);
        notesList.appendChild(card);
    });
}


// Create note
async function createNote() {

    const title = document.getElementById("note-title").value;
    const content = document.getElementById("note-content").value;

    const response = await fetch(`${API}/notes/`, {
        method: "POST",
        headers: authHeaders(),
        body: JSON.stringify({
            title,
            content
        })
    });

    const data = await response.json();

    if (!response.ok) {
        showMessage(data.detail || "Could not create note");
        return;
    }

    document.getElementById("note-title").value = "";
    document.getElementById("note-content").value = "";

    showMessage("Note created!");

    loadNotes();
}


// Delete note
async function deleteNote(noteId) {

    const response = await fetch(`${API}/notes/${noteId}`, {
        method: "DELETE",
        headers: authHeaders()
    });

    if (!response.ok) {
        const data = await response.json();
        showMessage(data.detail || "Could not delete note");
        return;
    }

    showMessage("Note deleted!");

    loadNotes();
}


// Logout
function logout() {

    accessToken = null;

    document.getElementById("auth-section").hidden = false;
    document.getElementById("notes-section").hidden = true;

    document.getElementById("notes-list").replaceChildren();

    showMessage("Logged out");
}