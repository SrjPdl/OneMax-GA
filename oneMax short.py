from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import random
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

ONE_MAX_LENGTH = 100
P_MUTATION = 0.1
P_CROSSOVER = 0.9
POPULATION_SIZE = 200
MAX_GENERATIONS = 50
HALL_OF_FRAME_SIZE = 10

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
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("max", np.max)

    hof = tools.HallOfFame(HALL_OF_FRAME_SIZE)

    population, logbook = algorithms.eaSimple(population,toolbox,P_CROSSOVER,P_MUTATION,MAX_GENERATIONS,stats,hof,verbose=True)

    maxFitnessValues = logbook.select("max")
    meanFitnessValues = logbook.select("avg")

    # print("Hall of Fame Individuals = ", *hof.items, sep="\n")
    # print("Best Ever Individual = ", hof.items[0])

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