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

3. The genetic algorithm begins, which - after filling the population with the initial data and calculating initial fitness values - does the following iteration times (*a maximum of 350 iterations, if there are no improvements consecutively*):

     - executes mutation, which swaps two cities between two vehicles
     - executes crossover (recombination), which selects two adjacent (at the last iteration, the first and last) generations, creates an intersection, then creates a merge generation
       - since crossover is hard in 2D, the recombination is made in a vector form, but it will be converted back to a matrix
       - the depot is removed temporarily from the routes until the procedure ends, but then it is readded
     - selects the best generation based on surviving probability, which can be considered a solution, albeit not necessarily the best and final one

4. Kirajzolásra kerül a megoldás. A genetikus algoritmus futása alatt a túlélési fázisnál is megjeleníti a konzol a "túlélő" megoldást.
4. The program creates a plot of the solution and prints the solution to the console. Also, while running the genetic algorithm, whenever a better solution is found, it is printed to the console.

Examples:


![](https://github.com/Medvetojas/VehicleRoutingProblem/blob/main/solution_example.png?raw=true)
![](https://github.com/Medvetojas/VehicleRoutingProblem/blob/main/plot_example.png?raw=true)


## Sources
I used the following sources to complete the assignment:
* The example for mutation and surviving probability from the assignment
* Levente Fazekas: [Genetic Algorithms](https://ai.leventefazekas.hu/lessons/2022-10-18-genetic-algorithms) and [Traveling Salesman Problem](https://ai.leventefazekas.hu/lessons/2022-10-11-travelling-salesman) lessons
* [Anita Agárdi: A járatszervezési probléma megoldása autonóm, elektromos járművek esetén c. cikke](http://www.tdk.uni-miskolc.hu/files/_elso_ot_oldala_vegleges.pdf)
* [Matplotlib's Wiki site](https://matplotlib.org/stable/gallery)

Also, for the solution's logic and the data structures to store the data, I asked the help of Imre Piller.

## Some mistakes

The code includes detailed commenting in Hungarian language, but the variables themselves are in English, therefore the whole project has a "hunglish" feeling.  
I gave a type for every method's return values and parameters aswell, because it is easier for me to see through the whole code (*hello C#*), this is why the typing package was required. I'm pretty sure this is neither a convention nor a positive thing.

------------------------------------- 

# Vehicle Routing Problem (Genetikus Algoritmussal)

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

2. A program 1 és 100 között véletlenszerűen legenerálja a városok x és y koordinátáit, letárolja őket egy mátrixba, majd pedig egy újabb mátrixot készít a városok közti távolságokból. Ezután a járműveknek ki lesznek osztva a városok, figyelembevéve az egymástól való távolságukat.

3. Elindul a genetikus algoritmus, mely - miután feltölti a populációt a kezdeti adatokkal és kezdeti fitness értéket számol - iterációszor (*maximum 350-szer, ha nem történik javulás*) végrehajtja röviden az alábbiakat:

     - végrehajtja a mutációt, mely két autó között két várost felcserél
     - végrehajtja a keresztezést (rekombinációt), mely kiválaszt két egymás melletti (a végén az utolsó és az első) generációt, készít egy kimetszést, majd készít egy egyesített útvonalat
       - mivel 2D-ben nehéz a keresztezés, vektor formában lesz végrehajtva a rekombináció, a folyamat végén kerül visszaalakításra mátrixszá
       - a depót eltávolítja átmenetileg a folyamat erejéig, majd visszateszi azt
     - túlélési valószínűség alapján kiválasztjuk a legjobb generációt, mely egy kész megoldásnak tekinthető, de nem feltétlenül a legjobbnak és a véglegesnek

4. Kirajzolásra illetve konzolra való kiírásra kerül a megoldás. A genetikus algoritmus a futása alatt is megjeleníti, hogyha jobb megoldást talált az előzőnél.

Példák:


![](https://github.com/Medvetojas/VehicleRoutingProblem/blob/main/solution_example.png?raw=true)
![](https://github.com/Medvetojas/VehicleRoutingProblem/blob/main/plot_example.png?raw=true)


## Felhasznált irodalomak és egyéb források, segítségek
A program elkészítéséhez a következő forrásokat használtam:
* A feladatkiírásban szereplő mutáció példa, illetve túlélési valószínűség képlet
* Fazekas Levente: [Genetikus algoritmusok](https://ai.leventefazekas.hu/lessons/2022-10-18-genetic-algorithms) és [Traveling Salesman Problem](https://ai.leventefazekas.hu/lessons/2022-10-11-travelling-salesman) tananyagai
* [Agárdi Anita: A járatszervezési probléma megoldása autonóm, elektromos járművek esetén c. cikke](http://www.tdk.uni-miskolc.hu/files/_elso_ot_oldala_vegleges.pdf)
* [Matplotlib Wiki oldala](https://matplotlib.org/stable/gallery)

A fentieken felül, a megoldási logika, és az adatok tárolásához szükséges adatstruktúra "kitalálásához" Piller Imre segítségét kértem.

## Hibák

A feladat részletes kommentezést tartalmaz, a változók angolul vannak, a komment viszont magyar, így kicsit "hunglish" jellege van az egésznek.  
Típust adtam minden függvény visszatérési értékének és paramétereinek is, hogy könnyebben átlássam a dolgokat (*hello C#*), ezért volt szükség a typing csomagra. Ez sem biztos, hogy konvenció követő, pozitív dolog.
