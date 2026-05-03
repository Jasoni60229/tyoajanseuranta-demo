# Työajanseuranta demo

Tämä projekti on yksinkertainen Chrome-selaimessa toimiva työajanseurantaohjelmiston demo. Ohjelma on tehty Pythonilla ja Flaskilla. Toteutus on tarkoitettu opiskelijaprojektin demoksi, ei valmiiksi tuotantojärjestelmäksi.

## Projektin tarkoitus

Sovelluksen tarkoituksena on näyttää, miten pienessä yrityksessä toimitusjohtaja ja työntekijät voisivat käyttää työajanseurantaa. Käyttäjiä on kaksi roolia:

- Toimitusjohtaja
- Työntekijä

Kirjautumisessa valitaan testirooli. Oikeaa käyttäjä- tai salasanojenhallintaa ei ole, koska se on rajattu pois projektista.

## Toteutetut ominaisuudet

### Kirjautuminen

- Käyttäjä voi valita roolin kirjautumisnäytöltä.
- Toimitusjohtaja voi kirjautua suoraan toimitusjohtajan näkymään.
- Työntekijä valitsee yhden viidestä testityöntekijästä.

### Työntekijän käyttöliittymä

Työntekijä voi:

- Aloittaa työajanseurannan.
- Lopettaa aloitetun työajanseurannan.
- Tarkastella aikaisempia työaikakirjauksiaan.

### Toimitusjohtajan käyttöliittymä

Toimitusjohtaja voi:

- Tarkastella työaikoja työntekijäkohtaisesti.
- Muokata työntekijöiden työaikakirjauksia.
- Tarkastella poikkeamia, esimerkiksi puuttuvia kirjauksia.
- Hyväksyä työaikakirjauksia yksittäin.
- Hyväksyä kaikki odottavat työaikakirjaukset kerralla.

## Rajaukset

Projektissa ei ole toteutettu:

- Integraatiota muihin järjestelmiin.
- Uusien työntekijöiden lisäämistä.
- Käyttäjienhallintaa.
- Salasanojenhallintaa.
- Varsinaista tietokantaa.

Tiedot ovat ohjelman muistissa. Kun sovellus käynnistetään uudelleen, tiedot palautuvat alkuperäiseen testidataan.

## Teknologiat

- Python 3
- Flask
- HTML
- CSS
- Chrome-selain

## Käyttöönotto

1. Lataa tai kloonaa Git-repo omalle koneelle.
2. Avaa komentorivi projektikansiossa.
3. Luo virtuaaliympäristö:

```bash
python -m venv venv
```

4. Ota virtuaaliympäristö käyttöön.

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

5. Asenna riippuvuudet:

```bash
pip install -r requirements.txt
```

6. Käynnistä sovellus:

```bash
python app.py
```

7. Avaa Chrome-selaimessa osoite:

```text
http://127.0.0.1:5000
```

## Testausohje

1. Avaa sovellus selaimessa.
2. Kirjaudu työntekijänä ja valitse testityöntekijä.
3. Aloita työaika.
4. Lopeta työaika.
5. Tarkista, että uusi kirjaus näkyy edellisissä kirjauksissa tilalla `odottaa`.
6. Kirjaudu ulos.
7. Kirjaudu toimitusjohtajana.
8. Avaa työaikojen hyväksyminen.
9. Hyväksy yksittäinen kirjaus tai kaikki kirjaukset kerralla.
10. Tarkista työntekijäkohtaisesta tarkastelusta, että tila muuttui hyväksytyksi.

## Projektin rakenne

```text
tyoajanseuranta_demo/
├── app.py
├── requirements.txt
├── README.md
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── login.html
    ├── employee.html
    ├── employee_entries.html
    ├── ceo_nav.html
    ├── ceo_employees.html
    ├── edit_entry.html
    ├── ceo_exceptions.html
    └── ceo_approvals.html
```

## Huomioita jatkokehitykseen

Jos sovellusta jatkokehitetään, siihen voisi lisätä oikean tietokannan, käyttäjätunnukset, salasanat, vientitoiminnon ja tarkemman raportoinnin. Tässä demossa keskityttiin projektin vaatimusten mukaiseen yksinkertaiseen ja selkeään toimintaan.
