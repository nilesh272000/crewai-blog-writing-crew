const form = document.getElementById("blogForm");
const result = document.getElementById("result");
const content = document.getElementById("content");
const statusEl = document.getElementById("status");
const button = document.getElementById("generateBtn");

let payload = null;

function markdownToHtml(text) {
  return text
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/^### (.*)$/gm, "<h3>$1</h3>")
    .replace(/^## (.*)$/gm, "<h2>$1</h2>")
    .replace(/^# (.*)$/gm, "<h1>$1</h1>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/^\- (.*)$/gm, "<li>$1</li>")
    .replace(/^\d+\. (.*)$/gm, "<li>$1</li>")
    .replace(/\n{2,}/g, "</p><p>")
    .replace(/\n/g, "<br>");
}

function renderTab(tab) {
  if (!payload) return;
  if (tab === "final") content.innerHTML = `<p>${markdownToHtml(payload.final_blog)}</p>`;
  if (tab === "outline") content.innerHTML = `<p>${markdownToHtml(payload.outline)}</p>`;
  if (tab === "draft") content.innerHTML = `<p>${markdownToHtml(payload.draft)}</p>`;
  if (tab === "seo") content.innerHTML = `<ul>${payload.seo_keywords.map(k => `<li>${k}</li>`).join("")}</ul>`;
}

document.querySelectorAll(".tab").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    tab.classList.add("active");
    renderTab(tab.dataset.tab);
  });
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  button.disabled = true;
  statusEl.textContent = "Running Planner → Writer → Editor...";
  result.classList.add("hidden");

  const keywords = document.getElementById("keywords").value
    .split(",").map(x => x.trim()).filter(Boolean);

  try {
    const response = await fetch("/api/blog/generate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        topic: document.getElementById("topic").value,
        audience: document.getElementById("audience").value,
        tone: document.getElementById("tone").value,
        target_words: Number(document.getElementById("targetWords").value),
        keywords
      })
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Generation failed");

    payload = data;
    document.getElementById("title").textContent = data.title;
    document.getElementById("meta").textContent = data.meta_description;
    document.getElementById("modeBadge").textContent = data.mode.toUpperCase();
    result.classList.remove("hidden");
    renderTab("final");
    statusEl.textContent = "Completed successfully.";
  } catch (error) {
    statusEl.textContent = `Error: ${error.message}`;
  } finally {
    button.disabled = false;
  }
});
