from Note import *
import midi


class Track:
    # Holds the notes and BPM for a given track

    # Serves effectively as a "genome" for our use, with the
    # notes list serving as the "alleles"

    # A track is a list of notes, a number describing the number of notes, and a
    # bpm which gives time context to ticks
    # 
    # Each note is
    #         name                desc                         range
    #      start tick     the tick the note begins at         0 - inf
    #      duration       how many ticks the note lasts       0 - inf
    #      pitch          what the note's sound is            0 - 127
    #      velocity       how hard the note is played         0 - 127
    # 
    # more info on pitch (might be relevant for heuristics):
    #             There are 12 notes in total
    #        C  C#  D  D#  E  F  F#  G  G#  A  A#  B
    # pitch  0  1   2  3   4  5  6   7  8   9  10  11
    # 
    #        These repeat until the max value of 127 (which happens to be a G)
    #        Each repetition is called an Octave, with 0-11 being octave 1,
    #        12-23 octave 2, etc...
    # 
    #        You can get the note name by calling
    #             midi.NOTE_NAMES[note.pitch % midi.OCTAVE_MAX_VALUE]
    #        where note.pitch is the note you want the name of

    # List of notes in the track
    notes = []
    fitness = 0

    def __init__(self):
        self.notes = []
        self.num = 0
        self.fitness = 0

    # overloads the print operation
    def __repr__(self):
        for note in self.notes:
            print(self.notes.index(note), " ", note)
        return " "

    # overloads the less than operator
    def __lt__(self, other):
        return self.fitness < other.fitness

    # Outputs the track as a midi.Pattern to be encoded back into a midi file
    # by the midi module
    # 
    # NEEDS the input pattern in order to reattach certain parts
    def output_pattern(self, pattern):
        output = midi.Pattern(resolution=pattern.resolution)
        output.append(pattern[0])
        track = midi.Track()
        track.append(pattern[1][0])
        track.append(midi.ProgramChangeEvent(tick=0, channel=2, data=[0]))

        # for event in pattern[1]:
        # if isinstance(event, midi.NoteOnEvent):
        #    break
        #  track.append(event)

        for note in self.notes:
            track.append(midi.NoteOnEvent(tick=note.start, channel=2,
                                          pitch=note.pitch,
                                          velocity=note.velocity))

            track.append(midi.NoteOffEvent(tick=(note.start + note.duration),
                                           channel=2,
                                           pitch=note.pitch,
                                           velocity=100))

        track.append(midi.EndOfTrackEvent(tick=PARAMS.END_TICK))
        track.tick_relative = False
        track.make_ticks_rel()

        for e in track:
            if isinstance(e, midi.NoteOnEvent):
                e.tick = 0

        output.append(track)
        output.append(pattern[2])
        output.append(pattern[3])
        return output

    # creates random notes and stores them in its note list
    def random(self):
        self.notes = []
        self.num = 65
        temp_note = Note()
        temp_note.random(0)
        self.notes.append(temp_note)

        for x in range(0, self.num - 1):
            temp_note = Note()
            temp_note.random(self.notes[-1].start + self.notes[-1].duration)

            if temp_note.start >= PARAMS.LAST_NOTE:
                temp_note.start = PARAMS.LAST_NOTE
                temp_note.duration = PARAMS.NOTE_DURATION["WHOLE"]

                for n in self.notes:
                    if (n.start + n.duration) >= PARAMS.LAST_NOTE:
                        del n

                self.notes.append(temp_note)
                return self.calc_fitness()

            self.notes.append(temp_note)

    # removes notes with same start tick
    def remove_dup(self):
        i = 1

        while i < len(self.notes):
            if (self.notes[i].start == self.notes[i - 1].start) or (self.notes[i].start > PARAMS.LAST_NOTE):
                del self.notes[i]
                i -= 1
            i += 1

    # restructures the note start times after readjusting the last note
    def normalize(self):
        i = len(self.notes) - 1

        self.notes[i].start = PARAMS.LAST_NOTE
        self.notes[i].duration = PARAMS.NOTE_DURATION["WHOLE"]
        while i > 0:
            self.notes[i - 1].start = self.notes[i].start - self.notes[i - 1].duration
            i -= 1
            if self.notes[i].start <= 0:
                self.notes[i].start = 0
                self.notes[i].duration = self.notes[i + 1].start
                i -= 1
                break

        while i >= 0:
            del self.notes[i]
            i -= 1

    # # # # # # # # # # # # #  FITNESS SECTION # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # calculates fitness based on parameters
    def calc_fitness(self):
        self.fitness = self.apply_rules()

    def apply_rules(self):
        fit = 0
        fit = self.key_fitness()
        fit += self.rule_one()
        fit += self.rule_two()
        fit += self.rule_three()
        fit += self.rule_four()
        return fit

    # calculates fitness of track based on notes falling within key
    def key_fitness(self):
        fit = 0
        for n in self.notes:
            if midi.NOTE_NAMES[(n.pitch % midi.NOTE_PER_OCTAVE)] in PARAMS.NOTES_IN_KEY:
                fit += 200
            else:
                fit -= 100
        return fit

    # This rule rewards starting and ending notes
    def rule_one(self):
        fit = 0

        # Start note
        if (midi.NOTE_NAMES[(self.notes[0].pitch % midi.NOTE_PER_OCTAVE)]
                == (PARAMS.NOTES_IN_KEY[0] or PARAMS.NOTES_IN_KEY[4])):
            fit += 200

        # End note
        if (midi.NOTE_NAMES[(self.notes[-1].pitch % midi.NOTE_PER_OCTAVE)]
                != PARAMS.NOTES_IN_KEY[0]):
            fit -= 100
        else:
            fit += 200

        return fit

    # This rule penalizes large jumps in pitch
    def rule_two(self):
        fit = 0
        for i in range(len(self.notes)):
            if i != 0:
                dist = abs(self.notes[i].pitch - self.notes[i - 1].pitch)
                if dist != 2:
                    fit -= dist * 5
        return fit

    # This rule rewards jumps in pitch if followed by reverse movement
    def rule_three(self):
        fit = 0
        for i in range(len(self.notes)):
            if i != 0 and i != (len(self.notes) - 1):
                if ((self.notes[i].pitch - self.notes[i - 1].pitch)
                        >= 3):
                    if self.notes[i + 1].pitch - self.notes[i].pitch < 0:
                        fit += 50
                    else:
                        fit -= 100

                elif (self.notes[i].pitch - self.notes[i - 1].pitch) <= -3:
                    if self.notes[i + 1].pitch - self.notes[i].pitch > 0:
                        fit += 50
                    else:
                        fit -= 100

        return fit

    # This rule penalizes a tritone jump
    def rule_four(self):
        fit = 0
        for i in range(len(self.notes)):
            if i != (len(self.notes) - 1):
                firstNote = midi.NOTE_NAMES[(self.notes[i].pitch % midi.NOTE_PER_OCTAVE)]
                secondNote = midi.NOTE_NAMES[(self.notes[i + 1].pitch % midi.NOTE_PER_OCTAVE)]
                if (((firstNote == PARAMS.NOTES_IN_KEY[3]) and (secondNote == PARAMS.NOTES_IN_KEY[6]))
                        or ((firstNote == PARAMS.NOTES_IN_KEY[6]) and (secondNote == PARAMS.NOTES_IN_KEY[3]))):
                    fit -= 250

        return fit
