/* MediNova: comportamiento interactivo del aviso de privacidad */
document.addEventListener("DOMContentLoaded", () => {
  const progressBar = document.getElementById("readProgressBar");
  const printBtn = document.getElementById("btnPrintLegal");
  const tocLinks = Array.from(document.querySelectorAll("#legalToc a"));
  const sections = tocLinks
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);

  const optOutCheckbox = document.getElementById("optOutAdditional");
  const optOutStatus = document.getElementById("optOutStatus");

  const updateReadProgress = () => {
    if (!progressBar) return;
    const scrollTop = window.scrollY;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    const pct = maxScroll > 0 ? Math.min(100, Math.max(0, (scrollTop / maxScroll) * 100)) : 0;
    progressBar.style.width = `${pct}%`;
  };

  window.addEventListener("scroll", updateReadProgress, { passive: true });
  updateReadProgress();

  if ("IntersectionObserver" in window && sections.length > 0) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const targetHash = `#${entry.target.id}`;
          tocLinks.forEach((a) => {
            a.classList.toggle("is-active", a.getAttribute("href") === targetHash);
          });
        });
      },
      {
        rootMargin: "-18% 0px -65% 0px",
        threshold: 0,
      }
    );

    sections.forEach((sec) => observer.observe(sec));
  }

  if (printBtn) {
    printBtn.addEventListener("click", () => {
      window.print();
    });
  }

  if (optOutCheckbox && optOutStatus) {
    const storageKey = "medinova_optout_finalidades_adicionales";
    const savedValue = localStorage.getItem(storageKey) === "true";
    optOutCheckbox.checked = savedValue;

    if (savedValue) {
      optOutStatus.textContent =
        "Preferencia guardada: no se usarán sus datos para finalidades adicionales.";
    }

    optOutCheckbox.addEventListener("change", () => {
      const isChecked = optOutCheckbox.checked;
      localStorage.setItem(storageKey, String(isChecked));
      optOutStatus.textContent = isChecked
        ? "Preferencia guardada: no se usarán sus datos para finalidades adicionales."
        : "Preferencia actualizada: acepta finalidades adicionales no indispensables.";
    });
  }
});