class Address:
    def __init__(self, value):
        self.value = int(value, 16)

    def __str__(self):
        return "{0:#0{1}x}".format(self.value, 6)