const API_BASE = "https://37mjdytez8.execute-api.us-east-1.amazonaws.com/dev";

let currentUser = null;   // { email, user_name }

function showLogin() {
  document.getElementById("login-section").style.display = "block";
  document.getElementById("register-section").style.display = "none";
  document.getElementById("main-section").style.display = "none";
}

function showRegister() {
  document.getElementById("login-section").style.display = "none";
  document.getElementById("register-section").style.display = "block";
}

function showMain() {
  document.getElementById("login-section").style.display = "none";
  document.getElementById("register-section").style.display = "none";
  document.getElementById("main-section").style.display = "block";
  document.getElementById("user-name-display").textContent = currentUser.user_name;
  loadAvailability();
}

async function doLogin() {
  const email = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value;
  const errorBox = document.getElementById("login-error");
  errorBox.style.display = "none";

  const res = await fetch(`${API_BASE}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const data = await res.json();

  if (res.status !== 200) {
    errorBox.textContent = data.error || "Login failed";
    errorBox.style.display = "block";
    return;
  }
  currentUser = { email: data.email, user_name: data.user_name };
  showMain();
}

async function doRegister() {
  const email = document.getElementById("register-email").value.trim();
  const user_name = document.getElementById("register-username").value.trim();
  const password = document.getElementById("register-password").value;
  const errorBox = document.getElementById("register-error");
  errorBox.style.display = "none";

  const res = await fetch(`${API_BASE}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, user_name, password }),
  });
  const data = await res.json();

  if (res.status !== 200) {
    errorBox.textContent = data.error || "Registration failed";
    errorBox.style.display = "block";
    return;
  }
  showLogin();
}

function logout() {
  currentUser = null;
  showLogin();
}

async function loadAvailability() {
  const res = await fetch(`${API_BASE}/availability`);
  const data = await res.json();
  const list = document.getElementById("spaces-list");
  list.innerHTML = "";

  data.spaces.forEach((space) => {
    const row = document.createElement("div");
    row.className = "space-row";
    const statusClass = space.status === "available" ? "status-available" : "status-occupied";
    const buttonLabel = space.status === "available" ? "Check in" : "Check out";
    const action = space.status === "available" ? "checkin" : "checkout";

    row.innerHTML = `
      <span>${space.name} (Floor ${space.floor}) - <span class="${statusClass}">${space.status}</span></span>
      <button onclick="doCheckAction('${space.space_id}', '${action}')">${buttonLabel}</button>
    `;
    list.appendChild(row);
  });
}

async function doCheckAction(spaceId, action) {
  await fetch(`${API_BASE}/${action}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ space_id: spaceId, user_email: currentUser.email }),
  });
  loadAvailability();
}