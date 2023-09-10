import pickle
import queue
import NEAT_population as P
import NEAT_snake as snake
from NEAT_network import Network
from NEAT_genome import Genome, NodeGene, ConnectionGene
import random
"""
def find_best_genome(population):
    for g in population.genomes:
        g.evaluate()
    best_genome = max(population.genomes, key = lambda x : x.fitness)
    best_genome.network.printAdjList()    
    best_genome.printGenome()
    #show best_genome results on task
    for i in range(2):
        for j in range(2):
            #reset recurrent activations
            for node in best_genome.nodeGenes:
                node.recurrentActivation = 0
            #evaluate for certain number of cycles
            for k in range(2):
                best_genome.network.forwardProp([i, j], best_genome)
            print(str((i, j)) + ", ", end="")
            for node in best_genome.outputNodes:
                print(str(node.activation) + ", ", end="")
            print("")
    print(best_genome.fitness)

    
    
"""
def save(genome):
    with open('NEAT_bestGenome', 'wb') as file:
        pickle.dump(genome, file)
    print("Genome saved to files!")
            
def load(file):
    genome = None    
    with open("NEAT_objects", 'rb') as file:
        genome = pickle.load(file)
        print(genome.network)
    return genome
    

def find_best_genome(population):
    for s in population.species:
        best_genome = max(s.members, key = lambda x : x.fitness)
        best_genome.fitness = snake.play(s.rep_genome)
        best_genome.network.printAdjList()
        best_genome.printGenome()
        print(s.rep_genome.fitness)
    for g in population.genomes:
        g.fitness = snake.play_silent(g, r, c)
    best_genome = max(population.genomes, key = lambda x : x.fitness)
    best_genome.network = Network(best_genome)
    best_genome.network.printAdjList()    
    best_genome.printGenome()
    print(best_genome.fitness)
    #save(best_genome)


population = P.Population(100, (15, 3))
population.evolve(10000)
find_best_genome(population)

#best = load("NEAT_bestGenome")
#print(best.geneNodes)
#best.fitness = snake.play(best)





