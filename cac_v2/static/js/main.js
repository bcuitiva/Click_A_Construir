// Click a Construir — main.js v2

document.addEventListener("DOMContentLoaded", () => {

  // ── LOGIN TABS ──────────────────────────────────
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => switchTab(btn.dataset.tab));
  });
  document.querySelectorAll(".link-btn[data-tab]").forEach(btn => {
    btn.addEventListener("click", () => switchTab(btn.dataset.tab));
  });
  function switchTab(target) {
    document.querySelectorAll(".tab-btn").forEach(b =>
      b.classList.toggle("tab-btn--active", b.dataset.tab === target));
    document.querySelectorAll(".tab-panel").forEach(p =>
      p.classList.toggle("tab-panel--active", p.id === "panel-" + target));
  }

  // ── ROLE SELECTOR ───────────────────────────────
  const roleBtns = document.querySelectorAll(".role-btn");
  const roleInput = document.getElementById("roleInput");
  roleBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      roleBtns.forEach(b => b.classList.remove("role-btn--active"));
      btn.classList.add("role-btn--active");
      if (roleInput) roleInput.value = btn.dataset.role;
    });
  });

  // ── MODAL ───────────────────────────────────────
  const fabBtn       = document.getElementById("fabBtn");
  const modalOverlay = document.getElementById("modalOverlay");
  const modalClose   = document.getElementById("modalClose");

  function openModal()  { modalOverlay?.classList.add("modal-overlay--open"); }
  function closeModal() { modalOverlay?.classList.remove("modal-overlay--open"); }

  fabBtn?.addEventListener("click", openModal);
  modalClose?.addEventListener("click", closeModal);
  modalOverlay?.addEventListener("click", e => { if (e.target === modalOverlay) closeModal(); });
  document.addEventListener("keydown", e => { if (e.key === "Escape") closeModal(); });

  // ── CARRUSEL ────────────────────────────────────
  const carousel   = document.getElementById("profCarousel");
  const btnLeft    = document.getElementById("scrollLeft");
  const btnRight   = document.getElementById("scrollRight");
  const SCROLL_AMT = 220;

  btnLeft?.addEventListener("click",  () => carousel?.scrollBy({ left: -SCROLL_AMT, behavior: "smooth" }));
  btnRight?.addEventListener("click", () => carousel?.scrollBy({ left:  SCROLL_AMT, behavior: "smooth" }));

  // Arrastre con mouse en el carrusel
  if (carousel) {
    let isDown = false, startX, scrollLeft;
    carousel.addEventListener("mousedown", e => {
      isDown = true; carousel.style.cursor = "grabbing";
      startX = e.pageX - carousel.offsetLeft;
      scrollLeft = carousel.scrollLeft;
    });
    carousel.addEventListener("mouseleave", () => { isDown = false; carousel.style.cursor = ""; });
    carousel.addEventListener("mouseup",    () => { isDown = false; carousel.style.cursor = ""; });
    carousel.addEventListener("mousemove",  e => {
      if (!isDown) return;
      e.preventDefault();
      carousel.scrollLeft = scrollLeft - (e.pageX - carousel.offsetLeft - startX);
    });
  }

  // ── AUTO-SCROLL CHAT ────────────────────────────
  const chatMessages = document.getElementById("chatMessages");
  if (chatMessages) chatMessages.scrollTop = chatMessages.scrollHeight;

  // ── AUTO-DISMISS ALERTS ─────────────────────────
  document.querySelectorAll(".alert").forEach(el => {
    setTimeout(() => {
      el.style.transition = "opacity .4s";
      el.style.opacity    = "0";
      setTimeout(() => el.remove(), 400);
    }, 4000);
  });

});
