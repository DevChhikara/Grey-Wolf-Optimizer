import os
import opfunu
import numpy as np
import pandas as pd
from mealpy.optimizer import Optimizer
from mealpy.swarm_based.WOA import OriginalWOA
import sys
import pickle


benchmark_dict = {
    2014: range(1, 31),
    2017: range(1, 30),
}


class EEGWO_helper(Optimizer):

    def __init__(self, problem, epoch=10000, pop_size=100, **kwargs):
        super().__init__(problem, epoch, pop_size, **kwargs)
        self.alpha_pos = None
        self.alpha_score = np.inf  # Change to -np.inf for maximization problems
        self.beta_pos = None
        self.beta_score = np.inf  # Change to -np.inf for maximization problems
        self.delta_pos = None
        self.delta_score = np.inf  # Change to -np.inf for maximization problems

    def initialize(self):
        """
        Initialize the population and positions of the Alpha, Beta, and Delta wolves.
        """
        super().initialize()

        # Initialize alpha, beta, delta positions and scores
        self.alpha_pos = np.zeros(self.problem.n_dims)
        self.beta_pos = np.zeros(self.problem.n_dims)
        self.delta_pos = np.zeros(self.problem.n_dims)

    def evolve(self, epoch):
        """
        Evolution process of GWO, including position update and leader selection.
        """
        a = 2 - 2 * (1 - epoch / self.epoch) ** 1.5  # Decrease the coefficient linearly

        for i in range(self.pop_size):
            fitness = self.problem.evaluate(self.pop[i].solution)

            # Update alpha, beta, and delta
            if fitness < self.alpha_score:
                self.delta_score = self.beta_score
                self.delta_pos = self.beta_pos.copy()
                self.beta_score = self.alpha_score
                self.beta_pos = self.alpha_pos.copy()
                self.alpha_score = fitness
                self.alpha_pos = self.pop[i].solution.copy()
            elif fitness < self.beta_score:
                self.delta_score = self.beta_score
                self.delta_pos = self.beta_pos.copy()
                self.beta_score = fitness
                self.beta_pos = self.pop[i].solution.copy()
            elif fitness < self.delta_score:
                self.delta_score = fitness
                self.delta_pos = self.pop[i].solution.copy()

        # Update positions of search agents (wolves)
        for i in range(self.pop_size):
            for j in range(self.problem.n_dims):
                r1, r2 = np.random.rand(), np.random.rand()
                A1 = 2 * a * r1 - a
                C1 = 2 * r2

                D_alpha = abs(C1 * self.alpha_pos[j] - self.pop[i].solution[j])
                X1 = self.alpha_pos[j] - A1 * D_alpha

                r1, r2 = np.random.rand(), np.random.rand()
                A2 = 2 * a * r1 - a
                C2 = 2 * r2

                D_beta = abs(C2 * self.beta_pos[j] - self.pop[i].solution[j])
                X2 = self.beta_pos[j] - A2 * D_beta

                r1, r2 = np.random.rand(), np.random.rand()
                A3 = 2 * a * r1 - a
                C3 = 2 * r2

                D_delta = abs(C3 * self.delta_pos[j] - self.pop[i].solution[j])
                X3 = self.delta_pos[j] - A3 * D_delta

                num = np.random.randint(0, self.pop_size)
                self.pop[i].solution[j] = 0.1 * np.random.rand() * ((X1 + X2 + X3) / 3) + 0.9 * np.random.rand() * (
                            self.pop[num].solution[j] - self.pop[i].solution[j])

                # Boundary check
                self.pop[i].solution[j] = np.clip(self.pop[i].solution[j], self.problem.lb[j], self.problem.ub[j])

                # Apply rounding if necessary (based on the original code)
                self.pop[i].solution[j] = np.floor(self.pop[i].solution[j] + 0.5)

            # Evaluate the new fitness
            self.pop[i].fitness = self.problem.evaluate(self.pop[i].solution)

        # Sort the population based on fitness
        self.pop = sorted(self.pop, key=lambda x: x.fitness)

        # Update alpha, beta, delta based on new population
        self.alpha_pos = self.pop[0].solution.copy()
        self.alpha_score = self.pop[0].fitness
        self.beta_pos = self.pop[1].solution.copy()
        self.beta_score = self.pop[1].fitness
        self.delta_pos = self.pop[2].solution.copy()
        self.delta_score = self.pop[2].fitness

        return self.alpha_score, self.alpha_pos


# class EEGWO:
#     def __init__(self, epoch, pop_size):
#         self.epoch = epoch
#         self.pop_size = pop_size
#         self.name = "mSDWOA"

#     def solve(self, problem_dict, termination):
#         opt_func = problem_dict["fit_func"]

#         b = 0.5
#         a = 2.0
#         a_step = 0.06
#         constraints = [problem_dict["lb"], problem_dict["ub"]]

#         if problem_dict["minmax"] == "min":
#             maximize = False
#         else:
#             maximize = True

#         opt_alg = EEGWO_helper(
#             opt_func,
#             # constraints,
#             self.pop_size,
#             b,
#             a,
#             a_step,
#             problem_dict["dim"],
#             maximize,
#         )

#         for t in range(self.epoch):
#             opt_alg.optimize(t, self.epoch, termination["max_fe"])
#         return opt_alg.best_solutions()





# def final_result(model_name):
#     WOAResults = {}
#     for year in [2014, 2017]:
#         for func_num in benchmark_dict[year]:
#             func_map_key_name = f"F{func_num}{year}"
#             WOAResults[func_map_key_name] = {}
#             for dimension in [10, 30, 50, 100]:
#                 func_name = f"opfunu.cec_based.F{func_num}2014(ndim={dimension})"
#                 WOAResults[func_map_key_name][dimension] = {}

#                 for pop_size in [
#                     10,
#                     20,
#                     30,
#                     40,
#                     50,
#                     70,
#                     100,
#                     200,
#                     300,
#                     400,
#                     500,
#                     700,
#                     1000,
#                 ]:
#                     problem = eval(func_name)
#                     problem_dict = {
#                         "fit_func": problem.evaluate,
#                         "lb": problem.lb,
#                         "ub": problem.ub,
#                         "minmax": "min",
#                         "log_to": "file",
#                         "log_file": "history-msdwoa.log",
#                         "dim": dimension,
#                     }
#                     run_result = np.array([])
#                     for iter in range(1, 52):
#                         epoch = 10000
#                         pop_size = pop_size
#                         model = model_name(epoch, pop_size)
#                         max_fe = 10000 * dimension
#                         term_dict = {"max_fe": max_fe}
#                         best_fitness, _ = model.solve(
#                             problem_dict, termination=term_dict
#                         )
#                         run_result = np.append(run_result, best_fitness)
#                         print(
#                             f"{model.name} => Function: {func_map_key_name}, Dimension: {dimension}, Population Size: {pop_size} :: Iteration: {iter}, Fitness: {best_fitness}",
#                             flush=True,
#                         )
#                     WOAResults[func_map_key_name][dimension][pop_size] = np.mean(
#                         run_result
#                     )
#                     print(
#                         f"=========={model.name} => Function: {func_map_key_name}, Dimension: {dimension}, Population Size: {pop_size} :: Completed: {WOAResults[func_map_key_name][dimension][pop_size]}==========",
#                         flush=True,
#                     )
#                     print(WOAResults)
#                     with open("outFile.dat", 'ab+') as outFile:
#                         pickle.dump(WOAResults, outFile)
    # for key in WOAResults.keys():
    #     df = pd.DataFrame(WOAResults[key])
    #     directory_path = f"./results/{model.name}"
    #     if not os.path.exists(directory_path):
    #         os.makedirs(directory_path)
    #     df.to_csv(f"{directory_path}/{key}.csv", index=True)



if __name__ == "__main__":
    func_name = f"opfunu.cec_based.F12014(ndim=10)"
    problem = eval(func_name)
    eegwo = EEGWO_helper(problem, 52, 10)
    eegwo.evolve(52)
