document.querySelectorAll('[data-nav-toggle]').forEach((toggle) => {
  toggle.addEventListener('click', () => {
    const nav = document.querySelector('[data-site-nav]');
    const isOpen = nav.dataset.open === 'true';
    nav.dataset.open = String(!isOpen);
    toggle.setAttribute('aria-expanded', String(!isOpen));
  });
});
