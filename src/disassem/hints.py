import os


class Hints:
    def __init__(self, outputfile):
        self.annotations = {}
        self.labels = {}
        self.comments = {}
        if os.path.isfile(outputfile):
            with open(outputfile, "r") as listing:
                for line in listing.readlines():
                    segments = line.split(';')
                    if len(segments) >= 2:
                        (pc, w, f) = self.deconstruct_notes(segments[1])
                        if f:
                            self.annotations[pc] = f.strip()
                        label = segments[0].split('\t')[0].strip()
                        if label:
                            self.labels[pc] = label
                        if len(segments) >= 3:
                            self.comments[pc] = segments[2].strip()

    def deconstruct_notes(self, value):
        parts = value.split(" ")
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

    def comment(self, pc):
        if pc is not None and pc in self.comments.keys():
            return f"\t; {self.comments[pc]}"
        return ""
