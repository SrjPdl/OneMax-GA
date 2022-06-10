from deap import base
from deap import creator
from deap import tools

import random
import seaborn as sns
import matplotlib.pyplot as plt

ONE_MAX_LENGTH = 100
P_MUTATION = 0.1
P_CROSSOVER = 0.9
POPULATION_SIZE = 200
MAX_GENERATIONS = 50

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

toolbox = base.Toolbox()
toolbox.register("ZerosOrOnes",random.randint,0,1)

creator.create("FitnessMax",base.Fitness,weights=(1.0,))
creator.create("Individual",list,fitness=creator.FitnessMax)

toolbox.register("individualCreator",tools.initRepeat,creator.Individual,toolbox.ZerosOrOnes,ONE_MAX_LENGTH)
toolbox.register("populationCreator",tools.initRepeat,list,toolbox.individualCreator)

def oneMaxFitness(individual):
    return sum(individual),

toolbox.register("evaluate",oneMaxFitness)
toolbox.register("select",tools.selTournament,tournsize=3)
toolbox.register("mate",tools.cxOnePoint)
toolbox.register("mutate",tools.mutFlipBit,indpb = 1.0/ONE_MAX_LENGTH)

def main():
    population = toolbox.populationCreator(n=POPULATION_SIZE)
    gen_counter = 0
    fitnessValues = list(map(toolbox.evaluate,population))

    for individual,fitnessValue in zip(population,fitnessValues):
        individual.fitness.values = fitnessValue
    
    fitnessValues = [individual.fitness.values[0] for individual in population]

    maxFitnessValues = []
    meanFitnessValues = []

    while max(fitnessValues)<ONE_MAX_LENGTH and gen_counter<MAX_GENERATIONS:
        gen_counter = gen_counter + 1
        offspring = toolbox.select(population, POPULATION_SIZE)
        offspring = list(map(toolbox.clone,offspring))
        
        for child1,child2 in zip(offspring[::2], offspring[1::2]):
            if P_CROSSOVER > random.random():
                toolbox.mate(child1,child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if P_MUTATION > random.random():
                toolbox.mutate(mutant)
                del mutant.fitness.values

        freshIndividuals = [individuals for individuals in offspring if not individuals.fitness.valid]

        freshFitnessValues = list(map(toolbox.evaluate,freshIndividuals))

        for individual,fitnessValue in zip(freshIndividuals,freshFitnessValues):
            individual.fitness.values = fitnessValue
        
        population[:] = offspring

        fitnessValues = [individual.fitness.values[0] for individual in population]
        maxFitnessValue = max(fitnessValues)
        maxFitnessValues.append(maxFitnessValue)
        meanFitnessValue = sum(fitnessValues)/POPULATION_SIZE
        meanFitnessValues.append(meanFitnessValue)
        print(f"Generation: {gen_counter} | Max Fitness: {maxFitnessValue} | Mean Fitness: {meanFitnessValue}")

    sns.set_style("whitegrid")
    plt.plot(maxFitnessValues,label="Max Fitness")
    plt.plot(meanFitnessValues,label="Mean Fitness")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("OneMax")
    plt.legend()
    plt.show()        



   
if __name__=="__main__":
    main()