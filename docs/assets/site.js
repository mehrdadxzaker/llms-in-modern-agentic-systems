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

const escapeHtml = (value = '') => String(value)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#039;');

const slugify = (value = '') => String(value)
  .toLowerCase()
  .normalize('NFKD')
  .replace(/[^a-z0-9]+/g, '-')
  .replace(/(^-|-$)/g, '');

const literature = Array.isArray(window.LITERATURE_DATA) ? window.LITERATURE_DATA : [];
const results = document.querySelector('[data-library-results]');
const searchInput = document.querySelector('[data-library-search]');
const filterButtons = [...document.querySelectorAll('[data-library-filter]')];
const count = document.querySelector('[data-library-count]');
const expandButton = document.querySelector('[data-library-expand]');

const branchOrder = [
  'Foundations and scope',
  'Grounding and action',
  'State, adaptation, and coordination',
  'Evaluation and evidence',
  'Assurance and deployment',
  'Extended evidence base',
];

const branchColors = {
  'Foundations and scope': '#4f7dd9',
  'Grounding and action': '#5a9f76',
  'State, adaptation, and coordination': '#8a6fb1',
  'Evaluation and evidence': '#db9560',
  'Assurance and deployment': '#70849b',
  'Extended evidence base': '#53657c',
};

let activeFilter = 'all';
let allExpanded = false;

const matchesFilter = (entry) => {
  if (activeFilter === 'atlas') return entry.atlas;
  if (activeFilter === 'extended') return !entry.atlas;
  if (activeFilter === 'pdf') return Boolean(entry.pdfUrl);
  if (activeFilter === 'recent') return Number(entry.year) >= 2025;
  if (branchOrder.includes(activeFilter)) return entry.branch === activeFilter;
  return true;
};

const matchesSearch = (entry, query) => {
  if (!query) return true;
  const haystack = [
    entry.title,
    entry.year,
    entry.venue,
    entry.key,
    entry.branch,
    entry.locus,
  ].join(' ').toLowerCase();
  return haystack.includes(query);
};

const entryLinks = (entry) => {
  const links = [];
  if (entry.pdfUrl) {
    links.push(`<a class="library-link primary" href="${escapeHtml(entry.pdfUrl)}" target="_blank" rel="noopener">PDF <span aria-hidden="true">↗</span></a>`);
  }
  if (entry.sourceUrl && entry.sourceUrl !== entry.pdfUrl) {
    links.push(`<a class="library-link" href="${escapeHtml(entry.sourceUrl)}" target="_blank" rel="noopener">Paper <span aria-hidden="true">↗</span></a>`);
  }
  if (!links.length) {
    links.push(`<a class="library-link" href="https://github.com/Xpounder-com/llms-in-modern-agentic-systems/search?q=${encodeURIComponent(entry.key)}" target="_blank" rel="noopener">Bibliography <span aria-hidden="true">↗</span></a>`);
  }
  return links.join('');
};

const renderEntry = (entry) => `
  <article class="library-row" role="row">
    <div class="library-year" role="cell"><span class="mobile-label">Year</span>${escapeHtml(entry.year || '—')}</div>
    <div class="library-paper" role="cell">
      <span class="scope-badge ${entry.atlas ? 'atlas' : 'extended'}">${entry.atlas ? 'Atlas' : 'Extended'}</span>
      <h4>${escapeHtml(entry.title)}</h4>
      <small>${escapeHtml(entry.key)}</small>
    </div>
    <div class="library-venue" role="cell"><span class="mobile-label">Venue</span>${escapeHtml(entry.venue || '—')}</div>
    <div class="library-links" role="cell">${entryLinks(entry)}</div>
  </article>`;

const renderLibrary = () => {
  if (!results) return;

  const query = (searchInput?.value || '').trim().toLowerCase();
  const visible = literature.filter((entry) => matchesFilter(entry) && matchesSearch(entry, query));
  if (count) count.textContent = visible.length.toLocaleString();

  if (!visible.length) {
    results.innerHTML = `
      <div class="library-empty">
        <strong>No matching sources</strong>
        <p>Try a broader term or choose a different filter.</p>
      </div>`;
    return;
  }

  const branches = new Map();
  visible.forEach((entry) => {
    if (!branches.has(entry.branch)) branches.set(entry.branch, new Map());
    const loci = branches.get(entry.branch);
    if (!loci.has(entry.locus)) loci.set(entry.locus, []);
    loci.get(entry.locus).push(entry);
  });

  results.innerHTML = branchOrder
    .filter((branch) => branches.has(branch))
    .map((branch) => {
      const loci = branches.get(branch);
      const branchTotal = [...loci.values()].reduce((sum, entries) => sum + entries.length, 0);
      const groups = [...loci.entries()].map(([locus, entries]) => `
        <details class="library-group" ${allExpanded || query || activeFilter !== 'all' ? 'open' : ''}>
          <summary>
            <span>${escapeHtml(locus)}</span>
            <small>${entries.length} ${entries.length === 1 ? 'source' : 'sources'}</small>
          </summary>
          ${entries[0].description ? `<p class="library-group-note">${escapeHtml(entries[0].description)}</p>` : ''}
          <div class="paper-table" role="table" aria-label="${escapeHtml(locus)} literature">
            <div class="library-row library-header" role="row">
              <div role="columnheader">Year</div>
              <div role="columnheader">Paper</div>
              <div role="columnheader">Venue</div>
              <div role="columnheader">Links</div>
            </div>
            ${entries.map(renderEntry).join('')}
          </div>
        </details>`).join('');

      return `
        <section class="library-branch" style="--branch-color: ${branchColors[branch] || '#53657c'}">
          <header>
            <div><span></span><h3>${escapeHtml(branch)}</h3></div>
            <p>${branchTotal} ${branchTotal === 1 ? 'source' : 'sources'}</p>
          </header>
          ${groups}
        </section>`;
    }).join('');
};

searchInput?.addEventListener('input', renderLibrary);

filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    activeFilter = button.dataset.libraryFilter;
    filterButtons.forEach((candidate) => {
      const active = candidate === button;
      candidate.classList.toggle('active', active);
      candidate.setAttribute('aria-pressed', String(active));
    });
    renderLibrary();
  });
});

expandButton?.addEventListener('click', () => {
  allExpanded = !allExpanded;
  document.querySelectorAll('.library-group').forEach((group) => {
    group.open = allExpanded;
  });
  expandButton.textContent = allExpanded ? 'Collapse all sections' : 'Expand all sections';
});

document.addEventListener('keydown', (event) => {
  if (event.key === '/' && document.activeElement?.tagName !== 'INPUT' && document.activeElement?.tagName !== 'TEXTAREA') {
    event.preventDefault();
    searchInput?.focus();
  }
});

const figureDialog = document.querySelector('[data-figure-dialog]');
document.querySelector('[data-figure-open]')?.addEventListener('click', () => figureDialog?.showModal());
document.querySelector('[data-figure-close]')?.addEventListener('click', () => figureDialog?.close());
figureDialog?.addEventListener('click', (event) => {
  if (event.target === figureDialog) figureDialog.close();
});

const updateProjectPulse = async () => {
  try {
    const response = await fetch('https://api.github.com/repos/Xpounder-com/llms-in-modern-agentic-systems', {
      headers: { Accept: 'application/vnd.github+json' },
    });
    if (!response.ok) throw new Error('GitHub project data unavailable');
    const project = await response.json();
    const values = {
      '[data-github-stars]': project.stargazers_count,
      '[data-github-forks]': project.forks_count,
      '[data-github-issues]': project.open_issues_count,
    };
    Object.entries(values).forEach(([selector, value]) => {
      const target = document.querySelector(selector);
      if (target) target.textContent = Number(value).toLocaleString();
    });
  } catch {
    document.querySelector('.project-pulse')?.classList.add('unavailable');
  }
};

const sectionLinks = [...document.querySelectorAll('.site-nav a[href^="#"], .contents a[href^="#"]')];
const sections = [...new Set(sectionLinks.map((link) => document.querySelector(link.getAttribute('href'))).filter(Boolean))];
const sectionObserver = new IntersectionObserver((entries) => {
  const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
  if (!visible) return;
  sectionLinks.forEach((link) => {
    const current = link.getAttribute('href') === `#${visible.target.id}`;
    if (current) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
}, { rootMargin: '-22% 0px -66% 0px', threshold: [0, 0.1, 0.4] });

sections.forEach((section) => sectionObserver.observe(section));

renderLibrary();
updateProjectPulse();
