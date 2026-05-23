// =============================================
// Click a Construir — main.js
// =============================================

document.addEventListener("DOMContentLoaded", () => {

  // ----- LOGIN TABS -----
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabPanels = document.querySelectorAll(".tab-panel");

  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const target = btn.dataset.tab;
      tabBtns.forEach(b => b.classList.remove("tab-btn--active"));
      tabPanels.forEach(p => p.classList.remove("tab-panel--active"));
      btn.classList.add("tab-btn--active");
      const panel = document.getElementById("panel-" + target);
      if (panel) panel.classList.add("tab-panel--active");
    });
  });

  // Link buttons inside panels that switch tabs
  document.querySelectorAll(".link-btn[data-tab]").forEach(btn => {
    btn.addEventListener("click", () => {
      const target = btn.dataset.tab;
      const tabBtn = document.querySelector(`.tab-btn[data-tab="${target}"]`);
      if (tabBtn) tabBtn.click();
    });
  });

  // ----- ROLE SELECTOR -----
  const roleBtns = document.querySelectorAll(".role-btn");
  const roleInput = document.getElementById("roleInput");

  roleBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      roleBtns.forEach(b => b.classList.remove("role-btn--active"));
      btn.classList.add("role-btn--active");
      if (roleInput) roleInput.value = btn.dataset.role;
    });
  });

  // ----- MODAL -----
  const fabBtn       = document.getElementById("fabBtn");
  const modalOverlay = document.getElementById("modalOverlay");
  const modalClose   = document.getElementById("modalClose");

  function openModal() {
    if (modalOverlay) modalOverlay.classList.add("modal-overlay--open");
  }
  function closeModal() {
    if (modalOverlay) modalOverlay.classList.remove("modal-overlay--open");
  }

  if (fabBtn)     fabBtn.addEventListener("click", openModal);
  if (modalClose) modalClose.addEventListener("click", closeModal);
  if (modalOverlay) {
    modalOverlay.addEventListener("click", e => {
      if (e.target === modalOverlay) closeModal();
    });
  }
  // ESC para cerrar modal
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") closeModal();
  });

  // ----- AUTO-DISMISS ALERTS -----
  document.querySelectorAll(".alert").forEach(alert => {
    setTimeout(() => {
      alert.style.transition = "opacity 0.4s";
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 400);
    }, 4000);
  });

});
