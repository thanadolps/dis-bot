# Brainfuck-python-interpreter
# https://github.com/thanadolps/Brainfuck-python-interpreter

class BF:
    data = [0]
    index = 0

    def __init__(self, will_return=True):
        self.will_return = will_return


    def _extendTo(self, index):
        while index >= len(self.data):
            self.data.append(0)

    def add(self):
        self.data[self.index] += 1

    def subtract(self):
        if self.data[self.index] > 0:
            self.data[self.index] -= 1

    def right(self):
        if self.index + 1 >= len(self.data):
            self.data.append(0)
        self.index += 1

    def left(self):
        self.index -= 1

    def findMatch(self, index, command):
        c = 0
        for i in range(index, len(command)):
            t = command[i]
            if t == '[':
                c += 1
            if t == ']':
                if c == 1:
                    return i
                else:
                    c -= 1

    def compile(self, command, top=True):
        i = 0
        out = ""
        while i < len(command):
            t = command[i]
            if t == '+':
                self.add()
            elif t == '-':
                self.subtract()
            elif t == '>':
                self.right()
            elif t == '<':
                self.left()
            elif t == '[':
                k = self.findMatch(i, command)
                while self.data[self.index] != 0:
                    self.compile(command[i + 1:k],top = False)
                i = k
            elif t == ',':
                self.data[self.index] = ord(input())
            elif t == '.':
                out += chr(self.data[self.index])
                print('Dot {}'.format(self.data))

            i += 1

        if top :
            if self.will_return:
                return out
            else :
                print(out)