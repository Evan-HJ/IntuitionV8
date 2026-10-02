function autocomplete(input, options) {
  if (!input || !Array.isArray(options)) return;

  let currentFocus = -1;

  input.addEventListener("input", function () {
    closeAllLists();
    const value = this.value.trim();
    if (!value) return;

    currentFocus = -1;
    const list = document.createElement("div");
    list.id = `${this.id}-autocomplete-list`;
    list.className = "autocomplete-items";
    list.setAttribute("role", "listbox");
    this.parentNode.appendChild(list);

    options
      .filter((option) => option.toLowerCase().startsWith(value.toLowerCase()))
      .slice(0, 8)
      .forEach((option) => {
        const item = document.createElement("div");
        item.setAttribute("role", "option");

        const match = document.createElement("strong");
        match.textContent = option.slice(0, value.length);
        item.appendChild(match);
        item.appendChild(document.createTextNode(option.slice(value.length)));

        item.addEventListener("click", function () {
          input.value = option;
          closeAllLists();
        });
        list.appendChild(item);
      });
  });

  input.addEventListener("keydown", function (event) {
    const list = document.getElementById(`${this.id}-autocomplete-list`);
    const items = list ? list.getElementsByTagName("div") : [];

    if (event.key === "ArrowDown") {
      event.preventDefault();
      currentFocus += 1;
      addActive(items);
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      currentFocus -= 1;
      addActive(items);
    } else if (event.key === "Enter" && currentFocus > -1 && items[currentFocus]) {
      event.preventDefault();
      items[currentFocus].click();
    } else if (event.key === "Escape") {
      closeAllLists();
    }
  });

  function addActive(items) {
    if (!items.length) return;
    removeActive(items);
    if (currentFocus >= items.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = items.length - 1;
    items[currentFocus].classList.add("autocomplete-active");
  }

  function removeActive(items) {
    Array.from(items).forEach((item) => item.classList.remove("autocomplete-active"));
  }

  function closeAllLists(exception) {
    document.querySelectorAll(".autocomplete-items").forEach((list) => {
      if (list !== exception && input !== exception) list.remove();
    });
  }

  document.addEventListener("click", (event) => closeAllLists(event.target));
}
