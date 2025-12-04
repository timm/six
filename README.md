<img align=left width=150 src="etc/brain.png"> 

[&copy; 2025](http://tiny.cc/lua6) by [timm](http://timm.fyi)    

[![Lua 5.4](https://img.shields.io/badge/Lua-5.4-blue?labelColor=1D4ED8&color=0A2A7A)](http://tiny.cc/lua6)
[![Purpose XAI](https://img.shields.io/badge/Purpose-XAI-orange?labelColor=FB8C00&color=A85A00)](http://tiny.cc/lua6)
[![Goal Multi-Obj](https://img.shields.io/badge/Goal-Multi--Obj-purple?labelColor=C026D3&color=6D1780)](http://tiny.cc/lua6)
[![Deps 0](https://img.shields.io/badge/Deps-0-green?labelColor=00C853&color=006B29)](http://tiny.cc/lua6)
[![LOC ~200](https://img.shields.io/badge/LOC-~200-yellow?labelColor=FDE047&color=C3A700)](http://tiny.cc/lua6)

[binr](docs/binr.md) :: 
[act](docs/act.md) 

# Six

* [Basics](src/data.md)

Here is the combined list of canonical algorithms in the optimization and Search-Based Software Engineering (SBSE) space, sorted chronologically by their introduction and rise to prominence:

* [**Random Search (1950s):**](src/hillc.md) The essential baseline "sanity check" to prove complex methods are actually adding value.
* [**Hill Climbing (1950s):**](src/hillc.md)  The fundamental local search strategy that iteratively moves to better neighbors.
* [**Tabu Search (1986):**](src/tabu.md) A metaheuristic using memory structures (forbidden lists) to force exploration and avoid cycling.
* **Genetic Programming / GP (1992):** Evolves actual parse trees or source code (e.g., automated bug fixing) rather than parameter vectors.
* **Genetic Algorithms / GA (1975):** The grandfather of evolutionary computation, using selection, crossover, and mutation on bitstrings.
* **Simulated Annealing / SA (1983):** A probabilistic technique using "temperature" to accept worse solutions early on to escape local optima.
* **Ant Colony Optimization / ACO (1992):** Uses pheromone trails to solve path-based problems like test sequence generation.
* **Particle Swarm Optimization / PSO (1995):** Simulates flocking behavior (birds/fish) to move candidates through continuous search spaces.
* **MaxWalkSat (1996):** A stochastic local search algorithm combining greedy moves with random walks, essential for SAT solving.
* **Differential Evolution / DE (1997):** A vector-based evolutionary algorithm that optimizes continuous problems using vector differences.
* **SPEA2 (2001):** An early modern multi-objective algorithm using "strength" values and nearest-neighbor density estimation.
* **NSGA-II (2002):** The "gold standard" for multi-objective optimization using non-dominated sorting and crowding distance.
* **IBEA (2004):** Optimizes quality indicators (like Hypervolume) directly rather than relying solely on dominance ranking.
* **MOEA/D (2007):** Decomposes a multi-objective problem into many scalar sub-problems and optimizes them simultaneously.
* **TPE (2011):** Tree-structured Parzen Estimator, a Bayesian approach for hyperparameter tuning that models $p(x|y)$.
* **SMBO (2011):** Sequential Model-Based Optimization, a broad class (including SMAC) that builds surrogates to choose the next sample.
* **GPM (2010s):** Gaussian Process Models, used within SMBO to provide probabilistic predictions (mean and variance) for expensive functions.
* **FLASH (2017):** A sequential model-based optimizer that uses decision trees (CART) to quickly find solutions with very few evaluations.
* **SWAY (2018):** A recursive spectral clustering method that samples data to approximate the Pareto frontier (very relevant to your `tree.py`).
