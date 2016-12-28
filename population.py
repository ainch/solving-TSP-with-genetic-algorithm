import random
import mpmath

#the city on gird
class City:         #1
   def __init__(self,x=0,y=0):
       self.x=x
       self.y=y

   def getX(self):
       return self.x

   def getY(self):
       return self.y

   def to_distance(self,nextcity):
       ret=0
       ret=(self.x-nextcity.x)*((self.x-nextcity.x))
       ret=ret+(self.y - nextcity.y) * ((self.y - nextcity.y))
       return mpmath.sqrt(ret)

#the collection of city
class Tour:         #2
   def __init__(self,l=None):
       self.tour=[]
       if l!=None:
           for x in range(len(l)):
               self.tour.append(City(l[x][0], l[x][1]))

   def size(self):
       return len(self.tour)

   def __len__(self):
       return len(self.tour)

   def add(self,city):
       self.tour.append(city)

   def __getitem__(self,idx):
       return self.tour[idx]

   def get(self,idx):
       return self.tour[idx]

class Gene:         #3
   def __init__(self,tour,gene=None):
       self.tour=tour
       self.gene=[]    #the order of city : example > [ 1, 0, 3, 2 ]
       self.real_grid=[]
       self.fitness=0.0
       self.distance=0.0
       if gene==None:
           for x in range(len(self.tour)):
               self.gene.append(x)
           random.shuffle(self.gene)   #make order randomly
       else:
           self.gene = gene
       for num in self.gene:
           city = self.tour[num]
           self.real_grid.append([city.getX(),city.getY()])

   def print(self):
       for x in self.gene:
           print(x,end= " ")
       print()

   def print_on_file(self):
       with open("data.txt","w") as f:
           for i in range(len(self.real_grid)):
               x=self.real_grid[i][0]
               y=self.real_grid[i][1]
               f.write(str(x)+","+str(y)+"\n")
       with open("data2.txt","w") as f2:
           f2.write(str(self.distance))
   def size(self):
       return len(self.gene)

   def __len__(self):
       return len(self.gene)

   def get_element(self,idx):
       return self.gene[idx]

   def __getitem__(self,idx):
       return self.gene[idx]

   def __setitem__(self,idx,value):
       self.gene[idx]=value
       self.real_grid[idx][0]=self.tour[value].getX()
       self.real_grid[idx][1]=self.tour[value].getY()

   def getfitness(self):
       if self.fitness!= 0:
           return self.fitness
       if self.distance ==0:
           self.distance = self.getdistance()
       self.fitness = 1/self.distance
       return self.fitness

   def from_to_distance(self,now,next):
       nowcity = self.tour[self.gene[now]]
       nextcity = self.tour[self.gene[next]]
       return nowcity.to_distance(nextcity)

   def getdistance(self):
       if self.distance!=0:
           return self.distance
       ret=0.0
       for x in range(len(self.gene)):
           if(x+1==len(self.gene)):
               next=0
           else:
               next=x+1
           ret = ret + self.from_to_distance(x,next)
       return ret

class Population:       #4

   def __init__(self,tour,populationsize):
       self.tour = tour    #standard tour
       self.genes=[]
       for x in range(populationsize):
           self.genes.append(Gene(tour))
   def populationsize(self):
       return len(self.genes)

   def add(self,gene):
       self.genes.append(gene)

   def set_gene(self,idx,gene):
       if type(gene)==Gene:
           raise TypeError
       self.genes[idx] = gene

   def get_gene(self,idx):
       return self.genes[idx]

   def getfittest(self):
       if self.populationsize() == 0:
           return -1
       ret = self.genes[0]
       for x in self.genes:
           if ret.getfitness()<x.getfitness():
               ret = x
       return ret

class GeneticAlgorithm:
   def __init__(self,tour,mutationrate=0.02,tournamentsize=6):
       self.tour=tour
       self.tournamentsize=tournamentsize
       self.mutationrate=mutationrate

   def crossover(self,parent1, parent2, st=None, end=None):
       if type(parent1)!=Gene:
           raise TypeError
       if type(parent2)!=Gene:
           raise TypeError
       if st == None:
           st = random.randrange(0, len(parent1))
       if end == None:
           end = random.randrange(0, len(parent2))
       if st > end:
           st, end = end, st
       tmp = []
       for x in range(len(parent1)):
           idx = (x + end + 1) % len(parent2)
           if parent2[idx] in parent1[st:end + 1]:
               continue
           tmp.append(parent2[idx])
       return Gene(self.tour,tmp[0:st] + parent1[st:end + 1] + tmp[st:])

   def mutate(self,gene):
       for tour1 in range(len(gene)):
           if random.random()<self.mutationrate:
               tour2 = random.randrange(0,len(gene))
               gene[tour1],gene[tour2]=gene[tour2],gene[tour1]

   def tournament_selection(self,pop):
       tournament=Population(self.tour,self.tournamentsize)
       for i in range(tournament.populationsize()):
           idx = random.randrange(pop.populationsize())
           gg = pop.genes[idx]
           tournament.genes[i] = gg
           #print(str(type(tournament.genes[i])))
       return tournament.getfittest()

   def evolve(self,current_present):
       next_population = Population(self.tour,0)
       for x in range(current_present.populationsize()):
           parent1 = self.tournament_selection(current_present)
           parent2 = self.tournament_selection(current_present)
           child = self.crossover(parent1,parent2)
           next_population.add(child)

       for x in range(next_population.populationsize()):
           self.mutate(next_population.get_gene(x))

       return next_population

