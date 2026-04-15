$(document).ready(function () {
  $(document).on("click", ".product__button-in-cart", function (e) {
    e.preventDefault();
    var buyProductForm = this.closest('.product__buy');
    var productPk = buyProductForm.querySelector(".product-pk").value;
    var productAmount = buyProductForm.querySelector(".amount-number").value;

    var url = buyProductForm.getAttribute('action');

    var csrf_token = buyProductForm.querySelector('[name="csrfmiddlewaretoken"]').value;

    var productBottom = buyProductForm.closest('.product__bottom');
    var packingPk = productBottom.querySelector('.packing-list__item.selected').getAttribute('packing_pk');

    
    
    data = {
        'product_pk': productPk,
        'product_amount': productAmount,
        'csrfmiddlewaretoken':csrf_token,
        'packing_pk': packingPk,
    }

    $.ajax({
      url: url,
      type: "POST",
      cache: true,
      data:data,
      success: function () {
        $(".link-cart").load(location.href + "  .link-cart");
        const popupSuccess = document.getElementById("popup-added-to-cart");
        popupOpen(popupSuccess);
      },
    });

  });
});
