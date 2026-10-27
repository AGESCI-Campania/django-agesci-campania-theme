(function () {
  "use strict";

  document.addEventListener("change", function (event) {
    var checkbox = event.target.closest(".ag-multiselect__checkbox");
    if (!checkbox) {
      return;
    }
    var container = checkbox.closest(".ag-multiselect");
    if (!container) {
      return;
    }
    var label = container.querySelector(".ag-multiselect__label");
    if (!label) {
      return;
    }
    var checked = container.querySelectorAll(".ag-multiselect__checkbox:checked");
    if (checked.length === 0) {
      label.textContent = label.getAttribute("data-placeholder");
    } else if (checked.length === 1) {
      var associata = container.querySelector('label[for="' + checked[0].id + '"]');
      label.textContent = associata ? associata.textContent : checked[0].value;
    } else {
      label.textContent = checked.length + " selezionati";
    }
  });
})();
