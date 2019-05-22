from Population import *
from Parameters import *
import os

POPULATION_SIZE = 2500
EPOCHS = 100000


# Creates population
pop = Population(2500, 0.3)

# Reproduce
for i in range(100000):
    pop.reproduction()
    print("Epoch {} finished.".format(i))

# Check the track fitness
fitness = hq.nlargest(len(pop.tracks), pop.tracks)[0].fitness

# Grab midi backing track which serves as a midi template
pattern = midi.read_midifile("data/backing.mid")

# Write the generated midi file to disk
p = "output/output"
path = p + ".mid"
i = 0
while os.path.exists(path):
    path = p + str(i) + ".mid"
    i += 1

midi.write_midifile(path, hq.nlargest(len(pop.tracks), pop.tracks)[0].output_pattern(pattern))

print("Saved output midi as " + path + "\n Ending fitness: " + str(fitness))