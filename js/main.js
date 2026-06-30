// ============================================================
// main.js — interazioni minime, scritte come BEST PRACTICE
// (l'opposto degli anti-pattern visti nell'audit):
//  - stato di invio visibile
//  - input MAI cancellato in caso di errore
//  - feedback accessibile via aria-live
// In FASE 9 il form andrà collegato a un endpoint reale (es. Formspree,
// un'API, o un servizio email). Per ora simula l'invio.
// ============================================================

// Anno dinamico nel footer
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// Gestione form lead
const form = document.getElementById('lead-form');
const status = document.getElementById('form-status');

if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = form.querySelector('#email');
    const nome = form.querySelector('#nome');

    // Validazione semplice e gentile (Heuristic: prevenzione errori)
    if (!nome.value.trim() || !email.value.trim() || !email.checkValidity()) {
      setStatus('Controlla nome ed email, per favore.', 'err');
      (!nome.value.trim() ? nome : email).focus();
      return; // NB: NON svuotiamo il form
    }

    const btn = form.querySelector('button[type="submit"]');
    const originalLabel = btn.textContent;
    btn.disabled = true;
    btn.textContent = 'Invio…';
    setStatus('', null);

    try {
      // FASE 9: sostituire con la vera chiamata all'endpoint.
      await new Promise((r) => setTimeout(r, 600));
      setStatus('Grazie! Ti ricontattiamo a breve. ✅', 'ok');
      form.reset(); // reset SOLO dopo un successo confermato
    } catch (err) {
      // In caso di errore l'input resta: l'utente non riscrive nulla
      setStatus('Qualcosa è andato storto. Riprova.', 'err');
    } finally {
      btn.disabled = false;
      btn.textContent = originalLabel;
    }
  });
}

function setStatus(msg, state) {
  if (!status) return;
  status.textContent = msg;
  if (state) status.setAttribute('data-state', state);
  else status.removeAttribute('data-state');
}
