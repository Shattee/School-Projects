# Method description
# the procedure is based on Youtube video "9.4: Genetic Algorithm: Looking at Code - The Nature of Code" which is JavaScript code.
# 1. set up class DNA first which include genes(the random sentence), method to calculate fitness, do crossover and mutate.
# 2. when running the program, first function setPopulation set up the population array based on defined total population number,
# then findMatch(population) start to count the fitness in each of genes, and doing crossover and mutate(generate child with mating pool)
# once the program find the perfect match(bestFitness == 1), the program will stop.

import random
geneRange = range(32,128)  # the range where the gene gonna generate
target = "To be or not to be"
len_target = len(target)
mutationRate = 0.01

# set up DNA class for GA
class DNA:
    def __init__(self):
        self.genes = []
        for ii in range(len_target):
            gene = chr(random.choice(geneRange))
            self.genes.append(gene)

    def getPhrase(self):    # return the random generate genes
            return ''.join(self.genes)

    def calcFitness(self):  # count the ratio of how many letters match the target
        score = 0
        for ll in range(len(self.genes)):
            if self.genes[ll] == target[ll]:
                score += 1
        self.fitness = float(score)/len(target)

    def crossover(self, partner):
        child = DNA()       # a new randomly generated genes
        # the position in each DNA to do crossover
        midpoint = random.choice(range(len(self.genes)))

        for ll in range(len(self.genes)):
            if ll > midpoint:
                child.genes[ll] = self.genes[ll]
            else:
                child.genes[ll] = partner.genes[ll]
        return child

    # mutate based on mutation rate
    def mutate(self):
        for ll in range(len(self.genes)):
            if random.random() < mutationRate:
                self.genes[ll] = chr(random.choice(geneRange))

totalPopulation = 1200
population = []

def setPopulation():
    for ii in range(totalPopulation):
        population.append(DNA())    # add random DNA to population

def findMatch(population):
    generation = 0
    perfect = False     # if sentence matches equals True
    while not perfect:
        bestFitness=0
        index = 0
        for ii in range(len(population)):
            population[ii].calcFitness()
            if population[ii].fitness > bestFitness:
                index = ii
                bestFitness = population[ii].fitness
                print(population[index].getPhrase(), "--Fitness:", bestFitness, ",Generation:", generation)
        if bestFitness == 1:    # perfect match the target sentence
            perfect = True


        matingPool = []
        Originpopulation = population
        population = []

        for ii in range(len(Originpopulation)):
            nn = int(Originpopulation[ii].fitness * 100)   # Arbitrary multiplier
            for j in range(nn):
                matingPool.append(Originpopulation[ii])    #set up mating pool randomly

        for ii in range(len(Originpopulation)):           # generate Child
            a = random.choice(range(len(matingPool)))
            b = random.choice(range(len(matingPool)))

            parentA = matingPool[a]
            parentB = matingPool[b]
            child = parentA.crossover(parentB)
            child.mutate()

            population.append(child)
        generation += 1

setPopulation()
findMatch(population)