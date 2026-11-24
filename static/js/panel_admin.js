/* MediNova: menú, búsqueda en tablas y resaltado de secciones */
document.addEventListener("DOMContentLoaded", () => {
  // Menú móvil
  const navToggle = document.querySelector(".nav-toggle");
  const navMenu = document.getElementById("menu");
  if (navToggle && navMenu) {
    navToggle.addEventListener("click", () => {
      const expanded = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!expanded));
      navMenu.classList.toggle("is-open", !expanded);
    });
  }

  // Filtro en tablas
  const filterInput = document.getElementById("adminFilterInput");
  const clearBtn = document.getElementById("btnClearFilter");
  const filterCount = document.getElementById("adminFilterCount");
  const dataCards = Array.from(document.querySelectorAll(".data-card"));

  const applyFilter = () => {
    if (!filterInput) return;
    const query = filterInput.value.trim().toLowerCase();
    if (clearBtn) clearBtn.hidden = query.length === 0;

    let visibleRowsTotal = 0;

    dataCards.forEach((card) => {
      const rows = Array.from(card.querySelectorAll("tbody tr"));
      const dataRows = rows.filter((row) => !row.querySelector("td.empty"));
      if (dataRows.length === 0) return;

      let cardVisibleCount = 0;
      dataRows.forEach((row) => {
        const matches = query === "" || row.textContent.toLowerCase().includes(query);
        row.classList.toggle("is-hidden-row", !matches);
        if (matches) cardVisibleCount += 1;
      });

      visibleRowsTotal += cardVisibleCount;

      let noMatchRow = card.querySelector("tbody tr.no-match-row");
      const colCount = card.querySelectorAll("thead th").length || 1;

      if (cardVisibleCount === 0 && query !== "") {
        if (!noMatchRow) {
          noMatchRow = document.createElement("tr");
          noMatchRow.className = "no-match-row";
          noMatchRow.innerHTML = `<td class="empty" colspan="${colCount}">Sin coincidencias para "${query}".</td>`;
          card.querySelector("tbody").appendChild(noMatchRow);
        } else {
          noMatchRow.querySelector("td").textContent = `Sin coincidencias para "${query}".`;
          noMatchRow.classList.remove("is-hidden-row");
        }
      } else if (noMatchRow) {
        noMatchRow.classList.add("is-hidden-row");
      }
    });

    if (filterCount) {
      filterCount.textContent =
        query === "" ? "" : `${visibleRowsTotal} coincidencia(s) encontradas`;
    }
  };

  if (filterInput) filterInput.addEventListener("input", applyFilter);

  if (clearBtn && filterInput) {
    clearBtn.addEventListener("click", () => {
      filterInput.value = "";
      applyFilter();
      filterInput.focus();
    });
  }

  // Resaltar sección al navegar con #hash
  const highlightTarget = () => {
    const hash = window.location.hash;
    dataCards.forEach((card) => card.classList.remove("is-highlighted"));
    if (!hash) return;
    const target = document.querySelector(hash);
    if (target && target.classList.contains("data-card")) {
      target.classList.add("is-highlighted");
      window.setTimeout(() => target.classList.remove("is-highlighted"), 1600);
    }
  };

  window.addEventListener("hashchange", highlightTarget);
  highlightTarget();
});

// Cerrar ventanas flotantes de alerta (manual o automático)
  document.querySelectorAll(".toast-alert").forEach((toast) => {
    const closeBtn = toast.querySelector(".toast-close");
    const dismiss = () => {
      toast.classList.add("is-hiding");
      window.setTimeout(() => toast.remove(), 220);
    };
    if (closeBtn) closeBtn.addEventListener("click", dismiss);
    window.setTimeout(dismiss, 4500);
  });