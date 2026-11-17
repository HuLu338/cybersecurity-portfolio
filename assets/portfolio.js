'use strict';
document.documentElement.classList.add('js');

const motionHero = document.querySelector('.hero[data-motion]');
const motionButton = document.querySelector('.motion-toggle');
if (motionHero && motionButton) {
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  let requested = !preference.matches;
  let visible = true;
  const updateMotion = () => {
    motionHero.dataset.motion = requested && visible && !document.hidden && !preference.matches ? 'running' : 'paused';
    motionButton.hidden = preference.matches;
    motionButton.setAttribute('aria-pressed', String(requested));
    motionButton.querySelector('.motion-label').textContent = requested ? 'Pause motion' : 'Play motion';
  };
  motionButton.addEventListener('click', () => { requested = !requested; updateMotion(); });
  preference.addEventListener('change', () => { requested = !preference.matches; updateMotion(); });
  document.addEventListener('visibilitychange', updateMotion);
  if ('IntersectionObserver' in window) {
    const visibility = new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting && entries[0].intersectionRatio >= .04;
      updateMotion();
    }, {threshold:[0,.04],rootMargin:'-80px 0px 0px'});
    visibility.observe(motionHero);
  }
  updateMotion();
}

const menu = document.querySelector('.nav-toggle');
const nav = document.querySelector('.site-nav');
if (menu && nav) {
  const closeMenu = () => {
    menu.setAttribute('aria-expanded', 'false');
    nav.classList.remove('is-open');
  };
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  });
  nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menu.focus();
    }
  });
}

const policyMessages = {
  owner: ['200 OK', 'The owner can read the file.'],
  other: ['403 Forbidden', 'A different user is denied access.'],
  admin: ['200 OK', 'An administrator can read the file.']
};
document.querySelectorAll('[data-policy]').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('[data-policy]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    const [status, message] = policyMessages[button.dataset.policy];
    document.getElementById('policy-status').textContent = status;
    document.getElementById('policy-message').textContent = message;
    document.getElementById('policy-result').classList.toggle('is-denied', button.dataset.policy === 'other');
  });
});

const filters = document.querySelector('.filters');
if (filters) {
  filters.hidden = false;
  const cards = [...document.querySelectorAll('.project-card')];
  filters.querySelectorAll('[data-filter]').forEach(button => {
    button.addEventListener('click', () => {
      filters.querySelectorAll('[data-filter]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      const selected = button.dataset.filter;
      cards.forEach(card => { card.hidden = selected !== 'All work' && card.dataset.category !== selected; });
      const count = cards.filter(card => !card.hidden).length;
      document.querySelector('.filter-count').textContent = `Showing ${count} project${count === 1 ? '' : 's'}`;
    });
  });
}

const pageSections = [...document.querySelectorAll('main > section[id]')];
if (pageSections.length) {
  const links = [...document.querySelectorAll('.site-nav a')];
  let scheduled = false;
  let activeId = null;
  const updateActiveSection = () => {
    scheduled = false;
    let current = 'top';
    const readingLine = Math.min(window.innerHeight * .3, 220);
    pageSections.forEach(section => {
      if (section.getBoundingClientRect().top <= readingLine) current = section.id;
    });
    if (current === activeId) return;
    activeId = current;
    links.forEach(link => {
      if (link.getAttribute('href') === `#${current}`) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  };
  const scheduleNavigationUpdate = () => {
    if (!scheduled) { scheduled = true; requestAnimationFrame(updateActiveSection); }
  };
  window.addEventListener('scroll', scheduleNavigationUpdate, {passive:true});
  window.addEventListener('resize', scheduleNavigationUpdate);
  window.addEventListener('load', scheduleNavigationUpdate);
  updateActiveSection();
}
