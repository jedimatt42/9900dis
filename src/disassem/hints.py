class Hints:
    def __init__(self, outputfile):
        self.annotations = {}
        self.labels = {}
        with open(outputfile, "r") as listing:
            for line in listing.readlines():
                segments = line.split(';')
                if len(segments) >= 2 and "f:" in segments[1]:
                    (pc, w, f) = self.deconstruct_notes(segments[1])
                    if f:
                        self.annotations[pc] = f.rstrip()
                label = segments[0].split('\t')[0]
                if label:
                    parts = segments[1].split(" ")
                    pc = int(parts[1][4:], 16)
                    self.labels[pc] = label.strip()

    def deconstruct_notes(self, value):
        parts = value.split(" ")
        if len(parts) != 4:
            return (None, None, None)
        pc = int(parts[1][4:], 16)
        w = int(parts[2][3:], 16)
        f = parts[3]
        return (pc, w, f)

    def format_note(self, pc):
        if pc is not None and pc in self.annotations.keys():
            return self.annotations[pc]
        return ""

    def label(self, pc):
        if pc is not None and pc in self.labels.keys():
            return self.labels[pc]
        return ""
