(function () {
  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function linkify(value) {
    return String(value ?? "").replace(
      /(https?:\/\/[^\s<]+)/g,
      '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    );
  }

  function formatText(value) {
    return linkify(escapeHtml(value)).replace(/\n/g, "<br>");
  }

  function normalize(value) {
    return String(value ?? "").toLowerCase().trim();
  }

  function includesSearch(variable, query) {
    // Bewusst nur Variablennamen durchsuchen.
    // Kommentare, Gleichungen, Views und Dependencies werden nicht durchsucht,
    // damit die Trefferliste vorhersehbar und nicht zu breit wird.
    if (!query) return true;
    return normalize(variable.name).includes(normalize(query));
  }

  function uniqueSorted(values) {
    return Array.from(new Set(values.filter(Boolean))).sort((a, b) => a.localeCompare(b));
  }

  function table(headers, rows) {
    if (!rows.length) {
      return `<p class="vensim-empty">Keine Einträge gefunden.</p>`;
    }
    const head = `<thead><tr>${headers.map(h => `<th>${escapeHtml(h)}</th>`).join("")}</tr></thead>`;
    const body = `<tbody>${rows.map(row => `<tr>${row.map(cell => `<td>${escapeHtml(cell)}</td>`).join("")}</tr>`).join("")}</tbody>`;
    return `<table class="vensim-table">${head}${body}</table>`;
  }

  function block(title, content, cssClass = "") {
    return `
      <section class="vensim-block ${cssClass}">
        <h4>${escapeHtml(title)}</h4>
        <div class="vensim-block-content">${content}</div>
      </section>
    `;
  }

  function documentationSubblock(title, value) {
    if (!value || !String(value).trim()) return "";
    return `
      <div class="vensim-doc-subblock">
        <h5>${escapeHtml(title)}</h5>
        <div class="vensim-doc-text">${formatText(value)}</div>
      </div>
    `;
  }

  function documentationBlock(variable) {
    const parts = [];

    if (variable.documentationStatus) {
      parts.push(`
        <div class="vensim-doc-status-row">
          <span class="vensim-doc-status-label">Dokumentationsstatus</span>
          <span class="vensim-doc-status">${escapeHtml(variable.documentationStatus)}</span>
        </div>
      `);
    }

    parts.push(documentationSubblock("Vensim-Kommentar", variable.documentation));
    parts.push(documentationSubblock("Zweck", variable.purpose));
    parts.push(documentationSubblock("Modelllogik", variable.logic));
    parts.push(documentationSubblock("Annahme", variable.assumption));
    parts.push(documentationSubblock("Quelle", variable.source));
    parts.push(documentationSubblock("Kalibrierung", variable.calibration));
    parts.push(documentationSubblock("Interpretation", variable.interpretation));

    const content = parts.join("").trim();

    if (!content) {
      return `<p class="vensim-empty">Für diese Variable ist noch keine Dokumentation vorhanden.</p>`;
    }

    return content;
  }

  function dependencyBlocks(variable) {
    const upstreamRows = variable.upstream.map(source => [
      source,
      variable.name,
      `${source} wird in der Gleichung von ${variable.name} verwendet.`
    ]);

    const downstreamRows = variable.downstream.map(target => [
      variable.name,
      target,
      `${variable.name} wird in der Gleichung von ${target} verwendet.`
    ]);

    return `
      <div class="vensim-dependency-grid">
        <div class="vensim-dependency-card">
          <h5>Beeinflusst diese Variable</h5>
          <p class="vensim-help-text">Diese Input-Variablen stehen upstream der Fokusvariable.</p>
          ${table(["Input", "Fokusvariable", "Bedeutung"], upstreamRows)}
        </div>
        <div class="vensim-dependency-card">
          <h5>Wird von dieser Variable beeinflusst</h5>
          <p class="vensim-help-text">Diese Output-Variablen stehen downstream der Fokusvariable.</p>
          ${table(["Fokusvariable", "Output", "Bedeutung"], downstreamRows)}
        </div>
      </div>
    `;
  }

  function renderVariable(variable, options) {
    if (!variable) {
      return `<p class="vensim-empty">Keine Fokusvariable ausgewählt.</p>`;
    }

    const statusPill = variable.documentationStatus
      ? `<span class="vensim-pill vensim-pill-muted">Doku: ${escapeHtml(variable.documentationStatus)}</span>`
      : `<span class="vensim-pill vensim-pill-warning">Doku: offen</span>`;

    const pills = [
      `<span class="vensim-pill">${escapeHtml(variable.kind)}</span>`,
      `<span class="vensim-pill">${escapeHtml(variable.units || "ohne Einheit")}</span>`,
      `<span class="vensim-pill">Inputs: ${variable.upstream.length}</span>`,
      `<span class="vensim-pill">Outputs: ${variable.downstream.length}</span>`,
      statusPill
    ].join("");

    let html = `
      <div class="vensim-result-header">
        <h3>${escapeHtml(variable.name)}</h3>
        <div class="vensim-pill-row">${pills}</div>
      </div>
    `;

    // Reihenfolge bewusst: zuerst Grafik, danach Detailblöcke.
    if (options.graph) {
      html += block("Grafik", `<div class="vensim-graph">${variable.graphSvg || "<p class='vensim-empty'>Keine Grafik verfügbar.</p>"}</div>`);
    }

    if (options.units) {
      html += block("Einheiten und Typ", table(
        ["Variable", "Typ", "Einheit"],
        [[variable.name, variable.kind, variable.units || "-"]]
      ));
    }

    if (options.documentation) {
      html += block("Dokumentation", documentationBlock(variable));
    }

    if (options.equation) {
      html += block("Gleichung", `<pre class="vensim-equation"><code>${escapeHtml(variable.equation)}</code></pre>`);
    }

    if (options.dependencies) {
      html += block("Verbundene Variablen", dependencyBlocks(variable));
    }

    if (options.views) {
      const rows = variable.views.map(view => [variable.name, view]);
      html += block("View-Zuordnung", table(["Variable", "View"], rows));
    }

    return html;
  }

  function initVensimSearch() {
    const app = document.getElementById("vensim-variable-search");
    if (!app || !window.VENSIM_SEARCH_DATA) return;

    const allVariables = window.VENSIM_SEARCH_DATA.variables || [];
    // Technische Steuergrössen werden im Such-UI standardmässig ausgeblendet.
    const variables = allVariables.filter(variable => variable.kind !== "control");
    const kinds = uniqueSorted(variables.map(v => v.kind));
    const views = uniqueSorted(variables.flatMap(v => v.views));

    app.innerHTML = `
      <h3 class="vensim-search-title">Variablen-Suche</h3>
      <p class="vensim-search-subtitle">
        Suche nach Variablennamen, wähle eine Fokusvariable und blende anschliessend die gewünschten Blöcke ein oder aus. Technische Steuergrössen wie FINAL TIME, TIME STEP und SAVEPER sind in dieser Suche ausgeblendet.
      </p>

      <div class="vensim-search-controls">
        <div class="vensim-field vensim-field-wide">
          <label for="vensim-query">Suchbegriff</label>
          <input id="vensim-query" type="search" placeholder="z. B. Urban Land, Rent, Transport" value="Urban Land" autocomplete="off" />
        </div>

        <div class="vensim-field vensim-field-medium">
          <label for="vensim-variable-select">Fokusvariable</label>
          <select id="vensim-variable-select"></select>
        </div>

        <div class="vensim-field vensim-field-small">
          <label for="vensim-kind-filter">Typ</label>
          <select id="vensim-kind-filter">
            <option value="">Alle Typen</option>
            ${kinds.map(kind => `<option value="${escapeHtml(kind)}">${escapeHtml(kind)}</option>`).join("")}
          </select>
        </div>

        <div class="vensim-field vensim-field-small">
          <label for="vensim-view-filter">View</label>
          <select id="vensim-view-filter">
            <option value="">Alle Views</option>
            ${views.map(view => `<option value="${escapeHtml(view)}">${escapeHtml(view)}</option>`).join("")}
          </select>
        </div>

        <fieldset class="vensim-checkboxes">
          <legend>Anzeigen</legend>
          <div class="vensim-checkbox-grid">
            <label><input type="checkbox" data-option="graph" checked /> Grafik</label>
            <label><input type="checkbox" data-option="units" checked /> Einheiten</label>
            <label><input type="checkbox" data-option="documentation" checked /> Dokumentation</label>
            <label><input type="checkbox" data-option="equation" checked /> Gleichung</label>
            <label><input type="checkbox" data-option="dependencies" checked /> Verbundene Variablen</label>
            <label><input type="checkbox" data-option="views" checked /> Views</label>
          </div>
        </fieldset>
      </div>

      <div id="vensim-search-meta" class="vensim-search-meta"></div>
      <div id="vensim-search-output"></div>
    `;

    const queryInput = app.querySelector("#vensim-query");
    const variableSelect = app.querySelector("#vensim-variable-select");
    const kindFilter = app.querySelector("#vensim-kind-filter");
    const viewFilter = app.querySelector("#vensim-view-filter");
    const meta = app.querySelector("#vensim-search-meta");
    const output = app.querySelector("#vensim-search-output");
    const optionInputs = Array.from(app.querySelectorAll("input[data-option]"));

    function currentOptions() {
      const options = {};
      optionInputs.forEach(input => {
        options[input.dataset.option] = input.checked;
      });
      return options;
    }

    function filteredVariables() {
      const query = queryInput.value.trim();
      const kind = kindFilter.value;
      const view = viewFilter.value;

      return variables.filter(variable => {
        const matchesQuery = includesSearch(variable, query);
        const matchesKind = !kind || variable.kind === kind;
        const matchesView = !view || variable.views.includes(view);
        return matchesQuery && matchesKind && matchesView;
      });
    }

    function updateSelect(keepSelection = true) {
      const oldValue = variableSelect.value;
      const matches = filteredVariables();

      variableSelect.innerHTML = matches
        .map(variable => `<option value="${escapeHtml(variable.name)}">${escapeHtml(variable.name)} (${escapeHtml(variable.kind)})</option>`)
        .join("");

      if (keepSelection && matches.some(variable => variable.name === oldValue)) {
        variableSelect.value = oldValue;
      }

      meta.textContent = `${matches.length} Treffer von ${variables.length} dokumentationsrelevanten Variablen`;
      render();
    }

    function selectedVariable() {
      const selectedName = variableSelect.value;
      if (!selectedName) return null;
      return variables.find(variable => variable.name === selectedName) || null;
    }

    function render() {
      const variable = selectedVariable();
      output.innerHTML = renderVariable(variable, currentOptions());
    }

    queryInput.addEventListener("input", () => updateSelect(false));
    kindFilter.addEventListener("change", () => updateSelect(false));
    viewFilter.addEventListener("change", () => updateSelect(false));
    variableSelect.addEventListener("change", render);
    optionInputs.forEach(input => input.addEventListener("change", render));

    updateSelect(false);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initVensimSearch);
  } else {
    initVensimSearch();
  }
})();
