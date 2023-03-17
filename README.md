# AI Final Project

TODO:

1. Create the simulated authentication function. (Nico)
   1. Password Generator, Hardcoded List admin123
1. Figure out how to measure time more accurate.
   1. time_ns() measures in nanoseconds.
   1. Maybe take the average of X executions as the fitness/utility
1. Implement a Genetic Algorithm (GA) to evolve a solution to break the
   authentication method using a timing attack. (Nico)
1. Implement a Particle Swarm Optimization (PSO) to evolve a solution to break the
   authentication method using a timing attack. (Caleb, Anna, Chentao)
1. Select metrics for comparing both algorithms:
   1. Table: Algorithm, CPU, Memory usage, Time that takes to run
   1. "How close to the solution they get in X time"
1. Create plots for the metrics:
   1. GA: Fitness over epoch (iteration of the algorithm) -> pyplot
   1. PSO: Utility over epoch (iteration of the algorithm) -> pyplot
1. Writeup
   1. Explaining what we did,
   1. Describing the implementations
   1. Describing the metrics
   1. Analyzing the plots
   1. Conclusion
