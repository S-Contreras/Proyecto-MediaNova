const toggle = document.querySelector('.nav-toggle');
const menu = document.getElementById('menu');

if (toggle && menu) {
  toggle.addEventListener('click', () => {
    const abierto = menu.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', abierto);
  });
}