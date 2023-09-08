import random

import NEAT_genome as G

class Species:
    
    def __init__(self, first_member):
        self.members = [first_member]
        self.shared_fitness = 0
        self.rep_genome = first_member
        self.stagnation = 0
    
    def select_parents(self):
        if len(self.members) > 1:
            summ = 0
            for g in self.members:
                summ += g.fitness
            summ /= len(self.members)
            #parent1
            cumulative_fitness = 0
            threshold = random.uniform(0, self.shared_fitness)
            parent1 = None
            for g in self.members:
                #print(g.fitness)
                adj_fitness = g.fitness / len(self.members)
                cumulative_fitness += adj_fitness
                #print((summ, cumulative_fitness, threshold, self.shared_fitness))
                if cumulative_fitness >= threshold:
                    parent1 = g
            if parent1 == None:
                pass
                print(cumulative_fitness, threshold, self.shared_fitness, summ)
            #parent2
            cumulative_fitness = 0
            threshold = random.uniform(0, self.shared_fitness)
            parent2 = None
            for g in self.members:
                adj_fitness = g.fitness / len(self.members)
                cumulative_fitness += adj_fitness
                if cumulative_fitness >= threshold:
                    parent2 = g
            if parent2 == None:
                pass
                print(True)
                print(cumulative_fitness, threshold, self.shared_fitness, summ)
        else:
            return self.members[0], self.members[0]  
        return parent1, parent2
    
    def crossover(self, g1, g2):
        offspring_nodes = []
        offspring_conns = []
        genes1 = g1.connectionGenes
        genes2 = g2.connectionGenes
        #determine which genome is larger
        if len(genes1) > len(genes2):
            small = genes2
            large = genes1
        else:
            small = genes1
            large = genes2
        i = 0
        j = 0
        #add connection genes to offspring
        while i < len(small) and j < len(large):
            conn1 = small[i]
            conn2 = large[j]
            if conn1.innovNum == conn2.innovNum:
                if random.random() >= 0.5:
                    offspring_conns.append(conn1)
                else:
                    offspring_conns.append(conn2)
                i += 1
                j += 1
            elif conn1.innovNum < conn2.innovNum:
                offspring_conns.append(conn1)
                i += 1
            else:
                offspring_conns.append(conn2)
                j += 1
        for k in range(j, len(large)):
            conn2 = large[k]
            offspring_conns.append(conn2)
        
        #add nodes to nodeGenes
        node_record = []

        for node in g1.nodeGenes:
            if node.innovNum not in node_record:
                offspring_nodes.append(node)
                node_record.append(node.innovNum)
        for node in g2.nodeGenes:
            if node.innovNum not in node_record:
                offspring_nodes.append(node)
                node_record.append(node.innovNum)
        for conn in offspring_conns:
            if conn.In.innovNum not in node_record:
                offspring_nodes.append(conn.In)
                node_record.append(conn.In.innovNum)
            if conn.Out.innovNum not in node_record:
                offspring_nodes.append(conn.Out)
                node_record.append(conn.Out.innovNum)
        if g1.biasNode not in offspring_nodes:
            offspring_nodes.append(g1.biasNode)
        offspring = G.Genome(child_genes = (offspring_nodes, offspring_conns))
        return offspring