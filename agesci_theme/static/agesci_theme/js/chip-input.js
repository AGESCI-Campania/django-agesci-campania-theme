(function () {
  "use strict";

  // Il chip input di Bootstrap 6 non crea un campo da inviare col form:
  // a ogni modifica (evento change.bs.chips, con l'elenco in event.values)
  // copiamo i valori, uniti da virgola, nell'<input type="hidden"> del
  // widget InputChip (agesci_theme/forms/input_chip.html).
  document.addEventListener("change.bs.chips", function (event) {
    var contenitore = event.target.closest("[data-ag-chip-input]");
    if (!contenitore) {
      return;
    }
    var campo = contenitore.querySelector('input[type="hidden"]');
    if (campo) {
      campo.value = (event.values || []).join(",");
    }
  });
})();
