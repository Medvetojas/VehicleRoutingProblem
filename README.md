## [For English, click here](#vehicle-routing-problem-with-genetic-algorithm) // [Magyar nyelvhez, kattints ide](#vehicle-routing-problem-genetikus-algoritmussal)

# Vehicle Routing Problem (with Genetic Algorithm)

## Assignment description
Vehicle Routing Problem, solved with Genetic Algorithm.  
The program was written in Python, with PyCharm IDE.  
Packages used: deepcopy, random, matplotlib, typing  

## Steps of solution

1. The program asks for the input of the user for the following data:

     - Number of cities (including the depot)
     - Number of vehicles
     - Number of iterations
     - Number of generations
     
Example:
     
![](https://github.com/Medvetojas/VehicleRoutingProblem/blob/main/input_example.png?raw=true)

2. The program generates the cities' x and y coordinates randomly between 1 and 100, then stores them in a matrix, then creates another matrix for the distances between the cities. A starting order is then created, based on the cities distances from each other.

3. The genetic algorithm begins, which - after filling the population with the initial data and calculating initial fitness values - does the following iteration times (*has a random maximum iteration limit, if the best result does not improve for a long time*):

     - executes mutation, which swaps two cities between two vehicles
     - executes crossover (recombination), which selects two adjacent (at the last iteration, the first and last) generations, creates an intersection, then creates a merge generation
       - the intersection part is being cut from the second generation (route), and it is being inserted into the first generation
       - since crossover is hard in 2D, the recombination is made in a vector form, but it will be converted back to a matrix
       - the depot is removed temporarily from the routes until the procedure ends, but then it is readded
     - selects the best generation based on surviving probability, which can be considered a solution, albeit not necessarily the best and final one

4. Kirajzol??sra ker??l a megold??s. A genetikus algoritmus fut??sa alatt a t??l??l??si f??zisn??l is megjelen??ti a konzol a "t??l??l??" megold??st.
4. The program creates a plot of the solution and prints the solution to the console. Also, while running the genetic algorithm, whenever a better solution is found, it is printed to the console.

Examples:


![](https://github.com/Medvetojas/VehicleRoutingProblem/blob/main/solution_example.png?raw=true)
![](https://github.com/Medvetojas/VehicleRoutingProblem/blob/main/plot_example.png?raw=true)


## Sources
I used the following sources to complete the assignment:
* The example for mutation and surviving probability from the assignment
* Levente Fazekas: [Genetic Algorithms](https://ai.leventefazekas.hu/lessons/2022-10-18-genetic-algorithms) and [Traveling Salesman Problem](https://ai.leventefazekas.hu/lessons/2022-10-11-travelling-salesman) lessons
* [Anita Ag??rdi: A j??ratszervez??si probl??ma megold??sa auton??m, elektromos j??rm??vek eset??n c. cikke](http://www.tdk.uni-miskolc.hu/files/_elso_ot_oldala_vegleges.pdf)
* [Matplotlib's Wiki site](https://matplotlib.org/stable/gallery)

Also, for the solution's logic and the data structures to store the data, I asked the help of Imre Piller.

## Some mistakes

The code includes detailed commenting in Hungarian language, but the variables themselves are in English, therefore the whole project has a "hunglish" feeling.  
I gave a type for every method's return values and parameters aswell, because it is easier for me to see through the whole code (*hello C#*), this is why the typing package was required. I'm pretty sure this is neither a convention nor a positive thing.

------------------------------------- 

# Vehicle Routing Problem (Genetikus Algoritmussal)

## Feladatle??r??s
Vehicle Routing Problem, genetikus algoritmussal megoldva.  
A program Python nyelven, PyCharm IDE haszn??lat??val k??sz??lt.  
Felhaszn??lt csomagok: deepcopy, random, matplotlib, typing

## Megold??s l??p??sei

1. A program bek??ri az inputokat a felhaszn??l??t??l:

     - A v??rosok sz??ma (a dep??val egy??tt)
     - J??rm??vek sz??ma (m??ssz??val fut??rok)
     - Iter??ci??k sz??ma
     - Gener??ci??k sz??ma
     
P??lda:
     
![](https://github.com/Medvetojas/VehicleRoutingProblem/blob/main/input_example.png?raw=true)

2. A program 1 ??s 100 k??z??tt v??letlenszer??en legener??lja a v??rosok x ??s y koordin??t??it, let??rolja ??ket egy m??trixba, majd pedig egy ??jabb m??trixot k??sz??t a v??rosok k??zti t??vols??gokb??l. Ezut??n a j??rm??veknek ki lesznek osztva a v??rosok, figyelembev??ve az egym??st??l val?? t??vols??gukat.

3. Elindul a genetikus algoritmus, mely - miut??n felt??lti a popul??ci??t a kezdeti adatokkal ??s kezdeti fitness ??rt??ket sz??mol - iter??ci??szor (*random be??p??tett iter??ci?? limittel, ha nem javulna a megold??s sok id??n ??t*) v??grehajtja r??viden az al??bbiakat:

     - v??grehajtja a mut??ci??t, mely k??t aut?? k??z??tt k??t v??rost felcser??l
     - v??grehajtja a keresztez??st (rekombin??ci??t), mely kiv??laszt k??t egym??s melletti (a v??g??n az utols?? ??s az els??) gener??ci??t, k??sz??t egy kimetsz??st, majd k??sz??t egy egyes??tett ??tvonalat
       - a kimetsz??s a m??sodik gener??ci??b??l (??tvonalb??l) t??rt??nik, ??s az els?? ??tvonalba ker??l beilleszt??sre
       - mivel 2D-ben neh??z a keresztez??s, vektor form??ban lesz v??grehajtva a rekombin??ci??, a folyamat v??g??n ker??l visszaalak??t??sra m??trixsz??
       - a dep??t elt??vol??tja ??tmenetileg a folyamat erej??ig, majd visszateszi azt
     - t??l??l??si val??sz??n??s??g alapj??n kiv??lasztjuk a legjobb gener??ci??t, mely egy k??sz megold??snak tekinthet??, de nem felt??tlen??l a legjobbnak ??s a v??glegesnek

4. Kirajzol??sra illetve konzolra val?? ki??r??sra ker??l a megold??s. A genetikus algoritmus a fut??sa alatt is megjelen??ti, hogyha jobb megold??st tal??lt az el??z??n??l.

P??ld??k:


![](https://github.com/Medvetojas/VehicleRoutingProblem/blob/main/solution_example.png?raw=true)
![](https://github.com/Medvetojas/VehicleRoutingProblem/blob/main/plot_example.png?raw=true)


## Felhaszn??lt irodalomak ??s egy??b forr??sok, seg??ts??gek
A program elk??sz??t??s??hez a k??vetkez?? forr??sokat haszn??ltam:
* A feladatki??r??sban szerepl?? mut??ci?? p??lda, illetve t??l??l??si val??sz??n??s??g k??plet
* Fazekas Levente: [Genetikus algoritmusok](https://ai.leventefazekas.hu/lessons/2022-10-18-genetic-algorithms) ??s [Traveling Salesman Problem](https://ai.leventefazekas.hu/lessons/2022-10-11-travelling-salesman) tananyagai
* [Ag??rdi Anita: A j??ratszervez??si probl??ma megold??sa auton??m, elektromos j??rm??vek eset??n c. cikke](http://www.tdk.uni-miskolc.hu/files/_elso_ot_oldala_vegleges.pdf)
* [Matplotlib Wiki oldala](https://matplotlib.org/stable/gallery)

A fentieken fel??l, a megold??si logika, ??s az adatok t??rol??s??hoz sz??ks??ges adatstrukt??ra "kital??l??s??hoz" Piller Imre seg??ts??g??t k??rtem.

## Hib??k

A feladat r??szletes kommentez??st tartalmaz, a v??ltoz??k angolul vannak, a komment viszont magyar, ??gy kicsit "hunglish" jellege van az eg??sznek.  
T??pust adtam minden f??ggv??ny visszat??r??si ??rt??k??nek ??s param??tereinek is, hogy k??nnyebben ??tl??ssam a dolgokat (*hello C#*), ez??rt volt sz??ks??g a typing csomagra. Ez sem biztos, hogy konvenci?? k??vet??, pozit??v dolog.
