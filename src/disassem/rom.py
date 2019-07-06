
mne351 = {
    0b101: "A",
    0b100: "C",
    0b011: "S",
    0b111: "SOC",
    0b010: "SZC",
    0b110: "MOV"
}

mne352 = {
    0b001000: "COC",
    0b001001: "CZC",
    0b001010: "XOR",
    0b001110: "MPY",
    0b001111: "DIV"
}


class ROM:
    def __init__(self, rompath, listpath):
        self.filename = rompath
        self.output = listpath

    def readword(self, rom):
        bytes = rom.read(2)
        if bytes == b"":
            return None
        return (bytes[0] << 8) + bytes[1]

    def word_to_hex(self, value):
        return ">" + "{0:#0{1}x}".format(value, 6)[2:]

    def deconstruct351(self, word):
        opcode = (word & 0xE000) >> 13
        b = (word & 0x1000) >> 12
        td = (word & 0x0C00) >> 10
        d = (word & 0x03C0) >> 6
        ts = (word & 0x0030) >> 4
        s = word & 0x000F
        return (opcode, b, td, d, ts, s)

    def mneumonic351(self, opcode, b):
        result = mne351[opcode]
        if b:
            result += 'B'
        return result

    def deconstruct352(self, word):
        opcode = (word & 0xFC00) >> 10
        d = (word & 0x03C0) >> 6
        ts = (word & 0x0030) >> 4
        s = (word & 0x000F)
        return (opcode, d, ts, s)

    def param351(self, t, v, rom):
        param = ""
        if t == 2:
            param = "@" + self.word_to_hex(self.readword(rom))
            if v != 0:
                param += "(r"
                param += str(v)
                param += ")"
            return param
        if (t == 0 or t == 1 or t == 3):
            if t == 1 or t == 3:
                param += "*"
            param += "r" + str(v)
            if t == 3:
                param += "+"
            return param
        return "error(t_%d)" % t

    def handle351(self, word, listing, rom):
        (opcode, b, td, d, ts, s) = self.deconstruct351(word)
        if opcode not in mne351.keys():
            return False
        src_param = self.param351(ts, s, rom)
        dst_param = self.param351(td, d, rom)
        line = "\t%s\t%s,%s" % (
            self.mneumonic351(opcode, b), src_param, dst_param
        )
        print(line, file=listing)
        return True

    def handle352(self, word, listing, rom):
        (opcode, d, ts, s) = self.deconstruct352(word)
        if opcode not in mne352.keys():
            return False
        src_param = self.param351(ts, s, rom)
        dst_param = "r" + str(d)
        line = "\t%s\t%s,%s" % (mne352[opcode], src_param, dst_param)
        print(line, file=listing)
        return True

    def handleData(self, word, listing):
        line = "\tDATA\t%s" % self.word_to_hex(word)
        print(line, file=listing)
        return True

    def disassemble(self):
        with open(self.output, "w") as listing:
            with open(self.filename, "rb") as rom:
                word = self.readword(rom)
                while(word is not None):
                    self.handle351(word, listing, rom)
                    self.handle352(word, listing, rom)
                    self.handleData(word, listing)

                    word = self.readword(rom)
