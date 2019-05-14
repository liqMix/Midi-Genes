KEY_MAP = {
    'C': 0,
    'C#': 1,
    'D': 2,
    'D#': 3,
    'E': 4,
    'F': 5,
    'F#': 6,
    'G': 7,
    'G#': 8,
    'A': 9,
    'A#': 10,
    'B': 11
}

INV_KEY_MAP = {v: k for k, v in KEY_MAP.items()}
MAJOR_STEPS = [0, 2, 4, 5, 7, 9, 11]


class Parameters:
    def __init__(self, bpm, key):

        # Pitch Parameters
        self.PITCH_MAX = 72
        self.PITCH_MIN = 48
        self.NOTES_IN_KEY = []
        self.key = KEY_MAP[key]
        for m in MAJOR_STEPS:
            self.NOTES_IN_KEY.append(INV_KEY_MAP[(m+self.key) % len(KEY_MAP)])

        # Duration constants
        self.BPM = bpm
        self.NOTE_DURATION = {
            "WHOLE": self.BPM * 16,
            "HALF" : self.BPM * 8,
            "QUARTER": self.BPM * 4,
            "EIGHTH": self.BPM * 2
        }

        self.END_TICK = 17280
        self.LAST_NOTE = self.END_TICK - self.NOTE_DURATION["WHOLE"]


PARAMS = Parameters(bpm=120, key='C')
