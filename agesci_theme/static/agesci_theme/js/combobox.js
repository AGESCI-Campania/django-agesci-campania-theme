(function () {
  "use strict";

  // Il combobox multiplo di Bootstrap 6 scrive nel bottone "<n> selected",
  // testo fisso in inglese senza un'opzione per cambiarlo
  // (Combobox._updateToggleText, 6.0.0-alpha.1): lo traduciamo ogni volta
  // che cambia, anche all'avvio con voci già selezionate.
  var INGLESE = /^(\d+) selected$/;

  function traduci(elemento) {
    var trovato = INGLESE.exec(elemento.textContent);
    if (trovato) {
      elemento.textContent = trovato[1] + " selezionate";
    }
  }

  function osserva() {
    document.querySelectorAll('[data-bs-toggle="combobox"] .combobox-value').forEach(function (elemento) {
      traduci(elemento);
      new MutationObserver(function () {
        traduci(elemento);
      }).observe(elemento, { childList: true, characterData: true, subtree: true });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", osserva);
  } else {
    osserva();
  }
})();
