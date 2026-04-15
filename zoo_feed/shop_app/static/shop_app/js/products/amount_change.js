function amountPlus() {
  let amountField = this.previousElementSibling;
  amountField.value = Number(amountField.value) + 1;
}

function amountMinus() {
  let amountField = this.nextElementSibling;
  if (Number(amountField.value) > 1) {
    amountField.value = Number(amountField.value) - 1;
  }
}

function setAmountButtonsList() {
  const amountPlusButtons = document.querySelectorAll(".amount-plus");
  const amountMinusButtons = document.querySelectorAll(".amount-minus");
  for (let i = 0, len = amountPlusButtons.length; i < len; i++) {
    amountPlusButtons[i].addEventListener("click", amountPlus);
    amountMinusButtons[i].addEventListener("click", amountMinus);
  }
}

setAmountButtonsList();
