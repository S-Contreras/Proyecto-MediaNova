(() => {
  const form = document.getElementById('consentForm');
  const chkRequired = document.getElementById('chkDatosSalud');
  const options = document.querySelectorAll('.consent-option');

  if (!form || !chkRequired) return;

  const syncCardState = (checkbox) => {
    const card = checkbox.closest('.consent-option');
    if (!card) return;
    card.classList.toggle('is-checked', checkbox.checked);
    if (checkbox.checked) {
      card.classList.remove('is-invalid');
    }
  };

  options.forEach((card) => {
    const cb = card.querySelector('input[type="checkbox"]');
    if (!cb) return;
    syncCardState(cb);
    cb.addEventListener('change', () => syncCardState(cb));
  });

  form.addEventListener('submit', (e) => {
    if (!chkRequired.checked) {
      e.preventDefault();
      const card = chkRequired.closest('.consent-option');
      if (card) card.classList.add('is-invalid');
      chkRequired.focus();
    }
  });
})();