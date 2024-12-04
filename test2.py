import random

population = ['Red', 'Blue', 'Green']
weights = [0.6, 0.3, 0.1]

chosen = random.choices(population, weights, k=1)
print(chosen)