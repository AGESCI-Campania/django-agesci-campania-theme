// Avviso per i browser che non supportano le basi di Bootstrap 6.
// Script classico ed ES5 (niente moduli, const, arrow): deve girare proprio nei
// browser vecchi. Controlla le funzionalita', non la versione: i browser sotto
// i minimi ufficiali ma funzionanti (es. Safari 18) non vedono l'avviso.
(function () {
  "use strict";

  var CHIAVE = "ag-avviso-browser-chiuso";
  var TESTO = "Il tuo browser non è aggiornato: alcune parti di questa pagina potrebbero non funzionare. " +
    "Aggiornalo o usane uno più recente.";
  var script = document.currentScript;

  function supporta(proprieta, valore) {
    return !!(window.CSS && CSS.supports && CSS.supports(proprieta, valore));
  }

  function compatibile() {
    return supporta("color", "light-dark(red, blue)") &&
      supporta("color", "oklch(50% 0.1 20)") &&
      supporta("color", "color-mix(in oklch, red, blue)") &&
      supporta("container-type", "inline-size") &&
      CSS.supports("selector(:has(a))") &&
      "CSSLayerBlockRule" in window &&
      "HTMLDialogElement" in window &&
      "noModule" in document.createElement("script");
  }

  function mostra() {
    // Senza @layer il layout a viewport fisso (body overflow:hidden) renderebbe
    // irraggiungibile il contenuto: si torna allo scroll di pagina.
    document.body.style.height = "auto";
    document.body.style.overflow = "auto";

    try {
      if (sessionStorage.getItem(CHIAVE)) { return; }
    } catch (e) { /* storage bloccato: l'avviso si mostra comunque */ }

    var avviso = document.createElement("div");
    avviso.setAttribute("role", "alert");
    avviso.className = "ag-avviso-browser";
    // Stili qui e non nel CSS: non devono dipendere da Bootstrap.
    avviso.style.cssText = "display:flex;align-items:center;padding:12px 16px;background:#fff3cd;color:#332701;" +
      "border-bottom:1px solid #997404;font:16px/1.4 sans-serif";
    var testo = document.createElement("span");
    testo.style.cssText = "flex:1";
    testo.textContent = (script && script.getAttribute("data-testo")) || TESTO;
    var chiudi = document.createElement("button");
    chiudi.type = "button";
    chiudi.textContent = "Chiudi";
    chiudi.style.cssText = "margin-left:16px;padding:6px 12px;background:#332701;color:#fff;border:0;font:inherit;cursor:pointer";
    chiudi.onclick = function () {
      avviso.parentNode.removeChild(avviso);
      try { sessionStorage.setItem(CHIAVE, "1"); } catch (e) { /* storage bloccato */ }
    };
    avviso.appendChild(testo);
    avviso.appendChild(chiudi);
    document.body.insertBefore(avviso, document.body.firstChild);
  }

  if (!compatibile()) { mostra(); }
})();
