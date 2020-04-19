from classes import Dataset
from classes import Classifier
from classes import Classifier_random
from classes import Generation
from classes import First_Generation
import time
import pickle

t=time.time()
data_1 = '\\flowers\\daisy'
data_2 = '\\flowers\\tulip'
data = Dataset(data_1,data_2)
#with open('test_dataset.pickle', 'rb') as handle:
#    data = pickle.load(handle)

print('---Data Loaded('+str(round(time.time()-t,2))+'s)---\n')

t=time.time()
g = First_Generation(500) #The number of individuals in all the generations is the same
g.evaluate(data)
print(f'Génération 1  ({round(time.time()-t,2)}s)')
print(g)

for i in range (2,100):
    t=time.time()
    g = g.make_new_gen(150, mutation_rate=0.005)
    g.evaluate(data)
    print(f'\nGénération {i}  ({round(time.time()-t,2)}s)')
    print(g)

data.save()
g.save_evolution('500indiv_fulldata_20epochs.pickle')
