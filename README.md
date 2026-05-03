# Työajanseuranta Demo

## Käyttöönotto

### 1. Lataa projekti

1. Mene projektin sivulle GitHub
2. Klikkaa **Code** → **Download ZIP**
3. Tallenna tiedosto koneellesi

---

### 2. Pura ZIP-tiedosto

* Mene latauksiin
* Klikkaa zip-tiedostoa hiiren oikealla
* Valitse **Pura kaikki (Extract All)**

Saat kansion, esim:

```
tyoajanseuranta-demo-main
```

---

### 3. Avaa kansio komentokehotteessa

1. Avaa kansio
2. Klikkaa kansion sisällä hiiren oikealla
3. Valitse:

   * **Open in Terminal** / **Avaa PowerShell täällä**

---

### 4. Asenna riippuvuudet

```
pip install flask
```

(Tai vaihtoehtoisesti:)

```
pip install -r requirements.txt
```

---

### 5. Käynnistä sovellus

```
python app.py
```

---

### 6. Avaa selain (Chrome)

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
