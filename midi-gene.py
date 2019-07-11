from Population import *
from Parameters import *
import os

POPULATION_SIZE = 5000
EPOCHS = 1000000
MUT_RATE = 0.3

# Creates population
pop = Population(POPULATION_SIZE, MUT_RATE)

# Reproduce
for i in range(EPOCHS):
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