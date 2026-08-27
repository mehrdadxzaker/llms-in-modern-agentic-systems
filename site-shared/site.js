document.querySelectorAll('[data-nav-toggle]').forEach((toggle) => {
  toggle.addEventListener('click', () => {
    const nav = document.querySelector('[data-site-nav]');
    const isOpen = nav.dataset.open === 'true';
    nav.dataset.open = String(!isOpen);
    toggle.setAttribute('aria-expanded', String(!isOpen));
  });
});

document.querySelectorAll('[data-site-nav] a').forEach((link) => {
  link.addEventListener('click', () => {
    const nav = document.querySelector('[data-site-nav]');
    const toggle = document.querySelector('[data-nav-toggle]');
    if (!nav || !toggle) return;
    nav.dataset.open = 'false';
    toggle.setAttribute('aria-expanded', 'false');
  });
});

document.querySelectorAll('[data-copy-target]').forEach((button) => {
  button.addEventListener('click', async () => {
    const target = document.getElementById(button.dataset.copyTarget);
    if (!target) return;

    const originalLabel = button.textContent;
    try {
      await navigator.clipboard.writeText(target.textContent.trim());
      button.textContent = 'Copied';
    } catch {
      button.textContent = 'Select to copy';
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(target);
      selection.removeAllRanges();
      selection.addRange(range);
    }

    window.setTimeout(() => {
      button.textContent = originalLabel;
    }, 1800);
  });
});
