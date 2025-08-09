// JavaScript to toggle 'Other' text inputs based on radio selection

    document.addEventListener("DOMContentLoaded", function () {
        const statusOtherRadio = document.getElementById("statusOtherRadio");
        const statusOtherInput = document.getElementById("statusOtherInput");

        const countryOtherRadio = document.getElementById("countryOtherRadio");
        const countryOtherInput = document.getElementById("countryOtherInput");

        // Helper function to toggle visibility of "Other" input fields
        function toggleOtherInput(radio, input) {
            if (radio.checked) {
            input.classList.add("visible");
            input.required = true;
            input.focus();
            } else {
            input.classList.remove("visible");
            input.required = false;
            input.value = "";
            }
        }

        // Watch all status radios to toggle 'Other' input
        const statusRadios = document.querySelectorAll('input[name="status"]');
        statusRadios.forEach(radio => {
            radio.addEventListener("change", () => {
            toggleOtherInput(statusOtherRadio, statusOtherInput);
            });
        });

        // Watch all country radios to toggle 'Other' input
        const countryRadios = document.querySelectorAll('input[name="country"]');
        countryRadios.forEach(radio => {
            radio.addEventListener("change", () => {
            toggleOtherInput(countryOtherRadio, countryOtherInput);
            });
        });

        // Initialize on page load
        toggleOtherInput(statusOtherRadio, statusOtherInput);
        toggleOtherInput(countryOtherRadio, countryOtherInput);
    });