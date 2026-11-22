/* Security Career Paths — Core UI: Theme, Search Modal, Mobile Drawer, TOC Scrollspy */
(function () {
  "use strict";

  const rootMeta = document.querySelector('meta[name="site-root"]');
  const SITE_ROOT = rootMeta ? rootMeta.getAttribute("content") : "./";

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  /* 1. Theme Toggle */
  const themeBtn = document.getElementById("theme-toggle");
  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    if (themeBtn) {
      themeBtn.setAttribute(
        "aria-label",
        theme === "dark" ? "Switch to light theme" : "Switch to dark theme"
      );
      themeBtn.textContent = theme === "dark" ? "☀" : "☾";
    }
  }
  const savedTheme = localStorage.getItem("scp-theme");
  const initialTheme =
    savedTheme ||
    (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light");
  applyTheme(initialTheme);

  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      const next =
        document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      localStorage.setItem("scp-theme", next);
      applyTheme(next);
    });
  }

  /* 2. Mobile Sidebar / Nav Drawer */
  const menuBtn = document.getElementById("menu-toggle");
  const sidebar = document.getElementById("docs-sidebar");
  if (menuBtn && sidebar) {
    menuBtn.addEventListener("click", function () {
      const open = sidebar.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("click", function (ev) {
      if (
        sidebar.classList.contains("open") &&
        !sidebar.contains(ev.target) &&
        !menuBtn.contains(ev.target)
      ) {
        sidebar.classList.remove("open");
        menuBtn.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* 3. Full-Text Search Modal */
  const searchTriggers = document.querySelectorAll("[data-open-search]");
  const backdrop = document.getElementById("search-backdrop");
  const searchInput = document.getElementById("search-input");
  const searchResults = document.getElementById("search-results");
  let searchIndex = null;
  let activeHit = -1;

  async function loadSearchIndex() {
    if (searchIndex) return searchIndex;
    try {
      const res = await fetch(SITE_ROOT + "data/search-index.json");
      searchIndex = await res.json();
    } catch (err) {
      searchIndex = [];
    }
    return searchIndex;
  }

  function makeSnippet(text, query) {
    const clean = text.replace(/\s+/g, " ").trim();
    if (!query) return clean.slice(0, 140) + (clean.length > 140 ? "…" : "");
    const idx = clean.toLowerCase().indexOf(query.toLowerCase());
    if (idx === -1) return clean.slice(0, 140) + (clean.length > 140 ? "…" : "");
    const start = Math.max(0, idx - 48);
    const end = Math.min(clean.length, idx + query.length + 92);
    return (start > 0 ? "…" : "") + clean.slice(start, end) + (end < clean.length ? "…" : "");
  }

  function renderHits(query) {
    if (!searchResults || !searchIndex) return;
    const q = query.trim().toLowerCase();
    const terms = q.split(/\s+/).filter(Boolean);
    activeHit = -1;

    let scored;
    if (!terms.length) {
      scored = searchIndex.slice(0, 10).map((item) => ({ item, score: 1 }));
    } else {
      scored = [];
      for (const item of searchIndex) {
        const titleL = item.title.toLowerCase();
        const metaL = (item.meta || "").toLowerCase();
        const bodyL = (item.body || "").toLowerCase();
        const hay = titleL + " " + metaL + " " + bodyL;
        if (!terms.every((t) => hay.includes(t))) continue;

        let score = 0;
        for (const t of terms) {
          if (titleL === t) score += 40;
          else if (titleL.startsWith(t)) score += 25;
          else if (titleL.includes(t)) score += 16;
          if (metaL.includes(t)) score += 10;
          if (bodyL.includes(t)) score += 4;
        }
        scored.push({ item, score });
      }
      scored.sort((a, b) => b.score - a.score);
    }

    if (!scored.length) {
      searchResults.innerHTML =
        '<div class="search-empty">No matches for "' +
        escapeHtml(query) +
        '". Try a path name, certification (e.g. OSCP, SecAI+), or acronym (e.g. SIEM, DPIA).</div>';
      return;
    }

    searchResults.innerHTML = scored
      .slice(0, 14)
      .map(function (entry) {
        const it = entry.item;
        const snippet = makeSnippet(it.summary || it.body || "", terms[0] || "");
        return (
          '<a class="search-hit" href="' +
          escapeHtml(SITE_ROOT + it.url) +
          '">' +
          '<div class="search-hit-top">' +
          '<span class="search-hit-title">' +
          escapeHtml(it.title) +
          "</span>" +
          '<span class="search-hit-type">' +
          escapeHtml(it.kind) +
          "</span>" +
          "</div>" +
          '<p class="search-hit-snippet">' +
          escapeHtml(snippet) +
          "</p>" +
          "</a>"
        );
      })
      .join("");
  }

  function openSearch() {
    if (!backdrop || !searchInput) return;
    backdrop.classList.add("open");
    backdrop.setAttribute("aria-hidden", "false");
    searchInput.focus();
    loadSearchIndex().then(function () {
      renderHits(searchInput.value);
    });
  }

  function closeSearch() {
    if (!backdrop) return;
    backdrop.classList.remove("open");
    backdrop.setAttribute("aria-hidden", "true");
  }

  searchTriggers.forEach(function (el) {
    el.addEventListener("click", openSearch);
  });

  if (backdrop) {
    backdrop.addEventListener("click", function (ev) {
      if (ev.target === backdrop) closeSearch();
    });
  }

  if (searchInput) {
    searchInput.addEventListener("input", function () {
      renderHits(searchInput.value);
    });
    searchInput.addEventListener("keydown", function (ev) {
      const hits = searchResults ? Array.from(searchResults.querySelectorAll(".search-hit")) : [];
      if (ev.key === "Escape") {
        closeSearch();
      } else if (ev.key === "ArrowDown" && hits.length) {
        ev.preventDefault();
        activeHit = (activeHit + 1) % hits.length;
        hits.forEach((h, i) => h.classList.toggle("active", i === activeHit));
        hits[activeHit].scrollIntoView({ block: "nearest" });
      } else if (ev.key === "ArrowUp" && hits.length) {
        ev.preventDefault();
        activeHit = activeHit <= 0 ? hits.length - 1 : activeHit - 1;
        hits.forEach((h, i) => h.classList.toggle("active", i === activeHit));
        hits[activeHit].scrollIntoView({ block: "nearest" });
      } else if (ev.key === "Enter" && hits.length) {
        const target = hits[activeHit >= 0 ? activeHit : 0];
        if (target) window.location.href = target.getAttribute("href");
      }
    });
  }

  document.addEventListener("keydown", function (ev) {
    const tag = (ev.target && ev.target.tagName) || "";
    const inField = tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT";
    if ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === "k") {
      ev.preventDefault();
      if (backdrop && backdrop.classList.contains("open")) closeSearch();
      else openSearch();
    } else if (ev.key === "/" && !inField) {
      ev.preventDefault();
      openSearch();
    } else if (ev.key === "Escape" && backdrop && backdrop.classList.contains("open")) {
      closeSearch();
    }
  });

  /* 4. Right-hand TOC Scrollspy */
  const tocLinks = Array.from(document.querySelectorAll(".toc a"));
  if (tocLinks.length && "IntersectionObserver" in window) {
    const headings = tocLinks
      .map((a) => document.getElementById(a.getAttribute("href").slice(1)))
      .filter(Boolean);
    const observer = new IntersectionObserver(
      function (entries) {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            const id = entry.target.id;
            tocLinks.forEach((a) =>
              a.classList.toggle("active", a.getAttribute("href") === "#" + id)
            );
          }
        }
      },
      { rootMargin: "-80px 0px -70% 0px", threshold: 0 }
    );
    headings.forEach((h) => observer.observe(h));
  }

  window.SCP = {
    SITE_ROOT: SITE_ROOT,
    escapeHtml: escapeHtml,
  };
})();
