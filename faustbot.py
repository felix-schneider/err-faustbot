from errbot.botplugin import BotPlugin
from errbot import botcmd
import random

class FaustBot(BotPlugin):

    def __init__(self):
        super(FaustBot, self).__init__()
        self.parseFaust()
        
    def parseFaust(self):
        sentences = {}
        characters = {}
        i = 0
        newlines = 2
        lastSentence = 0
        with open("faust.txt", encoding="utf-8") as faust:
            for line in faust:
                line = self.removeparentheses(line)
                if line == "\n":
                    newlines += 1
                #if the first few characters are uppercase,
                #there is a new character speaking
                elif (len(line) < 3 and line.isupper()) or line[:3].isupper():
                    characters[i+1] = line[:-2].title()
                    newlines = 0
                    lastSentence = 0
                elif newlines < 2 and not line == "":
                    i += 1
                    newlines = 0
                    if lastSentence == 0:
                        sentences[i] = line[:-1] # no ugly \n
                    else:
                        sentences[lastSentence]+= " \\ " + line[:-1]

                    if line[-2] in ["!", ".", "?"]:
                        lastSentence = 0
                    elif lastSentence == 0:
                        lastSentence = i
        
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
            if argss[0] == "help":
                return "!faust für einen zufälligen Vers. !faust [1.." + str(self.lines) + "]\
 für einen bestimmten und !faust [-" + str(self.lines) + ",-1] für einen bestimmten von hinten."
            try:
                i = int(argss[0])
                if abs(i) > self.lines:
                    err += "Faust hat nur " + str(self.lines) + " Verse. Du kriegst einen anderen:\n"
                elif i == 0:
                    line = 1
                else:
                    if i < 0:
                        line = self.lines - i + 1
                    else:
                        line = i
            except ValueError:
                err += "Das ist keine Zahl. Ich bin mir sicher. Nimm einen zufälligen Vers:\n"
        
        if line == 0:
            line = random.randint(0, self.lines)
        
        whosaidit = self.getnextsmaller(self.characters, line)
        sentence = self.getnextsmaller(self.sentences, line)
        return err + '"{0}", gesprochen von {1} in Vers {2}'.format(sentence, whosaidit, line)
    
    def getnextsmaller(self, d, i):
        last = -1
        for j in iter(sorted(d.keys())):
            if j > i:
                break
            last = j
        return d[last]
    
    def removeparantheses(self, s):
        if "(" not in s and ")" not in s:
            return s
        start = s.find("(")
        if start > 0 and s[start-1] == " ":
            start -= 1
        if start < 0:
            start = 0
        end = s.find(")") + 1
        if end < 0:
            end = len(s)
        return s[:start] + s[end:]