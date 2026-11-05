// Confirmación antes de eliminar
document.addEventListener("submit", (e) => {
  const msg = e.target.dataset.confirm;
  if (msg && !window.confirm(msg)) e.preventDefault();
});

// Los avisos desaparecen solos a los 4 segundos
document.querySelectorAll("[data-flash]").forEach((el) => {
  setTimeout(() => {
    el.classList.add("oculto");
    setTimeout(() => el.remove(), 400);
  }, 4000);
});
