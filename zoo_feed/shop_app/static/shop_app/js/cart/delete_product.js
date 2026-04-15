$(document).ready(function () {
  $(document).on("click", ".delete-product", function (e) {
    e.preventDefault();
    var prodInCartPk = this.getAttribute("prod_in_cart_pk");
    var url = $('.url-del-prod-from-cart').val();
    var csrf_token = $('input[name=csrfmiddlewaretoken]').val();

    data = {
      prod_in_cart_pk: prodInCartPk,
      csrfmiddlewaretoken: csrf_token,
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
