from errbot.botplugin import BotPlugin
from errbot import botcmd
import random

class FaustBot(BotPlugin):

    def __init__(self):
        super(FaustBot, self).__init__()
        self.parseFaust()

    def parseFaust(self):
        faust = open("faust.txt", encoding="utf-8")
        sentences = {}
        characters = {}
        line = faust.readline()
        i = 0
        newlines = 2
        lastSentence = 0

        while line != "":
            if line == "\n":
                newlines += 1
            #if the first few characters are uppercase,
            #there is a new character speaking
            elif (len(line) < 3 and line.isupper()) or line[:3].isupper():
                characters[i+1] = line[:-2]
                newlines = 0
                lastSentence = 0
            elif newlines < 2 and not line.startswith("("):
                i += 1
                newlines = 0
                if lastSentence == 0:
                    sentences[i] = line[:-1] # no ugly \n
                else:
                    sentences[lastSentence]+= "\\ " + line[:-1]

                if line[-2] in ["!", ".", "?"]:
                    lastSentence = 0
                elif lastSentence == 0:
                    lastSentence = i
            line = faust.readline()

        faust.close()
        self.sentences = sentences
        self.characters = characters
        self.lines = i

    @botcmd
    def faust(self, mess, args):
        """ Print a random line from Goethe's "Faust" in sentence context """
        argss = args.split(' ')
        line = 0
        err = ""
        if len(argss) != 0:
            if argss[0].isnumeric():
                i = int(argss[0])
                if abs(i) > self.lines:
                    err += "Faust hat nur " + str(self.lines) + " Verse.\n"
                elif i == 0:
                    line = 1
                else:
                    if i < 0:
                        line = self.lines - i + 1
                    else:
                        line = i

        if line == 0:
            line = random.randint(0, self.lines)

        whosaidit = self.getNextSmaller(self.characters, line)
        sentence = self.getNextSmaller(self.sentences, line)
        return err + '"{0}", gesprochen von {1} in Vers {2}'.format(sentence, whosaidit, line)

    def getNextSmaller(self, d, i):
        last = -1
        for j in iter(sorted(d.keys())):
            if j > i:
                break
            last = j
        return d[last]
