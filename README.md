# Työajanseuranta Demo

## Käyttöönotto

1. Lataa projekti:

```bash
git clone https://github.com/KAYTTAJA/tyoajanseuranta-demo.git
```

2. Siirry projektikansioon:

```bash
cd tyoajanseuranta-demo
```

3. Asenna riippuvuudet:

```bash
pip install -r requirements.txt
```

4. Käynnistä sovellus:

```bash
python app.py
```

5. Avaa selain (Chrome):

```
http://127.0.0.1:5000
```

---

## Testausohje

### Kirjautuminen

* Sovelluksessa ei ole oikeaa tunnistautumista
* Valitse rooli:

  * Toimitusjohtaja
  * Työntekijä

---

### Työntekijä (testaus)

1. Valitse rooliksi **Työntekijä**
2. Aloita työaika painamalla **Aloita**
3. Lopeta työaika painamalla **Lopeta**
4. Tarkastele aiempia kirjauksia näkymässä

Testaa:

* Et voi lopettaa ilman aloitusta
* Useita kirjauksia tallentuu listaan

---

### Toimitusjohtaja (testaus)

1. Valitse rooliksi **Toimitusjohtaja**

Testaa seuraavat:

#### Työntekijäkohtainen tarkastelu

* Näet kaikkien työntekijöiden kirjaukset

#### Poikkeamat

* Näet puuttuvat kirjaukset (demo-logiikka)

#### Hyväksyntä

* Hyväksy yksittäinen kirjaus
* Hyväksy kaikki kirjaukset

#### Muokkaus

* Muokkaa työntekijän työaikoja (demo)

---

### Virhetilanteet

Testaa:

* Lopetus ilman aloitusta → virheilmoitus
* Tyhjät kirjaukset → ilmoitus

---

## Huomio

* Sovellus on demoversio
* Ei sisällä oikeaa käyttäjähallintaa
* Ei tallenna tietoja pysyvästi (muistiin)
