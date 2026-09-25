// Layout CoreUI del tema AGESCI Campania.
// Va caricato PRIMA di coreui.bundle.min.js: CoreUI legge le classi della
// sidebar (sidebar-narrow-unfoldable) quando crea l'istanza al "load" della
// pagina, quindi lo stato salvato va ripristinato prima.
(function () {
  var KEY = 'ag-coreui-sidebar-unfoldable';
  var sidebar = document.getElementById('sidebar');

  if (sidebar) {
    try {
      if (localStorage.getItem(KEY) === '1') {
        sidebar.classList.add('sidebar-narrow-unfoldable');
      }
    } catch (e) { /* storage non disponibile: nessuna persistenza */ }

    // Toggler "unfoldable" in fondo alla sidebar: l'ordine rispetto
    // all'handler di CoreUI non è garantito, quindi si legge lo stato
    // effettivo della classe DOPO che CoreUI ha gestito il click.
    var toggler = sidebar.querySelector('[data-coreui-toggle="unfoldable"]');
    if (toggler) {
      toggler.addEventListener('click', function () {
        setTimeout(function () {
          var compressa = sidebar.classList.contains('sidebar-narrow-unfoldable');
          try { localStorage.setItem(KEY, compressa ? '1' : '0'); } catch (e) { /* ignora */ }
        }, 0);
      });
    }
  }

  // Hamburger nell'header: fuori dalla sidebar, quindi il data-api di
  // CoreUI (che ascolta solo dentro .sidebar) non lo gestisce.
  document.addEventListener('click', function (event) {
    var btn = event.target.closest('[data-ag-sidebar-toggle]');
    if (!btn || !window.coreui) return;
    var target = document.querySelector(btn.getAttribute('data-ag-sidebar-toggle'));
    if (target) window.coreui.Sidebar.getOrCreateInstance(target).toggle();
  });
}());
