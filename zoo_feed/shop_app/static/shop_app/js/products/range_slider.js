const priceFields = document.querySelectorAll(".inputs-prices input");
const rangeInput = document.querySelectorAll(".range-input input");
const progress = document.querySelector(".slider .progress");

let minVal = parseInt(priceFields[0].value);
let maxVal = parseInt(priceFields[1].value);
const difference = rangeInput[0].max - rangeInput[0].min;
progress.style.left = ((minVal- difference) / (rangeInput[0].max - difference) ) * 100 + "%";
progress.style.right = 100 - ((maxVal - difference) / (rangeInput[1].max- difference)) * 100 + "%";

priceFields.forEach((input) => {
  input.addEventListener("input", (event) => {
    let minVal = parseInt(priceFields[0].value);
    let maxVal = parseInt(priceFields[1].value);

    if ((maxVal - minVal >= 0) && (maxVal <= rangeInput[0].max) && (rangeInput[0].min <= minVal)) {
      const difference = rangeInput[0].max - rangeInput[0].min;
      if (event.target.className === "price-min") {
        rangeInput[0].value = minVal;
        progress.style.left = ((minVal- difference) / (rangeInput[0].max - difference) ) * 100 + "%";
      } else {
        rangeInput[1].value = maxVal;
        progress.style.right = 100 - ((maxVal - difference) / (rangeInput[1].max- difference)) * 100 + "%";
      }
    }
  });
});

rangeInput.forEach((input) => {
  input.addEventListener("input", (event) => {
    let minVal = parseInt(rangeInput[0].value);
    let maxVal = parseInt(rangeInput[1].value);

    if (maxVal - minVal < 0) {
      if (event.target.className === "range-min") {
        rangeInput[0].value = maxVal;
      } else {
        rangeInput[1].value = minVal;
      }
    } else {
      priceFields[0].value = minVal;
      priceFields[1].value = maxVal;
      const difference = rangeInput[0].max - rangeInput[0].min;
      progress.style.left = ((minVal- difference) / (rangeInput[0].max - difference) ) * 100 + "%";
      progress.style.right = 100 - ((maxVal - difference) / (rangeInput[1].max- difference)) * 100 + "%";
    }
  });
});
