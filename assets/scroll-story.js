'use strict';
/* Scroll narrative for the home page: pinned stage, reading ruler and section traces.
   Progress is measured once per layout change and applied with rAF, so scrolling
   only writes custom properties, opacity and transforms. */
(() => {
  const root = document.documentElement;
  const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const narrow = window.matchMedia('(max-width: 900px)');

  const stage = document.querySelector('.work-stage');
  const track = stage && stage.querySelector('.stage-track');
  const pin = stage && stage.querySelector('.stage-pin');
  const tabs = stage ? [...stage.querySelectorAll('[role="tab"]')] : [];
  const steps = stage && stage.querySelector('.stage-steps');
  const hero = document.querySelector('.hero[data-motion]');
  const transitions = [...document.querySelectorAll('.section-transition')].map(element => ({
    element, top: 0, progress: null
  }));

  /* Stage progress refers to the fraction of the pinned range that has scrolled past. */
  const state = { top: 0, offset: 0, distance: 1, step: 0, hidden: false, ready: false };
  const cache = { scrollMax: 1, heroHeight: 1 };

  const isStatic = () => reduce.matches || narrow.matches;

  const measureStage = () => {
    if (!stage || !track || !pin) return;
    state.hidden = stage.hidden || track.offsetHeight === 0;
    if (state.hidden) return;
    state.top = track.getBoundingClientRect().top + window.scrollY;
    const stickyTop = parseFloat(window.getComputedStyle(pin).top);
    state.offset = Number.isFinite(stickyTop) ? stickyTop : 0;
    state.distance = Math.max(1, track.offsetHeight - pin.offsetHeight);
  };

  const measurePage = () => {
    cache.scrollMax = Math.max(1, root.scrollHeight - window.innerHeight);
    cache.heroHeight = hero ? Math.max(1, hero.offsetHeight) : 1;
    const y = window.scrollY;
    transitions.forEach(transition => {
      transition.top = transition.element.getBoundingClientRect().top + y;
    });
  };

  const setStep = (step, focus = false) => {
    if (step === state.step) return;
    state.step = step;
    if (stage) stage.dataset.state = String(step);
    if (isStatic()) return;
    tabs.forEach((tab, index) => {
      const selected = index === step - 1;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      if (selected && focus) tab.focus({ preventScroll: true });
    });
  };

  /* All three panels are open on narrow or reduced-motion layouts, so the tab
     semantics are dropped there and the buttons become plain stage jumps. */
  const applySemantics = () => {
    if (!stage) return;
    const stat = isStatic();
    const list = stage.querySelector('.stage-tabs');
    if (list) list.setAttribute('role', stat ? 'group' : 'tablist');
    tabs.forEach((tab, index) => {
      const panel = document.getElementById(`stage-detail-${index + 1}`);
      const label = tab.textContent.replace(/^\s*\d+\s*/, '').trim();
      if (stat) {
        tab.removeAttribute('role');
        tab.removeAttribute('aria-selected');
        tab.removeAttribute('tabindex');
        if (panel) {
          panel.setAttribute('role', 'group');
          panel.setAttribute('aria-label', `${index + 1}. ${label}`);
          panel.removeAttribute('aria-labelledby');
          panel.removeAttribute('tabindex');
        }
      } else {
        tab.setAttribute('role', 'tab');
        tab.setAttribute('aria-selected', String(state.step === index + 1));
        tab.tabIndex = state.step === index + 1 ? 0 : -1;
        if (panel) {
          panel.setAttribute('role', 'tabpanel');
          panel.setAttribute('aria-labelledby', tab.id);
          panel.setAttribute('tabindex', '0');
          panel.removeAttribute('aria-label');
        }
      }
    });
  };

  const stageTargetProgress = step => (step === 1 ? 0.12 : step === 2 ? 0.44 : 0.84);

  const goToStep = step => {
    if (isStatic()) {
      const panel = document.getElementById(`stage-detail-${step}`);
      if (panel) panel.scrollIntoView({ behavior: reduce.matches ? 'auto' : 'smooth', block: 'start' });
      setStep(step);
      return;
    }
    if (!stage || state.hidden) return;
    const top = state.top - state.offset + stageTargetProgress(step) * state.distance;
    window.scrollTo({ top, behavior: reduce.matches ? 'auto' : 'smooth' });
    setStep(step);
  };

  /* Motion preference and the existing pause control both gate the hero handoff. */
  const motion = { paused: true };
  const syncMotion = () => {
    if (!hero) return;
    motion.paused = hero.dataset.motion !== 'running';
    if (reduce.matches) hero.style.setProperty('--hero-p', '0');
  };

  const update = () => {
    const y = window.scrollY;

    root.style.setProperty('--read', clamp(y / cache.scrollMax).toFixed(4));

    if (hero && !motion.paused) {
      hero.style.setProperty('--hero-p', clamp(y / cache.heroHeight).toFixed(3));
    }

    transitions.forEach(transition => {
      // Finish the trace as the next heading arrives in the reading area.
      const progress = reduce.matches ? 1 : clamp((y + innerHeight * .88 - transition.top) / (innerHeight * .48));
      if (progress === transition.progress) return;
      transition.progress = progress;
      transition.element.style.setProperty('--transition-progress', progress.toFixed(4));
      transition.element.classList.toggle('is-tracing', progress > 0 && progress < 1);
    });

    if (!stage || state.hidden || isStatic()) return;
    const progress = clamp((state.offset - (state.top - y)) / state.distance);
    stage.style.setProperty('--p', progress.toFixed(4));
    setStep(progress < 0.3 ? 1 : progress < 0.6 ? 2 : 3);
  };

  let frame = 0;
  const schedule = () => {
    if (frame) return;
    frame = window.requestAnimationFrame(() => {
      frame = 0;
      update();
    });
  };

  const remeasure = () => {
    measurePage();
    measureStage();
    schedule();
  };

  if (stage) {
    if (steps) steps.hidden = false;
    stage.dataset.state = '1';
    if (tabs.length) {
      tabs[0].tabIndex = 0;
      tabs.forEach((tab, index) => {        tab.addEventListener('click', () => goToStep(index + 1));
        tab.addEventListener('keydown', event => {
          if (isStatic()) return;
          const last = tabs.length - 1;
          let next = null;
          if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = index === last ? 0 : index + 1;
          else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = index === 0 ? last : index - 1;
          else if (event.key === 'Home') next = 0;
          else if (event.key === 'End') next = last;
          if (next === null) return;
          event.preventDefault();
          tabs[next].focus({ preventScroll: true });
          goToStep(next + 1);
        });
      });
    }
    remeasure();
    applySemantics();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(remeasure);
    addEventListener('load', remeasure, { once: true });
    addEventListener('resize', remeasure, { passive: true });
    addEventListener('pageshow', remeasure);
    addEventListener('orientationchange', remeasure);
    document.addEventListener('portfolio:filterchange', remeasure);
    document.addEventListener('visibilitychange', () => { if (!document.hidden) remeasure(); });
    if ('ResizeObserver' in window) {
      const observer = new ResizeObserver(remeasure);
      observer.observe(track);
      observer.observe(document.body);
    }
    const onModeChange = () => { applySemantics(); remeasure(); };
    reduce.addEventListener('change', onModeChange);
    narrow.addEventListener('change', onModeChange);
    addEventListener('hashchange', remeasure);
  }

  if (hero) {
    syncMotion();
    if ('MutationObserver' in window) {
      new MutationObserver(syncMotion).observe(hero, { attributes: true, attributeFilter: ['data-motion'] });
    }
    measurePage();
  }

  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', measurePage, { passive: true });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measurePage);
  measurePage();
  measureStage();
  update();
})();
