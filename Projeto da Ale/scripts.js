function toggleMenu() {
  document.querySelector('.nav-links').classList.toggle('open');
}

document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    document.querySelector('.nav-links').classList.remove('open');
  });
});

function enviarFormulario(e) {
  e.preventDefault();
  const sucesso = document.getElementById('sucesso');
  sucesso.style.display = 'block';
  e.target.reset();
  setTimeout(() => { sucesso.style.display = 'none'; }, 5000);
}

// Navbar com sombra ao rolar
window.addEventListener('scroll', () => {
  const navbar = document.querySelector('.navbar');
  if (window.scrollY > 20) {
    navbar.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
  } else {
    navbar.style.boxShadow = 'none';
  }
});
