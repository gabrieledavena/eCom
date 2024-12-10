# eCom

Benvenuto in **eCom**, una piattaforma e-commerce completamente funzionale costruita con Django. Questo progetto permette agli utenti di sfogliare prodotti, effettuare ordini e lasciare recensioni per gli articoli acquistati.

## Funzionalità

- **Autenticazione Utenti**: Registrazione e login degli utenti, con ruoli separati per clienti e fornitori.
- **Profilo fornitore**: Esplora il profilo del fornitore.
- **Carrello**: Aggiungi articoli al carrello.
- **Gestione Ordini**: Effettua ordini e traccia lo stato, con possibilità di aggiornamento stato da parte dei fornitori.
- **Recensioni e Valutazioni**: I clienti possono lasciare recensioni e valutazioni per i prodotti acquistati.
- **Dashboard Fornitori**: I fornitori possono visualizzare e gestire i propri prodotti e ordini.

## Requisiti

- Python 3.8+
- Django 3.2+
- PostgreSQL (o SQLite per lo sviluppo)

## Installazione

Clonare il repository:

    git clone https://github.com/gabrieledavena/eCom.git

    cd eCom


Creare un ambiente virtuale Python e attivarlo:

    python3 -m venv venv
    source venv/bin/activate   # Su Windows usa venv\Scripts\activate

Installare le dipendenze:

    pip install -r requirements.txt

Eseguire le migrazioni del database:

    python manage.py migrate


Avviare il server di sviluppo:

    python manage.py runserver

Accedere all'applicazione all'indirizzo http://localhost:8000.

## Testing

Per eseguire i test, utilizzare il seguente comando:

    python manage.py test

I test coprono le principali applicazioni: cart, account, checkout, reviews e store
## Frameworks e Linguaggi utilizzati:

<p> <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> </a> <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> </p>