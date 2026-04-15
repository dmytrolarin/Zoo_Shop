$(document).ready(function () {
  $(document).on("click", ".canel-filter-item", function (e) {
    e.preventDefault();
    var filterItemPk = this.getAttribute("filter_item_pk");
    var url = deleteFilterInUrl(filterItemPk, this.href);
    const priceRangeButton = document.querySelector('.filters__price-button');
    priceRangeButton.href = url;

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

function deleteFilterInUrl(pk, url) {
  var allParameters = url.split("?")[1].split("&");
  for (var i = 0; i < allParameters.length; i++) {
    if (allParameters[i].startsWith("filters=")) {
      let filtersItemsPks = allParameters[i].split("=")[1].split(",");
      filtersItemsPks.splice(filtersItemsPks.indexOf(pk), 1);
      if (filtersItemsPks.length > 0) {
        allParameters[i] = "filters=" + filtersItemsPks.join(",");
      } else {
        allParameters.splice(allParameters.indexOf(allParameters[i]), 1);
      }
      url = url.split("?")[0] + "?" + allParameters.join("&");
      return url;
    }
  }
}
