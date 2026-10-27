(function () {
  var sidebar = document.getElementById('agSidebar');
  var toggle  = document.getElementById('agSidebarToggle');
  var key     = 'ag-sidebar-collapsed';
  if (!sidebar || !toggle) return;

  // Nessuna API Bootstrap: dal 3.0 (Bootstrap 6) la strategia "fixed" dei menu
  // si imposta con data-bs-strategy="fixed" nel markup (vedi partials/sidebar.html).
  if (localStorage.getItem(key) === '1') {
    sidebar.classList.add('ag-sidebar--collapsed');
    toggle.setAttribute('aria-expanded', 'false');
  }
  toggle.addEventListener('click', function () {
    var collapsed = sidebar.classList.toggle('ag-sidebar--collapsed');
    localStorage.setItem(key, collapsed ? '1' : '0');
    toggle.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
  });
}());
