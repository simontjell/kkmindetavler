# kkmindetavler

Interaktivt kort over mindetavler i København og på Frederiksberg, bygget ud fra Københavns Bibliotekers liste.

- `index.html` – kortet (Leaflet). Åbnes direkte i en browser.
- `mindetavler-kbh.kml` – de samme punkter til Google My Maps, Google Earth, Organic Maps m.fl.

Seneste dataudtræk: **16. november 2026** – 291 tavler på 269 steder.

## Kilde

Københavns Biblioteker, "Bag om København": <https://bibliotek.kk.dk/din/bag-om-kobenhavn/mindetavler>

Listen er oprindeligt udarbejdet af Bjørn Westerbeek Dahl og vedligeholdes af biblioteket. Oversigtssiden har ingen tavler selv; de ligger på 14 undersider, én pr. bydel (`…/mindetavler/<slug>`):

| Bydel | Slug | Tavler 16/11 2026 |
|---|---|---|
| Bispebjerg | `bispebjerg` | 8 |
| Brønshøj-Husum | `bronshoj-husum` | 5 (heraf 1 flyttet til Sundby, se rettelser) |
| Christianshavn | `christianshavn` | 25 |
| Frederiksberg | `frederiksberg` | 28 |
| Indre By A–L | `indre-l` | 70 |
| Indre By M–Å | `indre-m` | 68 |
| Kongens Enghave | `kongens-enghave` | 1 |
| Nørrebro | `norrebro` | 12 |
| Sundby | `sundby` | 1 |
| Valby | `valby` | 5 |
| Vanløse | `vanlose` | 2 |
| Vestamager | `vestamager` | 2 |
| Vesterbro | `vesterbro` | 25 |
| Østerbro | `osterbro` | 39 |

Kilden har ingen koordinater, kort eller billeder – kun adresse og tavlens tekst/baggrund. Koordinaterne her er geokodet fra adresserne (se nedenfor). Beskrivelserne i `data/tavler.txt` er korte sammenfatninger; tavlens ordlyd står i en særskilt kolonne, når kilden gengiver den (208 af 291 tavler 16/11 2026).

## Filer

```
data/tavler.txt   én linje pr. tavle
data/coords.txt   én linje pr. sted
template.html     kortsiden; /*DATA*/, {{N}} og {{S}} udfyldes af build.py
build.py          bygger index.html og mindetavler-kbh.kml
index.html        genereret – redigér ikke i hånden
mindetavler-kbh.kml  genereret
```

### data/tavler.txt

`sted-id|bydel|adresse|beskrivelse|ordlyd`

- `sted-id` peger på en linje i `coords.txt`. Flere tavler på samme sted deler id og vises i samme markør.
- Linjerne står grupperet efter bydel; rækkefølgen bestemmer rækkefølgen i listen på kortet. Hold en bydels linjer samlet.
- `ordlyd` er tavlens tekst, som kilden gengiver den (i anførselstegn på bibliotekets side), uden de omgivende anførselstegn. ` / ` er linjeskift på tavlen, `///` (eller `//`) er afsnit eller en ny tavle/plade. Tom, hvis kilden ikke gengiver teksten – kolonnens `|` skal stadig være der. Ordlyden vises i kortets infoboks under beskrivelsen og indgår i søgningen.
- Infoboksen linker kun til bibliotekets oversigtsside, ikke til den enkelte bydelsside.
- Tegnet `|` må ikke forekomme i adresse, beskrivelse eller ordlyd.

### data/coords.txt

`sted-id|breddegrad,længdegrad` – med `|~` til sidst, hvis placeringen er omtrentlig (vises med svagere farve og teksten "Placering omtrentlig").

Id'erne er vilkårlige heltal; nye steder får blot det næste ledige nummer (aktuelt 269).

### Farver

`build.py` markerer et sted som "Besættelsen 1940–45" (rød), hvis *alle* stedets beskrivelser matcher regex'en `WAR` (besættelse, modstand, dræbt, faldt, Gestapo, Shellhuset, årstal 1940–45 m.m.). Ellers blå.

## Byg

```
python3 build.py
```

Kræver kun Python 3. Scriptet udskriver antal tavler/steder og advarer om koordinater uden for Københavnsområdet (skal være en tom liste).

## Opdatering fra kilden

1. Hent de 14 bydelssider **én ad gangen** – siden rate-limiter, hvis flere hentes samtidig. Bed om en komplet liste: adresse (inkl. bygningsnavn) og hvem/hvad tavlen mindes med årstal. Lange sider (Indre By, Østerbro) kan blive afkortet; tjek at listen når til slutningen af alfabetet, og hent igen ved tvivl.
2. Sammenlign med `data/tavler.txt` pr. bydel (antallet i tabellen ovenfor er et hurtigt første tjek): tilføj nye tavler, fjern dem, biblioteket har fjernet, og ret ændrede adresser/tekster. Ordlyden tages fra det eller de afsnit i anførselstegn, der følger lige efter tavlens indledende beskrivelse; senere citater i samme opslag er typisk baggrundslitteratur og skal ikke med. Enkelte opslag har ordlyden uden anførselstegn eller efter "Tekst på tavlen:".
3. Nye adresser geokodes og tilføjes i `data/coords.txt` med nyt id. Eksisterende steder genbruger deres id.
4. Kør `python3 build.py`, opdatér datoen og tallene i denne README, commit.

### Geokodning

Brugt 16/11 2026 (kaldt fra en browser, da de er åbne tjenester uden nøgle):

- **Photon**: `https://photon.komoot.io/api/?limit=1&bbox=12.44,55.61,12.66,55.75&q=<adresse>, København` – langsom (ca. 3 sek. pr. opslag), men finder de fleste husnumre. Resultater med `type` ≠ `house` er kun gade-/stedniveau.
- **Nominatim** til dem, Photon ikke fandt: `https://nominatim.openstreetmap.org/search?format=jsonv2&addressdetails=1&limit=1&bounded=1&viewbox=12.44,55.75,12.66,55.61&q=<adresse>` – højst ét opslag i sekundet.
- **DAWA** (`api.dataforsyningen.dk`) er lukket (svarer 410 Gone) og kan ikke bruges.

Faldgruber set ved første kørsel:

- Kontrollér altid, at det returnerede vejnavn/husnummer svarer til det, der blev søgt. "Nytorv" gav "Kongens Nytorv", "Østergade 23" gav "Ny Østergade 23", "Pile Allé 10" gav et forkert sted, og "Holmen" gav Holmens Kirke.
- OpenStreetMap staver nogle vejnavne anderledes end kilden: Julius Thomsens Gade, Peter Bangs Vej, Peder Skrams Gade, Prinsesse Charlottes Gade, Sankt Hans Gade, Forchhammersvej, Bellmansgade, Gasværksvej, Gamle Carlsberg Vej, Ny Carlsberg Vej, Sønder Boulevard, Vester Farimagsgade, Gammeltorv, Gammel Kalkbrænderi Vej.
- Intervaller og dobbeltnumre (10–12, 4/6, 28/30) geokodes på det første nummer.
- Tavler uden husnummer (plads, gade, bygning, "Kastellet", "Zoologisk Have") placeres på stedet/gaden og markeres `~`.

### Manuelle rettelser i forhold til kilden

Bevar disse ved opdatering, medmindre kilden er ændret:

- **Højdevangens Skole**: Står i kilden under Brønshøj-Husum med adressen "Grønlykkevej 1". Skolen ligger på Amager; punktet er sat ved skolen (fundet ved navn i OpenStreetMap), flyttet til bydelen Sundby og markeret omtrentlig. Adressen "Grønløkkevej 1" er ikke verificeret.
- **Vesterbro Torv 55A** (Erik Koch Michelsen): adressen er bevaret som i kilden, men punktet er geokodet som Vesterbrogade 55A.
- **Østergade 23**: kunne ikke geokodes; sat ved Østergade 21 og markeret omtrentlig.
- **Prinsessegade 53**: husnummer ikke fundet; sat ved Prinsessegade 52 og markeret omtrentlig. Tilsvarende er Antonigade 13 sat ved nr. 11 og Brolæggerstræde 7 ved nr. 9.
- **Brønshøj Skole (Liselundvej 2)** og **La Courvejens Skole (Emil Chr. Hansens Vej 6)**: sat ved skolen fundet ved navn, markeret omtrentlig.
- **Studiestræde, Bispegården**: sat ved Nørregade 11, markeret omtrentlig.
- **Grønnegården**: sat ved Bredgade 68 (Designmuseum Danmark), markeret omtrentlig.
- **Landbohøjskolen, Fødeklinikken**: sat ved Bülowsvej 17, markeret omtrentlig.
- **Holmen** (brandfolk 1951): sat midt i kvarteret Holmen, markeret omtrentlig.
- **Roskildevej, Frederiksberg Slot** og **Frederiksberg Slot, Hærens Officersskole** deler ét punkt; de to tavler i **Zoologisk Have** ligeså; de tre tavler i **Kastellet** ligeså.
- Tekstrettelser: "Sankelmark 1854" → 1864; "Waarsaae" → Worsaae; "Luftsværksregimentet" → Luftværnsregimentet.

## Baggrundskort

`index.html` henter kortfliser udefra. Erfaringer fra en lokalt åbnet fil (`file://`, ingen Referer):

- `tile.openstreetmap.de` – **virker**, er standard.
- `tile.openstreetmap.org` – afviser med "403 Access blocked". Brug den ikke.
- CARTO (`basemaps.cartocdn.com`) – kræver nu API-nøgle. Brug den ikke.
- Esri World Street Map / World Imagery – ligger som alternativer i lag-vælgeren; ikke bekræftet.

Leaflet 1.9.4 hentes fra cdnjs.

## Rettigheder

Oplysningerne om tavlerne stammer fra Københavns Biblioteker. Koordinater og baggrundskort: © OpenStreetMap-bidragydere (ODbL).
