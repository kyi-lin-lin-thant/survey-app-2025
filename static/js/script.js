document.addEventListener('DOMContentLoaded', () => {
    /* =========================
       CONSENT PAGE (guarded)
       ========================= */
    const consentForm = document.getElementById('consentForm');
    const proceedBtn  = document.getElementById('proceedBtn');
  
    if (consentForm && proceedBtn) {
      const checks = consentForm.querySelectorAll('input[type="checkbox"]');
      const update = () => { proceedBtn.disabled = ![...checks].every(c => c.checked); };
      checks.forEach(c => c.addEventListener('change', update));
      proceedBtn.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = 'survey';
      });
      update();
    }
  
    /* =========================
       SURVEY PAGE (guarded)
       Toggle “Other” inputs
       ========================= */
    function bindOther(groupName, inputId) {
      const input = document.getElementById(inputId);
      const anyInGroup = document.querySelector(`input[name="${groupName}"]`);
      if (!input || !anyInGroup) return; // not this page, skip safely
  
      const update = () => {
        const selected = document.querySelector(`input[name="${groupName}"]:checked`);
        const show = !!(selected && selected.value === 'Other'); // value must be exactly "Other"
        // Use inline style so no CSS conflict can hide it
        input.style.display = show ? 'block' : 'none';
        input.required = show;
        if (!show) input.value = '';
        if (show) input.focus();
      };
  
      // React whenever that group changes
      document.addEventListener('change', (e) => {
        if (e.target && e.target.name === groupName && e.target.type === 'radio') {
          update();
        }
      });
  
      // Initial state on load
      update();
    }
  
    // Hook up the two groups (will noop on consent page)
    bindOther('status',  'statusOtherInput');
    bindOther('country', 'countryOtherInput');
  });
  