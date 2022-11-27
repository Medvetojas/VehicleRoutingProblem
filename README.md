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
     
Példa:
     
![](https://github.com/Medvetojas/VehicleRoutingProblem/blob/main/input_example.png?raw=true)

2. A program 1 és 100 között legenerálja a városok x és y koordinátáit, letárolja őket egy mátrixba, majd pedig egy újabb mátrixot készít a városok közti távolságokból. Ezután a járműveknek ki lesznek osztva a városok, figyelembevéve az egymástól való távolságukat.

3. Elindul a genetikus algoritmus, mely iterációszor (*maximum 350-szer, ha nem történik javulás*) végrehajtja röviden az alábbiakat:
     - feltölti a populációt a kezdeti megoldással, majd kiszámolja a fitness értéküket
     - végrehajtja a mutációt, mely két autó között két várost felcserél
     - végrehajtja a keresztezést (rekombinációt), mely kiválasztja az egymás melletti (végül az utolsó és az első) útvonalakat, és közöttük cserél
       - mivel 2D-ben nehéz a keresztezés, vektor formában lesz végrehajtva a rekombináció, a folyamat végén kerül visszaalakításra mátrixszá
       - a depót eltávolítja átmenetileg a folyamat erejéig, majd visszateszi azt
     - túlélési valószínűség alapján kiválasztjuk a legjobb generációt, mely egy kész megoldásnak tekinthető

4. Kirajzolásra kerül a legjobb megoldás, annak hossza. A genetikus algoritmus futása alatt a túlélési fázisnál is megjeleníti a konzol a "túlélő" megoldást.

Példák:


![](https://github.com/Medvetojas/VehicleRoutingProblem/blob/main/solution_example.png?raw=true)
![](https://github.com/Medvetojas/VehicleRoutingProblem/blob/main/plot_example.png?raw=true)


## Felhasznált irodalomak és egyéb források, segítségek
A program elkészítéséhez a következő forrásokat használtam:
* A feladatkiírásban szereplő mutáció példa, illetve túlélési valószínűség képlet
* Fazekas Levente: [Genetikus algoritmusok](https://ai.leventefazekas.hu/lessons/2022-10-18-genetic-algorithms) és [TSP probléma](https://ai.leventefazekas.hu/lessons/2022-10-11-travelling-salesman) tananyagai
* [Agárdi Anita: A járatszervezési probléma megoldása autonóm, elektromos járművek esetén c. cikke](http://www.tdk.uni-miskolc.hu/files/_elso_ot_oldala_vegleges.pdf)
* [Matplotlib Wiki oldala](https://matplotlib.org/stable/gallery)

A fentieken felül, a megoldási logika, és az adatok tárolásához szükséges adatstruktúra "kitalálásához" Piller Imre segítségét kértem.

## Hibák

A feladat részletes kommentezést tartalmaz, a változók angolul vannak, a komment viszont magyar, így kicsit hunglish jellege van az egésznek.  
Típust adtam minden függvény visszatérési értékének és paramétereinek is, hogy könnyebben átlássam a dolgokat (*hello C#*), ezért volt szükség a typing csomagra. Ez sem biztos, hogy konvenció követő, pozitív dolog.
