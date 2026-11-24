(() => {
  const form = document.getElementById('login-form');
  if (!form) return;

  const pass = document.getElementById('id_password');
  const reveal = form.querySelector('.reveal');
  const caps = document.getElementById('caps-hint');
  const submit = form.querySelector('.submit');
  const label = submit.querySelector('.submit-label');
  const textoInicial = label.textContent;

  // Mostrar u ocultar la contraseña (solo si hay JavaScript)
  reveal.hidden = false;
  reveal.addEventListener('click', () => {
    const mostrar = pass.type === 'password';
    pass.type = mostrar ? 'text' : 'password';
    reveal.textContent = mostrar ? 'Ocultar' : 'Mostrar';
    pass.focus();
  });

  // Aviso de Bloq Mayús
  const revisarMayusculas = (e) => {
    if (e.getModifierState) caps.hidden = !e.getModifierState('CapsLock');
  };
  pass.addEventListener('keydown', revisarMayusculas);
  pass.addEventListener('keyup', revisarMayusculas);
  pass.addEventListener('blur', () => { caps.hidden = true; });

  // Evita envíos dobles y muestra que se está procesando
  form.addEventListener('submit', () => {
    submit.classList.add('is-loading');
    submit.setAttribute('aria-busy', 'true');
    label.textContent = 'Iniciando sesión…';
    submit.disabled = true;
  });

  // Si el navegador restaura la página al volver atrás, restablece el botón
  window.addEventListener('pageshow', (e) => {
    if (e.persisted) {
      submit.classList.remove('is-loading');
      submit.removeAttribute('aria-busy');
      label.textContent = textoInicial;
      submit.disabled = false;
    }
  });
})();