const novaPoshtaForm = document.querySelector(".nova-poshta-form");
const ukrPoshtaForm = document.querySelector(".ukrposhta-form");

const forms = [novaPoshtaForm, ukrPoshtaForm];

const radioButtons = document.querySelector(".client-form__radio-buttons");

radioButtons.addEventListener("click", function (event) {
  if (event.target.name == "order-receiving") {
    for (let i = 0; i < forms.length; i++) {
      const form = forms[i];
      form.classList.add("hidden");

      const formInputs = form.querySelectorAll("input");
      for (let i = 0; i < formInputs.length; i++) {
        const input = formInputs[i];
        input.required = false;
      }
    }

    if (event.target.value == "nova_poshta") {
      novaPoshtaForm.classList.remove("hidden");
      var selectedForm = novaPoshtaForm;
    } else if (event.target.value == "ukrposhta") {
      ukrPoshtaForm.classList.remove("hidden");
      var selectedForm = ukrPoshtaForm;
    }

    if (selectedForm != undefined) {
      const formInputs = selectedForm
        .closest(".order-receiving-form")
        .querySelectorAll("input");
      console.log(selectedForm);
      for (let i = 0; i < formInputs.length; i++) {
        const input = formInputs[i];
        input.required = true;
      }
    }
  }
});
