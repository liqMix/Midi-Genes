from Track import *
import heapq as hq


# Population to apply GAs
class Population:
    pop_size = 0
    mut_rate = 0
    tracks = []

    def __init__(self, pop_size, mut_rate):
        self.pop_size = pop_size
        self.mut_rate = mut_rate
        self.tracks = []

        # seeds the initial population with fitnesses over 0
        for i in range(pop_size):
            track = Track()
            track.random()

            while track.fitness <= 0:
                track.random()

            hq.heappush(self.tracks, track)

    def reproduction(self):
        # kill the two weakest
        dead = hq.heappop(self.tracks)
        dead = hq.heappop(self.tracks)

        # grab two random
        parent_one = self.tracks[rand.randrange(len(self.tracks))]
        parent_two = self.tracks[rand.randrange(len(self.tracks))]

        # and they make babiez :)
        self.crossover(parent_one, parent_two)

    def crossover(self, parent_one, parent_two):
        parent_one_len = len(parent_one.notes)
        parent_two_len = len(parent_two.notes)
        len_min = min(parent_one_len, parent_two_len)
        len_max = max(parent_one_len, parent_two_len)

        child_one = Track()
        child_two = Track()

        index = rand.randrange(len_min)
        # cross-over
        for i in range(len_max):

            # if we go past one parent, lets continue adding to the other child
            if i >= parent_one_len:
                while i < parent_two_len:
                    child_one.notes.append(parent_two.notes[i])
                    i += 1

            elif i >= parent_two_len:
                while i < parent_one_len:
                    child_two.notes.append(parent_one.notes[i])
                    i += 1

            elif i > index:
                child_one.notes.append(parent_one.notes[i])
                child_two.notes.append(parent_two.notes[i])
            else:
                child_one.notes.append(parent_two.notes[i])
                child_two.notes.append(parent_one.notes[i])

                # sort the notes since the cross-over mixed their start times
        child_one.notes.sort()
        child_two.notes.sort()

        # remove any notes that have same start-times
        child_one.remove_dup()
        child_two.remove_dup()

        # normalize
        child_one.normalize()
        child_two.normalize()

        if rand.random() <= self.mut_rate:
            child_one = self.mutate(child_one)
        if rand.random() <= self.mut_rate:
            child_two = self.mutate(child_two)

        # calc the fit
        child_one.calcFitness()
        child_two.calcFitness()

        # push them to the priority queue heap
        hq.heappush(self.tracks, child_one)
        hq.heappush(self.tracks, child_two)

    # clamps the value to min and max pitch, increases the pitch by 12
    # to get the same note in higher octave
    def mutate(self, child):
        NOTES_IN_KEY = PARAMS.NOTES_IN_KEY
        index = rand.randrange(len(child.notes))
        note = midi.NOTE_NAMES[(child.notes[index].pitch % midi.NOTE_PER_OCTAVE)]

        if (note == NOTES_IN_KEY[2]) or (note == NOTES_IN_KEY[6]):
            child.notes[index].pitch += rand.choice((-2, 1))
        elif (note == NOTES_IN_KEY[0]) or (note == NOTES_IN_KEY[3]):
            child.notes[index].pitch += rand.choice((-1, 2))
        elif ((note == NOTES_IN_KEY[1]) or (note == NOTES_IN_KEY[4])) or (note == NOTES_IN_KEY[5]):
            child.notes[index].pitch += rand.choice((-2, 2))
        else:
            child.notes[index].pitch += rand.choice((-1, 1))

        if child.notes[index].pitch > PARAMS.PITCH_MAX:
            child.notes[index].pitch -= 12
        elif child.notes[index].pitch < PARAMS.PITCH_MIN:
            child.notes[index].pitch += 12

        return child
