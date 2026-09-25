(function () {
  var sidebar = document.getElementById('agSidebar');
  var toggle  = document.getElementById('agSidebarToggle');
  var key     = 'ag-sidebar-collapsed';
  if (!sidebar || !toggle) return;

  // Bootstrap (window.bootstrap, data-bs-*) oppure CoreUI (window.coreui,
  // data-coreui-*): vedi il template tag ag_js in agesci_tags.py.
  var ui = window.coreui || window.bootstrap;
  var prefix = window.coreui ? 'coreui' : 'bs';

  sidebar.querySelectorAll('[data-' + prefix + '-toggle="dropdown"]').forEach(function (el) {
    ui.Dropdown.getOrCreateInstance(el, {
      popperConfig: function (defaultConfig) {
        return Object.assign({}, defaultConfig, { strategy: 'fixed' });
      },
    });
  });

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
