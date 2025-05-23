# Ülevaade
Rakendus, mis aitab kasutajatel hallata veebilehtedel veedetud aega. Rakendus jälgib aktiivset lehitsemisaega, blokeerib (suunab ümber) häirivad saidid pärast ajapiiri täitumist ja esitab kasutajatele küsimusi saidile juurdepääsu taastamiseks. Ehitatud Pythoniga (PyQt5 GUI jaoks, Flask API jaoks) ja SQLite andmebaasiga.

## Tehniline külg
* Backend: Python, Flask, SQLite

* Frontend: PyQt5

* Brauseri integratsioon: Chrome'i laiend ja BingAPI, et kuvada iga päev erinev pilt

* AI: Ollama koos Mistral mudeliga küsimuste genereerimiseks, töötab lokaalselt

## Paigaldusjuhised
### Eeltingimused
* Python 3.8+

* Git

* Ollama paigaldatud ja töökorras (küsimuste genereerimiseks)

* Mistral masinõppeprogramm

## Paigaldamine
### Kausta kloonimine enda arvutisse:

```
git clone https://github.com/Astonnnn/Kvalifikatsioon
cd Kvalifikatsioon
```
### Loo ja aktiveeri virtuaalne keskkond (samas terminalis):
```
python -m venv env

env\Scripts\activate #Windows
source env/bin/activate #Mac/Linux
```
### Paigalda sõltuvused/moodulid (terminalis pead olema kloonitud kaustas ning virtuaalne keskkond aktiveeritud nt. (env) PS C:\Users\aston\Documents\kval>):
```
pip install -r requirements.txt
```

## Seadista Chrome'i laiendus:

* Ava <chrome://extensions/>  

* Lülita sisse "Arendaja režiim"/"Developer mode"

* Klõpsa "Laadi lahtipakitud"/"Load unpacked" ja vali chrome_extension kaust (tervikuna) (ENNE RAKENDUSE KÄIVITAMIST VÕIB CHROME EXTENSIONI SISSE-VÄLJA LÜLITADA, SEE LAKKAB TÖÖTAMAST, KUI SERVER POLE PIKALT TÖÖTANUD)

## Ollama paigaldamine

* Mine lehele <https://ollama.com/download> ning lae Ollama alla
* Ava cmd ning sisesta:
```ollama run mistral```
*Laadimise lõppemisel võid cmd sulgeda || vahepeal võib juhtuda, et on vaja küsimuse_genereerija failis panna ollama.exe asemel absoluutne failitee 

## Käivita rakendus:

```
python main.py #või jooksuta lihtsalt otse failist
```

## Kasutusjuhend
* Lisa veebileht koos ajalimiidiga andmebaasi

* Chrome'i laiend saadab sinu aktiivse veebilehe URL rakendusele ning rakendus võtab aega maha, kui see sinu andmebaasis

### Kui aeg täitub:

* Sait blokeeritakse

* Vasta genereeritud küsimusele blokeeringu eemaldamiseks

* Kõik veebilehti saab näha ja hallata veebilehtede lehelt
