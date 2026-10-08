# Jazz Szervizkönyv

Karbantartási napló egy 2004-es Honda Jazz 1.2 i-DSI-hez (GD1). Prototípus.

## Mit tud

- **Az autó rajza:** a saját fotóról körberajzolva (`tools/trace.py`), a 13 alkatrészcsoport számozva. A szám színe mutatja az állapotot: rendben, hamarosan, lejárt, nincs adat. A számra vagy magára az alkatrészre koppintva megnyílik a csoport.
- **Napló:** cserék, javítások, ellenőrzések, tervezett teendők. Mindegyikhez tartozhat dátum, km-állás, költség, szerviz, leírás és csatolt számlafotó vagy PDF.
- **Papírok:** KGFB, CASCO, műszaki vizsga, autópálya-matrica, forgalmi, törzskönyv stb., lejárati figyelmeztetéssel.
- **Szervizterv:** km- és időalapú intervallumok, átírhatók. A kiinduló értékeket egyeztetni kell a szervizkönyvvel.
- **Mentés:** JSON-fájlba, a csatolmányokkal együtt, és visszatöltés.

## Kipróbálás

1. Nyisd meg az `index.html`-t egy böngészőben. Elég helyi szerverről is:
   `python3 -m http.server` és utána `http://localhost:8000`.
2. A ⚙ menüben a **Példaadatok betöltése** gombbal kitöltött állapotot kapsz.
   Ugyanott a **Példaadatok törlése** gombbal tüntetheted el őket.

Telefonon a legegyszerűbb, ha a GitHub Pages be van kapcsolva a repóra
(Settings → Pages → Branch). Ezután a böngésző menüjéből a kezdőképernyőre tehető, és offline is megnyílik.

## Hol vannak az adatok

- **Önálló webappként:** a böngésző IndexedDB-jében, csak azon az eszközön. Készíts időnként mentést.
- **Claude-oldalként (artifact):** az oldal saját adatbázisában és fájltárában, minden eszközről elérhetően.

## Fájlok

- `index.html`: maga az app (HTML, CSS, JS egy fájlban, keretrendszer nélkül)
- `manifest.webmanifest`, `icon.svg`, `sw.js`: telepíthetőség és offline működés
