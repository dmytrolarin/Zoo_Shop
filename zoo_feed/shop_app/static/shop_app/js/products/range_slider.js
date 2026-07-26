const priceFields = document.querySelectorAll(".inputs-prices input");
const rangeInput = document.querySelectorAll(".range-input input");
const progress = document.querySelector(".slider .progress");

function updateProgress(minValue, maxValue) {
  const absoluteMin = Number(rangeInput[0].min);
  const absoluteMax = Number(rangeInput[0].max);
  const rangeSize = absoluteMax - absoluteMin;

  if (rangeSize <= 0) {
    progress.style.left = "0%";
    progress.style.right = "0%";
    return;
  }

  progress.style.left = ((minValue - absoluteMin) / rangeSize) * 100 + "%";
  progress.style.right = 100 - ((maxValue - absoluteMin) / rangeSize) * 100 + "%";
}

updateProgress(Number(priceFields[0].value), Number(priceFields[1].value));

priceFields.forEach((input) => {
  input.addEventListener("input", (event) => {
    let minVal = parseInt(priceFields[0].value);
    let maxVal = parseInt(priceFields[1].value);

    if ((maxVal - minVal >= 0) && (maxVal <= rangeInput[0].max) && (rangeInput[0].min <= minVal)) {
      if (event.target.className === "price-min") {
        rangeInput[0].value = minVal;
      } else {
        rangeInput[1].value = maxVal;
      }
      updateProgress(minVal, maxVal);
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
      updateProgress(minVal, maxVal);
    }
  });
});
