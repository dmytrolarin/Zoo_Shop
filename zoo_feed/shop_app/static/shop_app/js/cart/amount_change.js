function amountPlus(button) {
  let amountField = button.previousElementSibling;
  amountField.value = Number(amountField.value) + 1;
}

function amountMinus(button) {
  let amountField = button.nextElementSibling;
  if (Number(amountField.value) > 1) {
    amountField.value = Number(amountField.value) - 1;
  }
}
productsWrapper = document.querySelector('.products-wrapper');

productsWrapper.addEventListener("click", function (event) {
  if (event.target.classList.contains('amount-plus')) {
    amountPlus(event.target);
  } else if (event.target.classList.contains('amount-minus')){
    amountMinus(event.target);
  }
});

$(document).ready(function () {
  $(document).on("click", ".change-amount", function (e) {
    e.preventDefault();
    const productAmountBlock = e.target.closest('.product__amount');
    const productAmountInput = productAmountBlock.querySelector('.amount-number');
    const updatedAmount = productAmountInput.value;
    const prodInCartPk = productAmountInput.getAttribute('prod_in_cart_pk');
    const csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    const url = $('.url-udpate-amount-prod-in-cart').val();

    data = {
      prod_in_cart_pk: prodInCartPk,
      csrfmiddlewaretoken: csrfToken,
      updated_amount: updatedAmount,
    };

    $.ajax({
      url: url,
      type: "POST",
      data: data,
      success: function () {
        $(".products-wrapper").load(location.href + "  .products-wrapper");
        $(".link-cart").load(location.href + "  .link-cart");
      },
    });
  });
});

