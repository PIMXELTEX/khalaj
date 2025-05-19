document.addEventListener('DOMContentLoaded', function() {
  // Loading functionality
  const loadingOverlay = document.getElementById('loading-overlay');
  
  // Hide loading overlay when page is fully loaded
  window.addEventListener('load', function() {
    setTimeout(() => {
      loadingOverlay.classList.add('hidden');
    }, 500); // Add a small delay for smoother transition
  });

  // Show loading overlay when navigating between pages
  document.addEventListener('click', function(e) {
    if (e.target.tagName === 'A' && !e.target.classList.contains('social-icon')) {
      loadingOverlay.classList.remove('hidden');
    }
  });

  // Show loading overlay when submitting forms
  document.addEventListener('submit', function(e) {
    loadingOverlay.classList.remove('hidden');
  });

  const burgerMenu = document.querySelector('.burger-menu');
  const navList = document.querySelector('.nav-list');
  const body = document.body;

  burgerMenu.addEventListener('click', function() {
      burgerMenu.classList.toggle('active');
      navList.classList.toggle('active');
      body.style.overflow = navList.classList.contains('active') ? 'hidden' : '';
  });

  // Close menu when clicking outside
  document.addEventListener('click', function(event) {
      if (!event.target.closest('.nav-list') && !event.target.closest('.burger-menu')) {
          burgerMenu.classList.remove('active');
          navList.classList.remove('active');
          body.style.overflow = '';
      }
  });

  // Close menu when clicking on a link
  const navLinks = document.querySelectorAll('.nav-list a');
  navLinks.forEach(link => {
      link.addEventListener('click', function() {
          burgerMenu.classList.remove('active');
          navList.classList.remove('active');
          body.style.overflow = '';
      });
  });
});