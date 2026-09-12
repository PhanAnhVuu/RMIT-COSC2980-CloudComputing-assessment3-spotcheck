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

  const sorted = data.spaces.slice().sort((a, b) => {
    const floorDiff = Number(a.floor) - Number(b.floor);
    if (floorDiff !== 0) return floorDiff;
    return a.space_id.localeCompare(b.space_id, undefined, { numeric: true });
  });

  sorted.forEach((space) => {
    const row = document.createElement("div");
    row.className = "space-row";
    const statusClass = space.status === "available" ? "status-available" : "status-occupied";
    const isMine = space.checked_in_by === currentUser.email;

    let label = space.status;
    if (isMine) label = "Checked in by you";

    let buttonHtml = "";
    if (space.status === "available") {
      buttonHtml = `<button onclick="doCheckAction('${space.space_id}', 'checkin')">Check in</button>`;
    } else if (isMine) {
      buttonHtml = `<button onclick="doCheckAction('${space.space_id}', 'checkout')">Check out</button>`;
    }

    row.innerHTML = `
      <span>Floor ${space.floor} - ${space.name} - <span class="${statusClass}">${label}</span></span>
      ${buttonHtml}
    `;
    list.appendChild(row);
  });
}

async function doCheckAction(spaceId, action) {
  const res = await fetch(`${API_BASE}/${action}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ space_id: spaceId, user_email: currentUser.email }),
  });
  console.log("Response status:", res.status);
  const data = await res.json();
  console.log("Response data:", data);

  if (res.status !== 200) {
    alert(data.error || "Something went wrong");
  }

  loadAvailability();
}

async function loadTrends() {
  const res = await fetch(`${API_BASE}/trends`);
  const data = await res.json();

  const spacesDiv = document.getElementById("trends-spaces");
  spacesDiv.innerHTML = "";
  data.busiest_spaces.forEach((row) => {
    const p = document.createElement("p");
    p.textContent = `${row.space_id}: ${row.total_checkins} check-ins`;
    spacesDiv.appendChild(p);
  });

  const hoursDiv = document.getElementById("trends-hours");
  hoursDiv.innerHTML = "";
  data.busiest_hours.forEach((row) => {
    const p = document.createElement("p");
    p.textContent = `${row.hour_of_day}:00 - ${row.total_checkins} check-ins`;
    hoursDiv.appendChild(p);
  });
}