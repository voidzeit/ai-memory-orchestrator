const $ = (sel) => document.querySelector(sel);
const token = new URLSearchParams(location.search).get("token");
const api = (path, options) =>
  fetch(path + (token ? (path.includes("?") ? "&" : "?") + "token=" + token : ""), options).then((r) => {
    if (!r.ok) return r.json().then((body) => Promise.reject(body.detail || r.statusText));
    return r.json();
  });

const esc = (value) =>
  String(value ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

function kv(rows) {
  return (
    "<table class='kv'>" +
    rows.map(([key, value]) => `<tr><th>${esc(key)}</th><td>${value}</td></tr>`).join("") +
    "</table>"
  );
}

// --- Tabs -------------------------------------------------------------
document.querySelectorAll("#tabs button").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("#tabs button").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".view").forEach((v) => v.classList.remove("active"));
    button.classList.add("active");
    $("#view-" + button.dataset.view).classList.add("active");
  });
});

// --- Health -----------------------------------------------------------
function renderHealth(snapshot) {
  const badge = $("#health-badge");
  badge.textContent = snapshot.status;
  badge.className = "badge " + esc(snapshot.status);
  const adapters = Object.entries(snapshot.adapters || {})
    .map(([name, present]) => `<span class="pill ${present ? "on" : "off"}">${esc(name)}</span>`)
    .join(" ");
  const severities = Object.entries((snapshot.evolution || {}).by_severity || {})
    .map(([severity, count]) => `<span class="pill sev-${esc(severity)}">${esc(severity)}: ${count}</span>`)
    .join(" ");
  $("#view-health").innerHTML =
    "<h2>Vital signs</h2>" +
    kv([
      ["Validation", esc((snapshot.validation || {}).status || "not run")],
      ["Graph", `${snapshot.graph.nodes} nodes / ${snapshot.graph.edges} edges`],
      [
        "Levels",
        Object.entries(snapshot.graph.by_level)
          .map(([level, count]) => `<span class="pill">${esc(level)}: ${count}</span>`)
          .join(" "),
      ],
      ["Findings", severities || "none"],
      ["Context packs", (snapshot.packs || []).map((p) => `<code>${esc(p)}</code>`).join(" ") || "none"],
      ["Adapters", adapters],
      ["Evidence entries", snapshot.ledger_entries],
    ]) +
    (snapshot.benchmark
      ? "<h2>Latest benchmark</h2>" +
        kv(Object.entries(snapshot.benchmark).map(([key, value]) => [key, esc(JSON.stringify(value))]))
      : "<p class='muted'>No benchmark yet — run <code>amo benchmark</code>.</p>");
}

// --- Graph explorer ----------------------------------------------------
let graphNodes = [];
function renderGraphRows() {
  const query = ($("#graph-search").value || "").toLowerCase();
  const rows = graphNodes
    .filter((node) =>
      !query ||
      [node.id, node.label, node.type, node.level].some((field) => String(field || "").toLowerCase().includes(query))
    )
    .slice(0, 400)
    .map(
      (node) =>
        `<tr><td>${esc(node.type)}</td><td title="${esc(node.id)}">${esc(node.label)}</td>` +
        `<td>${esc(node.level || "")}</td><td>${esc(node.authority ?? "")}</td><td>${esc(node.source || "")}</td></tr>`
    )
    .join("");
  $("#graph-table tbody").innerHTML = rows || "<tr><td colspan='5' class='muted'>No matching nodes.</td></tr>";
}
$("#graph-search").addEventListener("input", renderGraphRows);

// --- Context flow -------------------------------------------------------
$("#context-form").addEventListener("submit", (event) => {
  event.preventDefault();
  $("#context-result").innerHTML = "<p class='muted'>Compiling…</p>";
  api("/api/context", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task: $("#context-task").value, profile: $("#context-profile").value }),
  })
    .then((result) => {
      const explanation = ((result.explanation || {}).selection || [])
        .map(
          (item) =>
            `<tr><td><code>${esc(item.path)}</code></td><td>${esc(item.score ?? "")}</td>` +
            `<td>${(item.reasons || []).map(esc).join(", ")}</td><td>${esc(item.tokens ?? "")}</td></tr>`
        )
        .join("");
      $("#context-result").innerHTML =
        `<p>Pack written to <code>${esc(result.pack)}</code></p>` +
        (explanation
          ? "<h3>Why these units</h3><table><thead><tr><th>Path</th><th>Score</th><th>Reasons</th><th>Tokens</th></tr></thead><tbody>" +
            explanation +
            "</tbody></table>"
          : "") +
        `<h3>Pack</h3><pre>${esc(result.content)}</pre>`;
    })
    .catch((error) => {
      $("#context-result").innerHTML = `<p class="error">${esc(error)}</p>`;
    });
});

// --- Static views -------------------------------------------------------
function renderBenchmark() {
  api("/api/benchmark")
    .then((benchmark) => {
      $("#view-benchmark").innerHTML =
        `<h2>Benchmark — ${esc(benchmark.task)}</h2>` +
        kv(Object.entries(benchmark.metrics).map(([key, value]) => [key, esc(JSON.stringify(value))]));
    })
    .catch(() => {
      $("#view-benchmark").innerHTML = "<p class='muted'>No benchmark yet — run <code>amo benchmark</code>.</p>";
    });
}

function renderFindings() {
  api("/api/evolution").then((evolution) => {
    const findings = ((evolution.latest_cycle || {}).findings || [])
      .map(
        (finding) =>
          `<tr><td><span class="pill sev-${esc(finding.severity)}">${esc(finding.severity)}</span></td>` +
          `<td>${esc(finding.layer)}</td><td><code>${esc(finding.id)}</code></td>` +
          `<td>${esc(finding.message)}<br/><span class="muted">${esc(finding.recommendation)}</span></td></tr>`
      )
      .join("");
    $("#view-findings").innerHTML = findings
      ? "<table><thead><tr><th>Severity</th><th>Layer</th><th>Signal</th><th>Detail</th></tr></thead><tbody>" +
        findings +
        "</tbody></table>"
      : "<p class='muted'>No findings — run <code>amo optimize suggest</code>.</p>";
  });
}

function renderLedger() {
  api("/api/ledger?limit=100").then((ledger) => {
    const rows = ledger.entries
      .slice()
      .reverse()
      .map(
        (entry) =>
          `<tr><td class="muted">${esc((entry.timestamp || "").slice(0, 19))}</td>` +
          `<td><code>${esc(entry.kind)}</code></td><td>${esc(entry.source)}</td>` +
          `<td>${esc(entry.result)}</td><td>${esc(entry.authority)}</td></tr>`
      )
      .join("");
    $("#view-ledger").innerHTML =
      `<p class="muted">${ledger.total} entries total; latest first.</p>` +
      "<table><thead><tr><th>Time (UTC)</th><th>Kind</th><th>Source</th><th>Result</th><th>Authority</th></tr></thead><tbody>" +
      rows +
      "</tbody></table>";
  });
}

// --- Boot ----------------------------------------------------------------
api("/api/organism").then(renderHealth);
api("/api/graph").then((graph) => {
  graphNodes = graph.nodes || [];
  $("#graph-stats").textContent = `${graphNodes.length} nodes / ${(graph.edges || []).length} edges`;
  renderGraphRows();
});
renderBenchmark();
renderFindings();
renderLedger();
