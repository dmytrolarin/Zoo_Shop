$(document).ready(function () {
  $(document).on("click", ".filters__price-button", function (e) {
    e.preventDefault();
    var minPrice = document.querySelector(".price-min").value;
    var maxPrice = document.querySelector(".price-max").value;
    var url = setPriceRangeInUrl(this.href, minPrice, maxPrice);

    $.ajax({
      url: url,
      type: "GET",
      cache: true,
      success: function () {
        $(".list-products").load(location.href + "  .product");
        $(".filters__parametres").load(location.href + "  .parameter");
      },
    });

    setLocation(url);
  });
});

function setPriceRangeInUrl(url, minPrice, maxPrice) {
  var allParameters = url.split("?")[1].split("&");
  for (var i = 0; i < allParameters.length; i++) {
    if (allParameters[i].startsWith("price_range=")) {
      let prices = allParameters[i].split("=")[1].split(",");
      prices[0] = minPrice;
      prices[1] = maxPrice;
      allParameters[i] = "price_range=" + minPrice + "," + maxPrice;
      url = url.split("?")[0] + "?" + allParameters.join("&");
      return url;
    }
  }
  url += "&price_range=" + minPrice + "," + maxPrice;
  return url;
}
