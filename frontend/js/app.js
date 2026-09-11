const API_BASE = "/api";

// ---------- index.html: ticket submission ----------
const ticketForm = document.getElementById("ticketForm");
if (ticketForm) {
  ticketForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const messageEl = document.getElementById("formMessage");

    const payload = {
      name: document.getElementById("name").value,
      email: document.getElementById("email").value,
      title: document.getElementById("title").value,
      description: document.getElementById("description").value,
      priority: document.getElementById("priority").value,
      category: document.getElementById("category").value,
    };

    try {
      const res = await fetch(`${API_BASE}/SubmitTicket`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Submit failed");
      const ticket = await res.json();

      messageEl.textContent = `Ticket submitted! Category: ${ticket.category}. Reference: ${ticket.id.slice(0, 8)}`;
      messageEl.className = "success";
      ticketForm.reset();
    } catch (err) {
      messageEl.textContent =
        "Something went wrong submitting your ticket. Please try again.";
      messageEl.className = "error";
    }
  });
}

// ---------- admin.html: ticket list ----------
const ticketsBody = document.getElementById("ticketsBody");
if (ticketsBody) {
  let allTickets = [];

  async function loadTickets() {
    const res = await fetch(`${API_BASE}/GetTickets`);
    allTickets = await res.json();
    renderTickets();
  }

  function renderTickets() {
    const search = document.getElementById("searchBox").value.toLowerCase();
    const statusFilter = document.getElementById("statusFilter").value;
    const categoryFilter = document.getElementById("categoryFilter").value;

    let filtered = allTickets.filter((t) => {
      const matchesSearch =
        !search ||
        t.name.toLowerCase().includes(search) ||
        t.email.toLowerCase().includes(search);
      const matchesStatus = !statusFilter || t.status === statusFilter;
      const matchesCategory = !categoryFilter || t.category === categoryFilter;
      return matchesSearch && matchesStatus && matchesCategory;
    });

    ticketsBody.innerHTML = "";
    document.getElementById("emptyState").style.display = filtered.length
      ? "none"
      : "block";

    filtered
      .sort((a, b) => new Date(b.created_date) - new Date(a.created_date))
      .forEach((t) => {
        const tr = document.createElement("tr");
        const badgeClass = t.status.replace(/\s+/g, "");
        tr.innerHTML = `
          <td>${escapeHtml(t.title)}</td>
          <td>${escapeHtml(t.name)}</td>
          <td>${escapeHtml(t.category)}</td>
          <td>${escapeHtml(t.priority)}</td>
          <td><span class="badge ${badgeClass}">${escapeHtml(t.status)}</span></td>
          <td>${new Date(t.created_date).toLocaleDateString()}</td>
        `;

        const statusCell = document.createElement("td");
        const select = document.createElement("select");
        select.className = "status-select";
        ["New", "Categorised", "In Progress", "Resolved"].forEach((s) => {
          const opt = document.createElement("option");
          opt.value = s;
          opt.textContent = s;
          if (s === t.status) opt.selected = true;
          select.appendChild(opt);
        });
        select.addEventListener("change", () =>
          updateStatus(t.id, select.value),
        );
        statusCell.appendChild(select);
        tr.appendChild(statusCell);

        ticketsBody.appendChild(tr);
      });
  }

  async function updateStatus(ticketId, newStatus) {
    await fetch(`${API_BASE}/UpdateTicket/${ticketId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus }),
    });
    await loadTickets();
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  ["searchBox", "statusFilter", "categoryFilter"].forEach((id) => {
    document.getElementById(id).addEventListener("input", renderTickets);
  });

  loadTickets();
}
