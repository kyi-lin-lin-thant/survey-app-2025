
    document.addEventListener("DOMContentLoaded", function () {
        // toggle work for consent form button 
        const checkboxes = document.querySelectorAll('#consentForm input[type="checkbox"]');
        const btn = document.getElementById('proceedBtn');
        function updateButtonState() {
            const allChecked = [...checkboxes].every(c => c.checked);
            btn.disabled = !allChecked;
        }
        checkboxes.forEach(cb => {
            cb.addEventListener('change', updateButtonState);
        });
        btn.addEventListener('click', (e) => {
            e.preventDefault(); 
            window.location.href = "survey"; 
        });
        updateButtonState(); 

        // toggle 'Other' text inputs based on radio selection
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