const revealElements = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window && revealElements.length > 0) {
  const observer = new IntersectionObserver(
    (entries, observerRef) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observerRef.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );

  revealElements.forEach((element) => observer.observe(element));
} else {
  revealElements.forEach((element) => element.classList.add("is-visible"));
}

const stepperItems = document.querySelectorAll(".stepper li");
if ("IntersectionObserver" in window && stepperItems.length > 0) {
  const stepperObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-active");
        }
      });
    },
    { threshold: 0.35 }
  );

  stepperItems.forEach((item) => stepperObserver.observe(item));
}

const backTopButton = document.querySelector(".back-top");
if (backTopButton) {
  backTopButton.addEventListener("click", (event) => {
    event.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

const nav = document.querySelector(".nav");
const navToggle = document.getElementById("nav-menu-toggle");
const navLinksEl = document.getElementById("primary-nav-links");

function setNavMenuOpen(open) {
  if (!nav || !navToggle) return;
  nav.classList.toggle("is-open", Boolean(open));
  navToggle.setAttribute("aria-expanded", open ? "true" : "false");
  if (open && navLinksEl) {
    requestAnimationFrame(() => {
      navLinksEl.scrollTop = 0;
    });
  }
}

if (nav && navToggle && navLinksEl) {
  navToggle.addEventListener("click", () => {
    setNavMenuOpen(!nav.classList.contains("is-open"));
  });

  navLinksEl.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => setNavMenuOpen(false));
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && nav.classList.contains("is-open")) {
      setNavMenuOpen(false);
      navToggle.focus();
    }
  });

  const desktopNavMq = window.matchMedia("(min-width: 901px)");
  const closeNavOnDesktop = () => {
    if (desktopNavMq.matches) setNavMenuOpen(false);
  };
  desktopNavMq.addEventListener("change", closeNavOnDesktop);
  window.addEventListener("resize", closeNavOnDesktop);
}

// Equalize card heights within a grid (separate CSS grid row heights otherwise differ).
function equalizeGridCards(grid) {
  if (!grid) return;

  const cards = grid.querySelectorAll("article.card");
  if (cards.length === 0) return;

  const wideLayout = window.matchMedia("(min-width: 701px)").matches;
  if (!wideLayout) {
    cards.forEach((card) => {
      card.style.minHeight = "";
    });
    return;
  }

  cards.forEach((card) => {
    card.style.minHeight = "";
  });
  void grid.offsetHeight;

  let max = 0;
  cards.forEach((card) => {
    max = Math.max(max, card.offsetHeight);
  });

  const px = `${Math.ceil(max)}px`;
  cards.forEach((card) => {
    card.style.minHeight = px;
  });
}

function equalizeCardGrids() {
  CARD_GRID_SELECTORS.forEach((sel) =>
    equalizeGridCards(document.querySelector(sel))
  );
}

const CARD_GRID_SELECTORS = [
  "#features .grid.three-col",
  "#security .grid.three-col",
  "#findings .findings-grid",
  "#conclusion .conclusion-future-grid",
  "#objectives .grid.three-col",
  "#about .grid.two-col",
  "#stack .grid.two-col",
  "#in-action .grid.two-col",
  "#deliverables .deliverables-grid",
];

const CARD_GRID_SECTION_IDS = [
  "features",
  "security",
  "findings",
  "conclusion",
  "objectives",
  "about",
  "stack",
  "in-action",
  "deliverables",
];

function debounce(fn, ms) {
  let t;
  return function debounced(...args) {
    clearTimeout(t);
    t = window.setTimeout(() => fn.apply(this, args), ms);
  };
}

const equalizeCardGridsDebounced = debounce(equalizeCardGrids, 120);

const cardGrids = CARD_GRID_SELECTORS.map((sel) => document.querySelector(sel)).filter(
  Boolean
);

if (cardGrids.length > 0) {
  window.addEventListener("resize", equalizeCardGridsDebounced);
  window.addEventListener("load", equalizeCardGrids);
  requestAnimationFrame(() => {
    equalizeCardGrids();
    requestAnimationFrame(equalizeCardGrids);
  });

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(equalizeCardGrids).catch(() => {});
  }

  if ("ResizeObserver" in window) {
    const ro = new ResizeObserver(equalizeCardGridsDebounced);
    cardGrids.forEach((grid) => ro.observe(grid));
  }

  function observeRevealSection(id) {
    const section = document.getElementById(id);
    if (section && "MutationObserver" in window) {
      const mo = new MutationObserver(() => {
        if (section.classList.contains("is-visible")) {
          equalizeCardGrids();
        }
      });
      mo.observe(section, { attributes: true, attributeFilter: ["class"] });
    }
  }

  CARD_GRID_SECTION_IDS.forEach((id) => observeRevealSection(id));
}
