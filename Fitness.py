import midi

NOTE_IN_KEY_REWARD = 15
STARTING_NOTE_REWARD = 2
ENDING_NOTE_PENALTY = -50
JUMP_IN_PITCH_MULT = 2
REVERSE_MOVEMENT_REWARD = 3
TRITONE_PENALTY = -5
REPEATED_LEN_PENALTY = -1


class Fitness:
    def __init__(self, params):
        self.PARAMS = params

    def calc_fitness(self, track):
        fit = self.key_fitness(track)
        fit += self.rule_one(track)
        fit += self.rule_two(track)
        fit += self.rule_three(track)
        fit += self.rule_four(track)
        fit += self.rule_five(track)
        return fit

    # calculates fitness of track based on notes falling within key
    def key_fitness(self, track):
        fit = 0
        for n in track.notes:
            if midi.NOTE_NAMES[(n.pitch % midi.NOTE_PER_OCTAVE)] in self.PARAMS.NOTES_IN_KEY:
                fit += NOTE_IN_KEY_REWARD
        return fit

    # This rule rewards starting and ending notes
    def rule_one(self, track):
        fit = 0
        start_note = midi.NOTE_NAMES[(track.notes[0].pitch % midi.NOTE_PER_OCTAVE)]
        end_note = midi.NOTE_NAMES[(track.notes[-1].pitch % midi.NOTE_PER_OCTAVE)]

        # Start note
        if start_note in [self.PARAMS.NOTES_IN_KEY[0], self.PARAMS.NOTES_IN_KEY[4]]:
            fit += STARTING_NOTE_REWARD

        # End note
        if end_note != self.PARAMS.NOTES_IN_KEY[0]:
            fit += ENDING_NOTE_PENALTY

        return fit

    # This rule penalizes large jumps in pitch
    def rule_two(self, track):
        fit = 0
        for i in range(len(track.notes)):
            if i != 0:
                dist = abs(track.notes[i].pitch - track.notes[i - 1].pitch)
                if dist > 4:
                    fit += dist * JUMP_IN_PITCH_MULT
        return fit

    # This rule rewards jumps in pitch if followed by reverse movement
    def rule_three(self, track):
        fit = 0
        for i in range(len(track.notes)):
            if i != 0 and i != (len(track.notes) - 1):
                current = track.notes[i].pitch
                prev = track.notes[i - 1].pitch
                next = track.notes[i + 1].pitch

                if (current - prev) >= 3:
                    if (next - current) < 0:
                        fit += REVERSE_MOVEMENT_REWARD

                elif (current - prev) <= -3:
                    if (next - current) > 0:
                        fit += REVERSE_MOVEMENT_REWARD

        return fit

    # This rule penalizes a tritone jump
    def rule_four(self, track):
        fit = 0
        fourth = self.PARAMS.NOTES_IN_KEY[3]
        seventh = self.PARAMS.NOTES_IN_KEY[6]
        for i in range(len(track.notes)):
            if i != (len(track.notes) - 1):
                first_note = midi.NOTE_NAMES[(track.notes[i].pitch % midi.NOTE_PER_OCTAVE)]
                second_note = midi.NOTE_NAMES[(track.notes[i + 1].pitch % midi.NOTE_PER_OCTAVE)]
                if (((first_note == fourth) and (second_note == seventh))
                        or ((first_note == seventh) and (second_note == fourth))):
                    fit += TRITONE_PENALTY

        return fit

    # This rule penalizes repeated note lengths
    def rule_five(self, track):
        fit = 0
        for i in range(len(track.notes)):
            if i != (len(track.notes) - 1):
                if track.notes[i].duration == track.notes[i+1].duration:
                    fit += REPEATED_LEN_PENALTY
        return fit
