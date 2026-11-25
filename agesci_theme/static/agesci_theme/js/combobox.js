(function () {
  "use strict";

  // Il combobox di Bootstrap 6 (anche quello modificabile del widget InputChip)
  // scrive testi fissi in inglese senza un'opzione per cambiarli
  // (combobox.ts, 6.0.0-alpha.2): li traduciamo ogni volta che cambiano,
  // anche all'avvio con voci già selezionate.
  var TESTI = [
    [/^(\d+) selected$/, "$1 selezionate"],
    [/^1 chip selected for removal$/, "1 voce selezionata per la rimozione"],
    [/^(\d+) chips selected for removal$/, "$1 voci selezionate per la rimozione"],
    [/^Chip selection cleared$/, "Selezione annullata"],
    [/^Selected for removal$/, "Selezionata per la rimozione"],
    [/^Remove (.*)$/, "Rimuovi $1"]
  ];

  function traduci(testo) {
    for (var i = 0; i < TESTI.length; i++) {
      if (TESTI[i][0].test(testo)) {
        return testo.replace(TESTI[i][0], TESTI[i][1]);
      }
    }
    return testo;
  }

  function aggiorna(contenitore) {
    contenitore.querySelectorAll('.combobox-value, .menu + [role="status"]').forEach(function (elemento) {
      var tradotto = traduci(elemento.textContent);
      if (tradotto !== elemento.textContent) {
        elemento.textContent = tradotto;
      }
    });
    [[".combobox-control .chip-dismiss", "aria-label"], [".combobox-control .chip", "aria-description"]].forEach(function (coppia) {
      contenitore.querySelectorAll(coppia[0] + "[" + coppia[1] + "]").forEach(function (elemento) {
        var testo = elemento.getAttribute(coppia[1]);
        var tradotto = traduci(testo);
        if (tradotto !== testo) {
          elemento.setAttribute(coppia[1], tradotto);
        }
      });
    });
  }

  function osserva() {
    // Il genitore, non il combobox: l'annuncio [role="status"] è un fratello.
    var contenitori = new Set();
    document.querySelectorAll('[data-bs-toggle="combobox"]').forEach(function (elemento) {
      contenitori.add(elemento.parentElement);
    });
    contenitori.forEach(function (contenitore) {
      aggiorna(contenitore);
      new MutationObserver(function () {
        aggiorna(contenitore);
      }).observe(contenitore, {
        childList: true,
        characterData: true,
        subtree: true,
        attributes: true,
        attributeFilter: ["aria-label", "aria-description"]
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", osserva);
  } else {
    osserva();
  }
})();
