function switchPacking() {
  let allPackings = this.parentElement.children;
  if (this.classList.contains("selected") != true) {
    for (let i = 0, len = allPackings.length; i < len; i++) {
      if (allPackings[i] == this) {
        this.classList.add("selected");
      } else {
        allPackings[i].classList.remove("selected");
      }
    }

    let mainInfoBlock = this.closest(".center-block__main-info");
    let currentPrice = mainInfoBlock.querySelector(".product__currently-price");
    let oldPrice = mainInfoBlock.querySelector(".product__old-price");

    currentPrice.innerHTML = this.getAttribute("current_price") + " USD";
    if (this.getAttribute("old_price") != "none") {
      oldPrice.innerHTML = this.getAttribute("old_price") + " USD";
    } else {
      oldPrice.innerHTML = "";
    }
  }
}

function setPackingsList() {
  const packingButtons = document.querySelectorAll(".packing-list__item");
  for (let i = 0, len = packingButtons.length; i < len; i++) {
    packingButtons[i].addEventListener("click", switchPacking);
  }
}

setPackingsList();
