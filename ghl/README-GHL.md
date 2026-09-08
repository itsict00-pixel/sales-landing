# Portare la landing su GoHighLevel — workflow "mix"

**Design statico = mio** (incollato come blocchi Code/HTML).
**Parti dinamiche = widget nativi GHL** (form, calendario, countdown…).

> Questi file in `ghl/` sono GENERATI da `build.py`. Non modificarli a mano:
> modifica i `blocks/`, rilancia `python3 build.py`, poi ri-incolla in GHL.

## 1) CSS — una volta sola
Copia TUTTO il contenuto di **`ghl/sl-styles.css`** e incollalo in:
`GHL → Sites/Funnels → (la pagina) → Settings → Custom CSS`
(in alternativa: un *Tracking Code* nel `<head>`).
È tutto scopato sotto `.sl`, quindi **non entra in conflitto** con le classi di GHL.

## 2) Sezioni di design — come blocchi Code/HTML
Per ogni sezione statica:
1. In GHL aggiungi una **Section** → dentro un elemento **Custom Code / HTML**.
2. Incolla il contenuto del file corrispondente in `ghl/`.
Ogni file è già avvolto in `<div class="sl">…</div>` → si stila da solo.

Ordine consigliato:
`10-hero` → `20-problema` → `30-come-funziona` → `40-benefici` → `50-testimonianze` → `60-offerta` → `70-faq` → `80-cta-finale`

`header.html` / `footer.html`: opzionali — di norma usi nav e footer **nativi** di GHL.

## 3) Widget dinamici — nativi GHL
- **Form / Booking:** nel blocco `60-offerta` c'è uno slot tratteggiato
  *"[ Inserisci qui la Form o il Calendario di GoHighLevel ]"*. Lì **non** usare HTML mio:
  trascina la **Form** o il **Calendar** di GHL → i lead entrano nel CRM e parte l'automazione.
- **Countdown, Popup, Chat, Video:** aggiungili come widget GHL dove vuoi, tra un blocco e l'altro.

## 4) Quando modifichi qualcosa
1. Edita il file in `blocks/` (o i token/stili in `css/`).
2. `python3 build.py`
3. Ri-incolla in GHL il blocco aggiornato (e il CSS solo se hai cambiato stili/token).

## Se un colore o un font NON si applica in GHL
Significa che uno stile di GHL è più forte. Dimmelo: alzo la specificità del
selettore (`.sl .x` → più specifico, o un `!important` mirato) e rigenero `sl-styles.css`.
