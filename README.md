# Vehicle Routing Problem (Genetic Algorithm)

## Feladatleírás
Vehicle Routing Problem, genetikus algoritmussal megoldva.  
A program Python nyelven, PyCharm IDE használatával készült.  
Felhasznált csomagok: deepcopy, random, matplotlib, typing

## Megoldás lépései

1. A program bekéri az inputokat a felhasználótól:
     - A városok száma (a depóval együtt)
     - Járművek száma (másszóval futárok)
     - Iterációk száma
     - Generációk száma

2. A program 1 és 100 között legenerálja a városok x és y koordinátáit, letárolja őket egy mátrixba, majd pedig egy újabb mátrixot készít a városok közti távolságokból. Ezután a járműveknek ki lesznek osztva a városok, figyelembevéve az egymástól való távolságukat.

3. Elindul a genetikus algoritmus, mely iterációszor (*maximum 350-szer, ha nem történik javulás*) végrehajtja röviden az alábbiakat:
     - feltölti a populációt a kezdeti megoldással, majd kiszámolja a fitness értéküket
     - végrehajtja a mutációt, mely két autó között két várost felcserél
     - végrehajtja a keresztezést (rekombinációt), mely kiválasztja az egymás melletti (végül az utolsó és az első) útvonalakat, és közöttük cserél
       - mivel 2D-ben nehéz a keresztezés, ezért egy darab vektorrá alakítja az útvonalakat, majd visszaalakítja azt a rekombináció után 2D-re
       - a depót eltávolítjuk átmenetileg a folyamat erejéig, majd visszateszi azt
     - túlélési valószínűség alapján kiválasztjuk a legjobb generációt, mely egy kész megoldásnak tekinthető

4. Kirajzolásra kerül a legjobb megoldás, annak hossza. A genetikus algoritmus futása alatt a túlélési fázisnál is megjeleníti a konzol a "túlélő" megoldást.

### Hibák

A feladat részletes kommentezést tartalmaz, a változók angolul vannak, a komment viszont magyar, így kicsit hunglish jellege van az egésznek.  
Típust adtam minden függvény visszatérési értékének és paramétereinek is, hogy könnyebben átlássam a dolgokat (*hello C#*), ezért volt szükség a typing csomagra.

## Felhasznált irodalomak és egyéb források, segítségek
A program elkészítéséhez a következő forrásokat használtam:
* A feladatkiírásban szereplő mutáció példa, illetve túlélési valószínűség képlet
* [Agárdi Anita: A járatszervezési probléma megoldása autonóm, elektromos járművek esetén c. cikke](http://www.tdk.uni-miskolc.hu/files/_elso_ot_oldala_vegleges.pdf)

A fentieken felül, a megoldási logika, és az adatok tárolásához szükséges adatstruktúra "kitalálásához" Piller Imre segítségét kértem.