import copy
import math
import random

import NEAT_genome as G
import NEAT_species as S
import NEAT_snake as snake


compatability_threshold = 2
c1 = 1
c2 = 2
c3 = 0.4
count = 0

class Population:

    def __init__ (self, pop_num, inOutNodes):
        self.genomes = self.init_pop(pop_num, inOutNodes[0], inOutNodes[1])
        self.species = []
        
    def init_pop(self, num, In, Out):
        genomes = []
        new_genome = G.Genome(In, Out)
        for i in range(num):
            g = copy.deepcopy(new_genome)
            #print(g.biasNode)
            g.mutate()
            genomes.append(g)
        return genomes
            
    def speciate(self):
        global compatability_threshold, c1, c2, c3
        avg_compat = 0
        #compute genome size for normalization purposes
        #add the first genome as new species if None exist
        if len(self.species) == 0:
            first_species = S.Species(self.genomes[0])
            self.species.append(first_species)
        else:
            #purge species membership excluding rep_genome
            for s in self.species:
                s.members = []
                s.members.append(s.rep_genome)

        #categorize remaining genomes into species
        for g in self.genomes:
            not_added = True
            #check if genome is compatible with any existing species
            for s in self.species:
                rep_genome = s.rep_genome
                #check if g is a rep_genome of species
                if rep_genome == g:
                    not_added = False
                    break
                #keep track of types of gene compariosns
                matching = 0
                excess = 0
                disjoint = 0
                avg_weight_diff = 0
                #determine which connections genome is larger
                if len(rep_genome.connectionGenes) >= len(g.connectionGenes):
                    large = rep_genome.connectionGenes
                    small = g.connectionGenes
                else:
                    large = g.connectionGenes
                    small = rep_genome.connectionGenes
                #iterate through smaller genome and count matching and disjoint genes
                j = 0
                k = 0
                while j < len(small) and k < len(large):
                    conn_s = small[j]
                    conn_l = large[k]
                    if conn_s.innovNum == conn_l.innovNum:
                        matching += 1
                        avg_weight_diff += abs(conn_s.weight - conn_l.weight)
                        j += 1
                        k += 1
                    elif conn_s.innovNum < conn_l.innovNum:
                        disjoint += 1
                        j += 1
                    else:
                        disjoint += 1
                        k += 1
                excess += len(small) - j + len(large) - k
                if matching != 0:
                    avg_weight_diff /= matching
                #determine compatability
                if len(large) > 0:
                    compatability = ((c1 * excess) + (c2 * disjoint))/len(large) + (c3 * avg_weight_diff)
                else:
                    compatability = (c1 * excess) + (c2 * disjoint) + (c3 * avg_weight_diff)
                #print((matching, disjoint, excess, compatability))
                #add genome to species if compatible with rep_genome
                if compatability <= compatability_threshold:
                    s.members.append(g)
                    avg_compat += compatability
                    not_added = False
                    break
            #if genome is not compatible with any existing species, create a new species and make this genome its rep_genome
            if not_added == True:
                new_s = S.Species(g)
                avg_compat += compatability
                self.species.append(new_s)
        #print(avg_compat/len(self.genomes))        
        
        #purge any stagnant speciez
        for s in self.species:
            if len(s.members) == 1:
                s.stagnation += 1
            else:
                s.stagnation = 0
            if s.stagnation > 10:
                self.species.remove(s)
            best_genome = max(s.members, key = lambda x : x.fitness)
            s.rep_genome = best_genome
        #dynamically adjust compatability_threshold to keep the num of species in certain range
        """
        global count
        if len(self.species) > 20 and count > 50:
            compatability_threshold += 0.1
            count = 0
            print(compatability_threshold)
        elif len(self.species) < 10 and count > 50:
            compatability_threshold -= 0.1
            count = 0
            print(compatability_threshold)
        count += 1
        """
    
    
    
    
    def createNextGen(self, pop_num):
        next_gen = []
        culled_species = []

        #selected upper half of fittest per species
        for s in self.species:
            if len(s.members) > 1:
                fitness_sorted = sorted(s.members, key = lambda x : x.fitness)
                half = math.floor(len(fitness_sorted)/2)
                fittest_half = fitness_sorted[:half]
                s.species = fittest_half
                culled_species.append(s)

        #calc shared_fitness per species
        for s in culled_species:
            for g in s.members:
                s.shared_fitness += g.fitness
            s.shared_fitness /= len(s.members)
            #print(s.shared_fitness)
        
        #determine total population fitness
        total_pop_fitness = 0
        for s in culled_species:
            total_pop_fitness += s.shared_fitness

        #create a new population using species fitness
        for s in culled_species:
            offspring_num = 0
            l = len(s.members)

            #allocate offspring proportional to total_pop_fitness
            #print((s.shared_fitness, total_pop_fitness, int(math.floor(s.shared_fitness/total_pop_fitness * pop_num))))
            if total_pop_fitness > 0:    
                offspring_num = int(math.floor(s.shared_fitness/total_pop_fitness * pop_num))
            else:
                offspring_num = int(math.floor(len(self.genomes)/len(self.species)))
            #if offspring_num >= 100:
             #   s.rep_genome.network.printAdjList()
            #print((len(s.members), offspring_num))
            #save fittest genome of species
            if offspring_num > 0:
                offspring_num -= 1
                best_genome = max(s.members, key = lambda x: x.fitness)
                best_genome.fitness = 0
                next_gen.append(copy.deepcopy(best_genome))

            #create new offspring
            for i in range(offspring_num):
                parent1, parent2 = s.select_parents()
                child = s.crossover(parent1, parent2)
                child.mutate()
                next_gen.append(child)

        #fill remaining spots with random child
        temp_next_gen = copy.deepcopy(next_gen)
        while len(next_gen) < pop_num:
            child = random.choice(temp_next_gen)
            child.mutate()
            next_gen.append(child)

        #sort genomes
        for g in next_gen:
            g.sort()

        self.genomes = next_gen
    
    def evolve(self, iterations):
        for i in range(iterations):
            #evaluate each genome in population
            for g in self.genomes:
                g.fitness = snake.play_silent(g)
            #speciate
            self.speciate()
            print(str(i) + ": ",end="")
            best = 0
            for s in self.species:
                best_genome = max(s.members, key = lambda x : x.fitness)
                best_fitness = best_genome.fitness
                if best_fitness > best:
                    best = best_fitness
                #best_genome.network.printAdjList()
                #best_genome.printGenome()
                print(str((len(s.members), (len(best_genome.nodeGenes), len(best_genome.connectionGenes)), s.stagnation, round(best_fitness, 3))) + ", ",end="")
                """
                avg_size_n = 0
                avg_size_c =0
                for g in s.members:
                    avg_size_n += len(g.nodeGenes)
                    avg_size_c += len(g.connectionGenes)
                avg_size_n /= len(s.members)
                avg_size_c /= len(s.members)
                print(str(((round(avg_size_n), round(avg_size_c)), (len(s.rep_genome.nodeGenes), len(s.rep_genome.connectionGenes)))) + ", ",end="")
                """
            print(len(self.species), round(best, 3))
            #print("--------------")
            self.createNextGen(len(self.genomes))
        #for s in self.species:
         #   s.rep_genome.network.printAdjList()
          #  s.rep_genome.printGenome()