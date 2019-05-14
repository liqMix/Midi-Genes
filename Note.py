# Holds the individual note information
import random as rand
from Parameters import *

class Note:
    # initalizes note to parameters or to 0 if none given
    def __init__(self, start=0, duration=0, pitch=0, velocity=0):
        self.start = start
        self.duration = duration
        self.pitch = pitch
        self.velocity = velocity

    # overloads less-than operator for list sorting
    # USES ticks as sort value
    # used at the moment for reorganizing random notes
    # that are out of order in the note list
    def __lt__(self, other):
        return self.start < other.start

    def __repr__(self):
        return "Note(start=%r, duration=%r, pitch=%r, velocity=%r)" % \
               (self.start, self.duration, self.pitch, self.velocity)

    # creates random note
    def random(self, start=0):
        self.start = start
        self.pitch = rand.randrange(PARAMS.PITCH_MIN, PARAMS.PITCH_MAX)
        self.duration = PARAMS.NOTE_DURATION[rand.choice(list(PARAMS.NOTE_DURATION))]
        self.velocity = 100
