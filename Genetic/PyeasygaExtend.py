from pyeasyga.pyeasyga import pyeasyga


class PayeasygaExtend(pyeasyga.GeneticAlgorithm):
    def run(self):
        average_fitness_table = []
        best_fitness_table = []
        self.create_first_generation()
        avg_fit = sum([i.fitness for i in self.current_generation]) / len(self.current_generation)
        average_fitness_table.append(avg_fit)
        best_fit = self.current_generation[0].fitness
        best_fitness_table.append(best_fit)
        for _ in range(1, self.generations):
            self.create_next_generation()
            avg_fit = sum([i.fitness for i in self.current_generation]) / len(self.current_generation)
            average_fitness_table.append(avg_fit)
            best_fit = self.current_generation[0].fitness
            best_fitness_table.append(best_fit)

        return average_fitness_table, best_fitness_table
