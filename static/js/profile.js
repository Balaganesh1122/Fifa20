function openTab(tabId) {
  document.querySelectorAll('.tab-section').forEach(sec => {
    sec.classList.remove('active');
  });

  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('active');
  });

  document.getElementById(tabId).classList.add('active');
  event.target.classList.add('active');
}
function scrollToSection(id) {
    document.getElementById(id).scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}
