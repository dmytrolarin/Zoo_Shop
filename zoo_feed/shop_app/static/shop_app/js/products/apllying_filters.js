$(document).ready(function () {
  $(document).on("click", ".apply-filter-item", function (e) {
    e.preventDefault();
    var url = this.href;

    if (this.hasAttribute("filter_item_pk")) {
      var allParameters = url.split("?")[1].split("&");
      for (var i = 0; i < allParameters.length; i++) {
        if (allParameters[i].startsWith("filters=")) {
          allParameters[i] =
            allParameters[i] + "," + this.getAttribute("filter_item_pk");
          url = url.split("?")[0] + "?" + allParameters.join("&");
          break;
        }
      }
    }

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

function setLocation(curLoc) {
  try {
    history.pushState(null, null, curLoc);
    return;
  } catch (e) {}
  location.hash = "#" + curLoc;
}
