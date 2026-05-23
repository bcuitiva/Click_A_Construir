// chat.js — Lógica del chat con adjuntos

document.addEventListener("DOMContentLoaded", () => {

  // ── Scroll automático al final ──────────────────────────────────────
  const chatMessages = document.getElementById("chatMessages");
  if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // ── Enviar con Enter (Shift+Enter = salto de línea si fuera textarea) ──
  const chatInput = document.getElementById("chatTextInput");
  const chatForm  = document.getElementById("chatForm");
  chatInput?.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      chatForm?.requestSubmit();
    }
  });

});

// ── Preview del adjunto antes de enviar ─────────────────────────────
function previewAttach(input) {
  const file    = input.files[0];
  const preview = document.getElementById("attachPreview");
  const inner   = document.getElementById("attachPreviewInner");
  const sendBtn = document.getElementById("chatSendBtn");
  if (!file || !preview || !inner) return;

  inner.innerHTML = "";

  const ext = file.name.split(".").pop().toLowerCase();
  const isImg = ["png","jpg","jpeg","gif","webp"].includes(ext);

  if (isImg) {
    const reader = new FileReader();
    reader.onload = (e) => {
      inner.innerHTML = `
        <img src="${e.target.result}" alt="preview" class="attach-preview__img"/>
        <span class="attach-preview__name">${file.name}</span>`;
    };
    reader.readAsDataURL(file);
  } else if (ext === "pdf") {
    inner.innerHTML = `
      <span class="attach-preview__icon">📄</span>
      <span class="attach-preview__name">${file.name}</span>
      <span class="attach-preview__size">${formatSize(file.size)}</span>`;
  } else {
    inner.innerHTML = `
      <span class="attach-preview__icon">📎</span>
      <span class="attach-preview__name">${file.name}</span>
      <span class="attach-preview__size">${formatSize(file.size)}</span>`;
  }

  preview.style.display = "flex";
  if (sendBtn) sendBtn.style.background = "var(--primary)";
}

function removeAttach() {
  const input   = document.getElementById("adjuntoInput");
  const preview = document.getElementById("attachPreview");
  if (input)   input.value = "";
  if (preview) preview.style.display = "none";
}

function formatSize(bytes) {
  if (bytes < 1024)         return bytes + " B";
  if (bytes < 1024 * 1024)  return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

// ── Lightbox para imágenes recibidas ───────────────────────────────
function openLightbox(src) {
  const lb  = document.getElementById("lightbox");
  const img = document.getElementById("lightboxImg");
  if (!lb || !img) return;
  img.src = src;
  lb.style.display = "flex";
}
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    const lb = document.getElementById("lightbox");
    if (lb) lb.style.display = "none";
  }
});
