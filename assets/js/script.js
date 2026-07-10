document.addEventListener('DOMContentLoaded', () => {
  const navLinks = document.querySelectorAll('.nav a');

  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      navLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
    });
  });

  console.log('Tintorgal Info chargé avec succès !');
  console.log('Actualités fournies par Guineenews.org');
});
