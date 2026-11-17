'use strict';
const sectionLinks = [...document.querySelectorAll('.site-nav a[href^="#"]')];
if ('IntersectionObserver' in window && sectionLinks.length) {
  const observer = new IntersectionObserver(entries => {
    const current = entries.filter(entry => entry.isIntersecting).sort((a,b) => b.intersectionRatio-a.intersectionRatio)[0];
    if (!current) return;
    sectionLinks.forEach(link => {
      if (link.hash === `#${current.target.id}`) link.setAttribute('aria-current','location');
      else link.removeAttribute('aria-current');
    });
  }, {rootMargin:'-120px 0px -45% 0px',threshold:[0,.15,.4]});
  document.querySelectorAll('main section[id]').forEach(section => observer.observe(section));
}
