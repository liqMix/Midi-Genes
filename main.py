from Parameters import *
from Population import *
from Track import *

PARAMS = Parameters(bpm=120, key='C')
##Creates population
pop = Population(10000, 0.2)

##Reproduce
for i in range(10000000):
  pop.reproduction()

##check the track fitness
hq.nlargest(len(pop.tracks), pop.tracks)[0].fitness

##Download
pattern = midi.read_midifile("backing.mid")
midi.write_midifile("example.mid", hq.nlargest(len(pop.tracks), pop.tracks)[0].outputPattern(pattern))
files.download('example.mid')