/* Security Career Paths — Interactive Tools: Path Finder, Certs Explorer, Transition Map */
(function () {
  "use strict";

  const rootMeta = document.querySelector('meta[name="site-root"]');
  const SITE_ROOT = rootMeta ? rootMeta.getAttribute("content") : "./";

  function esc(str) {
    return String(str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function familyClass(family) {
    const f = (family || "").toLowerCase();
    if (f.includes("defend")) return "fam-defend";
    if (f.includes("attack")) return "fam-attack";
    if (f.includes("build")) return "fam-build";
    if (f.includes("govern")) return "fam-govern";
    if (f.includes("ai")) return "fam-ai";
    return "fam-leadership";
  }

  /* =========================================================================
     1. INTERACTIVE PATH FINDER (finder.html)
     ========================================================================= */
  const finderRoot = document.getElementById("path-finder-app");
  if (finderRoot) {
    const state = {
      workStyle: null,
      coding: null,
      onCall: null,
      background: null,
      entryPref: null,
    };

    const BACKGROUND_MAP = {
      "new-to-tech": {
        label: "New to tech / career changer",
        paths: [
          "security-operations",
          "governance-risk-compliance",
          "identity-access-management",
          "vulnerability-management",
        ],
        note: "Accessible entry point without prior engineering years",
      },
      "it-ops": {
        label: "IT support, sysadmin or networking",
        paths: [
          "security-operations",
          "vulnerability-management",
          "identity-access-management",
          "security-engineering-architecture",
          "ot-industrial-security",
        ],
        note: "Builds directly on your systems, directory or networking background",
      },
      "dev-data": {
        label: "Software or data engineering",
        paths: [
          "application-security",
          "detection-engineering",
          "ai-security-engineering",
          "vulnerability-research",
        ],
        note: "Leverages your coding and engineering habits directly",
      },
      "cloud-devops": {
        label: "Cloud, DevOps or platform engineering",
        paths: [
          "cloud-security",
          "security-engineering-architecture",
          "detection-engineering",
          "ai-security-engineering",
        ],
        note: "Carries over your IaC, cloud and automation skills",
      },
      "audit-legal": {
        label: "Audit, compliance, risk or legal",
        paths: ["governance-risk-compliance", "privacy", "ai-governance-assurance"],
        note: "Direct fit for regulatory, risk and assurance backgrounds",
      },
      "ml-ai": {
        label: "Data science or ML engineering",
        paths: ["ai-security-engineering", "ai-red-teaming", "ai-governance-assurance"],
        note: "Uses your knowledge of how models, data pipelines and agents work",
      },
      "industrial": {
        label: "Control, electrical or plant engineering",
        paths: ["ot-industrial-security", "security-engineering-architecture"],
        note: "Pairs your industrial and safety knowledge with security",
      },
      "in-security": {
        label: "Already working in security",
        paths: [
          "detection-engineering",
          "incident-response-forensics",
          "cloud-security",
          "security-engineering-architecture",
          "ai-security-engineering",
          "ai-red-teaming",
          "security-leadership",
        ],
        note: "Strong next step for practitioners moving sideways or up",
      },
    };

    const ON_CALL_HEAVY = new Set(["security-operations", "incident-response-forensics"]);

    fetch(SITE_ROOT + "data/paths.json")
      .then((r) => r.json())
      .then(function (paths) {
        const resultsEl = document.getElementById("finder-results");
        const choiceButtons = finderRoot.querySelectorAll(".choice-btn[data-q]");
        const resetBtn = document.getElementById("finder-reset");

        function renderResults() {
          const answered = Object.values(state).filter(Boolean).length;
          const scored = paths.map(function (p) {
            let score = 0;
            const reasons = [];

            if (state.workStyle && (p.work_styles || []).includes(state.workStyle)) {
              score += 35;
              reasons.push("Matches how you like to work");
            }
            if (state.coding) {
              if (p.coding_level === state.coding) {
                score += 26;
                reasons.push("Matches your coding preference");
              } else {
                const order = ["daily", "regularly", "occasionally", "rarely"];
                const diff = Math.abs(order.indexOf(p.coding_level) - order.indexOf(state.coding));
                if (diff === 1) score += 10;
              }
            }
            if (state.onCall === "office-hours") {
              if (!ON_CALL_HEAVY.has(p.slug)) {
                score += 14;
                reasons.push("Mostly predictable hours");
              } else {
                score -= 12;
              }
            } else if (state.onCall === "shifts-ok" && ON_CALL_HEAVY.has(p.slug)) {
              score += 14;
              reasons.push("Fits live operations and response");
            }
            if (state.background && BACKGROUND_MAP[state.background]) {
              const bg = BACKGROUND_MAP[state.background];
              if (bg.paths.includes(p.slug)) {
                score += 28;
                reasons.push(bg.note);
              }
            }
            if (state.entryPref === "beginner") {
              if (p.entry_accessible) {
                score += 22;
                reasons.push("Accessible entry point");
              } else {
                score -= 8;
              }
            } else if (state.entryPref === "specialist" && !p.entry_accessible) {
              score += 10;
            }

            return { path: p, score: score, reasons: reasons };
          });

          scored.sort((a, b) => b.score - a.score || a.path.title.localeCompare(b.path.title));

          if (answered === 0) {
            resultsEl.innerHTML =
              '<h2 style="font-family:var(--font-serif);margin:0 0 8px;">Your top matches</h2>' +
              '<p style="color:var(--ink-muted);margin:0 0 14px;font-size:0.93rem;">Select any answers on the left to rank all 18 paths. You can answer one question or all five.</p>' +
              '<div class="match-card"><p style="margin:0;color:var(--ink-secondary);font-size:0.9rem;">Not sure where to start? Try picking <strong>what kind of work draws you in</strong> and <strong>what you already know</strong>—those two questions narrow the field fastest.</p></div>';
            return;
          }

          const top = scored.slice(0, 3);
          const runners = scored.slice(3, 6);

          let html =
            '<h2 style="font-family:var(--font-serif);margin:0 0 6px;">Top matches for you</h2>' +
            '<p style="color:var(--ink-muted);margin:0 0 16px;font-size:0.88rem;">Based on ' +
            answered +
            " of 5 answers. Spend a weekend trying the free labs on two of these before committing.</p>";

          top.forEach(function (entry, idx) {
            const p = entry.path;
            html +=
              '<div class="match-card">' +
              '<div class="match-top">' +
              '<div><a class="match-title" href="' +
              esc(SITE_ROOT + p.url) +
              '">' +
              (idx + 1) +
              ". " +
              esc(p.title) +
              "</a></div>" +
              '<span class="badge ' +
              familyClass(p.family) +
              '">' +
              esc(p.family) +
              "</span>" +
              "</div>" +
              '<p style="margin:6px 0 8px;font-size:0.9rem;color:var(--ink-secondary);">' +
              esc(p.one_line) +
              "</p>" +
              '<div style="font-size:0.8rem;color:var(--ink-muted);">Typical entry: ' +
              esc(p.typical_entry) +
              "</div>";
            if (entry.reasons.length) {
              html +=
                '<div class="match-reasons">' +
                entry.reasons.map((r) => '<span class="reason-tag">' + esc(r) + "</span>").join("") +
                "</div>";
            }
            html += "</div>";
          });

          html +=
            '<div style="margin-top:16px;padding-top:14px;border-top:1px solid var(--border);">' +
            '<div style="font-size:0.78rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:var(--ink-muted);margin-bottom:8px;">Also worth a look</div>' +
            '<div class="neighbour-chips">' +
            runners
              .map(
                (r) =>
                  '<a class="chip-link" href="' +
                  esc(SITE_ROOT + r.path.url) +
                  '">' +
                  esc(r.path.title) +
                  "</a>"
              )
              .join("") +
            "</div></div>";

          resultsEl.innerHTML = html;
        }

        choiceButtons.forEach(function (btn) {
          btn.addEventListener("click", function () {
            const q = btn.getAttribute("data-q");
            const val = btn.getAttribute("data-val");
            if (state[q] === val) {
              state[q] = null;
              btn.setAttribute("aria-pressed", "false");
            } else {
              state[q] = val;
              finderRoot
                .querySelectorAll('.choice-btn[data-q="' + q + '"]')
                .forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
            }
            renderResults();
          });
        });

        if (resetBtn) {
          resetBtn.addEventListener("click", function () {
            Object.keys(state).forEach((k) => (state[k] = null));
            choiceButtons.forEach((b) => b.setAttribute("aria-pressed", "false"));
            renderResults();
          });
        }

        renderResults();
      });
  }

  /* =========================================================================
     2. FILTERABLE CERTIFICATIONS EXPLORER (certifications.html)
     ========================================================================= */
  const certsRoot = document.getElementById("certs-explorer-app");
  if (certsRoot) {
    fetch(SITE_ROOT + "data/certifications.json")
      .then((r) => r.json())
      .then(function (data) {
        const rows = data.entries || [];
        const searchEl = document.getElementById("cert-search");
        const familyEl = document.getElementById("cert-family");
        const levelBtns = certsRoot.querySelectorAll(".choice-btn[data-level]");
        const countEl = document.getElementById("cert-count");
        const tbody = document.getElementById("cert-tbody");
        let activeLevel = "all";

        function render() {
          const q = (searchEl.value || "").trim().toLowerCase();
          const fam = familyEl.value;
          const filtered = rows.filter(function (row) {
            if (fam !== "all" && row.family !== fam) return false;
            if (activeLevel !== "all" && row.level.toLowerCase() !== activeLevel) return false;
            if (q) {
              const hay = (
                row.name +
                " " +
                row.path_title +
                " " +
                row.family +
                " " +
                row.level
              ).toLowerCase();
              if (!hay.includes(q)) return false;
            }
            return true;
          });

          countEl.textContent =
            "Showing " + filtered.length + " of " + rows.length + " path certification entries";

          if (!filtered.length) {
            tbody.innerHTML =
              '<tr><td colspan="4" style="text-align:center;padding:24px;color:var(--ink-muted);">No matching certifications. Try clearing a filter or searching another term.</td></tr>';
            return;
          }

          tbody.innerHTML = filtered
            .map(function (r) {
              const lvlCls = "level-" + r.level.toLowerCase();
              return (
                "<tr>" +
                '<td><strong>' +
                esc(r.name) +
                "</strong></td>" +
                '<td><span class="level-badge ' +
                lvlCls +
                '">' +
                esc(r.level) +
                "</span></td>" +
                '<td><a href="' +
                esc(SITE_ROOT + r.path_url) +
                '">' +
                esc(r.path_title) +
                "</a></td>" +
                '<td><span class="badge ' +
                familyClass(r.family) +
                '">' +
                esc(r.family) +
                "</span></td>" +
                "</tr>"
              );
            })
            .join("");
        }

        searchEl.addEventListener("input", render);
        familyEl.addEventListener("change", render);
        levelBtns.forEach(function (btn) {
          btn.addEventListener("click", function () {
            activeLevel = btn.getAttribute("data-level");
            levelBtns.forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
            render();
          });
        });

        render();
      });
  }

  /* =========================================================================
     3. INTERACTIVE CAREER TRANSITION MAP (map.html)
     ========================================================================= */
  const mapRoot = document.getElementById("transition-map-app");
  if (mapRoot) {
    Promise.all([
      fetch(SITE_ROOT + "data/paths.json").then((r) => r.json()),
      fetch(SITE_ROOT + "data/transitions.json").then((r) => r.json()),
    ]).then(function ([paths, transitionsData]) {
      const bySlug = {};
      paths.forEach((p) => (bySlug[p.slug] = p));
      const moves = transitionsData.moves || [];

      const boardEl = document.getElementById("map-board");
      const inspectorEl = document.getElementById("map-inspector");
      const FAMILY_ORDER = [
        "Defend",
        "Attack and assess",
        "Build",
        "Govern",
        "AI security",
        "Leadership",
      ];

      boardEl.innerHTML = FAMILY_ORDER.map(function (fam) {
        const items = paths.filter((p) => p.family === fam);
        return (
          '<div class="map-family-row">' +
          '<h3 class="map-family-title">' +
          esc(fam) +
          "</h3>" +
          '<div class="map-nodes">' +
          items
            .map(
              (p) =>
                '<button type="button" class="map-node" data-slug="' +
                esc(p.slug) +
                '">' +
                esc(p.title) +
                "</button>"
            )
            .join("") +
          "</div></div>"
        );
      }).join("");

      const nodeButtons = Array.from(boardEl.querySelectorAll(".map-node"));

      function selectPath(slug) {
        const p = bySlug[slug];
        if (!p) return;
        const neighSet = new Set(p.neighbours || []);

        nodeButtons.forEach(function (btn) {
          const s = btn.getAttribute("data-slug");
          btn.classList.toggle("is-selected", s === slug);
          btn.classList.toggle("is-neighbour", neighSet.has(s));
          btn.classList.toggle("is-dimmed", s !== slug && !neighSet.has(s));
        });

        const relatedMoves = moves.filter(
          (m) =>
            (m.from_slugs || []).includes(slug) || (m.to_slugs || []).includes(slug)
        );

        let html =
          '<span class="badge ' +
          familyClass(p.family) +
          '">' +
          esc(p.family) +
          "</span>" +
          "<h2>" +
          esc(p.title) +
          "</h2>" +
          '<p style="color:var(--ink-secondary);margin:0 0 14px;font-size:0.93rem;">' +
          esc(p.one_line) +
          "</p>" +
          '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px;">' +
          '<span class="meta-pill">Entry: ' +
          esc(p.typical_entry) +
          "</span>" +
          '<span class="meta-pill">Coding: ' +
          esc(p.coding_label) +
          "</span>" +
          "</div>" +
          '<a class="btn btn-primary" style="width:100%;margin-bottom:18px;" href="' +
          esc(SITE_ROOT + p.url) +
          '">Read full path guide →</a>' +
          '<div style="font-size:0.76rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:var(--ink-muted);margin-bottom:8px;">Direct neighbouring paths (' +
          (p.neighbours || []).length +
          ")</div>" +
          '<div class="neighbour-chips" style="margin-bottom:18px;">' +
          (p.neighbours || [])
            .map(function (ns) {
              const np = bySlug[ns];
              if (!np) return "";
              return (
                '<button type="button" class="chip-link" data-jump="' +
                esc(ns) +
                '" style="cursor:pointer;font-family:var(--font-sans);">' +
                esc(np.title) +
                "</button>"
              );
            })
            .join("") +
          "</div>";

        if (relatedMoves.length) {
          html +=
            '<div style="font-size:0.76rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:var(--ink-muted);margin-bottom:8px;">Documented career transitions</div>';
          relatedMoves.forEach(function (m) {
            html +=
              '<div class="transition-item">' +
              '<div style="margin-bottom:4px;"><strong>' +
              esc(m.from_label) +
              " → " +
              esc(m.to_label) +
              "</strong></div>" +
              '<div style="color:var(--ink-secondary);margin-bottom:3px;"><strong>Carries over:</strong> ' +
              esc(m.carries_over) +
              "</div>" +
              '<div style="color:var(--ink-muted);"><strong>What to add:</strong> ' +
              esc(m.to_add) +
              "</div></div>";
          });
        }

        inspectorEl.innerHTML = html;
        inspectorEl.querySelectorAll("[data-jump]").forEach(function (b) {
          b.addEventListener("click", function () {
            selectPath(b.getAttribute("data-jump"));
          });
        });
      }

      nodeButtons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          selectPath(btn.getAttribute("data-slug"));
        });
      });

      const initialSlug =
        (window.location.hash && bySlug[window.location.hash.slice(1)]
          ? window.location.hash.slice(1)
          : "security-operations");
      selectPath(initialSlug);
    });
  }
})();
