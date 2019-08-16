import midi
import os
import sys
import heapq as hq
import argparse
from Parameters import Parameters
from Fitness import Fitness

# Create the argument parser
parser = argparse.ArgumentParser('Generates melodies using a evolutionary model of fitness.')
parser.add_argument('-note', help='The note of the musical key.', default='C')
parser.add_argument('-scale', help='The scale of the musical key.', default='major', choices=['major', 'minor'])
parser.add_argument('-bpm', help='The speed of the music. (Beats per Minute)', default=120, type=int)
parser.add_argument('-pop_size', help='The number of tracks in the population.', default=5000, type=int)
parser.add_argument('-epochs', help='The number of reproduction cycles.', default=5000, type=int)
parser.add_argument('-mut_rate', help='The rate at which notes within a reproducing track mutate.', default=0.05,
                    type=float)
parser.add_argument('-instrument', help='The instrument playing the generated melody.', default=0, type=int)
parser.add_argument('-bass', help='Whether to attach the bass backing track.', default='true', choices=['true', 'false'])
parser.add_argument('-drums', help='Whether to attach the drum backing track.', default='true', choices=['true', 'false'])

args = parser.parse_args()
args.note = args.note.upper()

# Create note parameters
PARAMS = Parameters(bpm=args.bpm, note=args.note, scale=args.scale)
FIT = Fitness(PARAMS)

if __name__ == "__main__":

    # Import population after defining parameters
    from Population import Population

    # Creates population
    pop = Population(args.pop_size, args.mut_rate)

    print('Parameters: ', vars(args))
    print('\nGenerating...\n')
    # Reproduce
    for i in range(args.epochs):
        pop.reproduction()

        sys.stdout.write("\r\x1b[K" + 'Epoch ' + str(i+1) + ' / ' + str(args.epochs))
        sys.stdout.flush()

    # Grab the top track
    best = hq.nlargest(len(pop.tracks), pop.tracks)[0]
    fitness = best.fitness

    # Grab midi backing track which serves as a midi template
    if args.scale is 'major':
        backing = midi.read_midifile("data/backing.mid")
    elif 'minor':
        backing = midi.read_midifile("data/backing-minor.mid")

    # Write the generated midi file to disk
    p = "output/output"
    path = p + ".mid"
    i = 0

    while os.path.exists(path):
        path = p + str(i) + ".mid"
        i += 1

    output_midi = best.output_pattern(backing, {'bass': args.bass, 'drums': args.drums}, instrument)
    midi.write_midifile(path, output_midi)

    print("\nSaved output midi as " + path + "\n Ending fitness: " + str(fitness))
