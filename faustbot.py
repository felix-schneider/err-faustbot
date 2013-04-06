# coding=utf-8

from errbot.botplugin import BotPlugin
from errbot import botcmd
import random

class FaustBot(BotPlugin):

    def __init__(self):
        super(FaustBot, self).__init__()
        self.parseFaust()

    def parseFaust(self):
        # The sentence database
        faustdb = {}

        # Current line number
        linenumber = 0

        # Currently speaking character
        character = ""

        # The line where the current sentence started
        contline = 1

        # Whether the current sentence is a continuation of a previous sentence
        sentencecont = False

        with open("faust.txt", encoding="utf-8") as faust:
            for line in faust:
                line = line.strip()

                # determine line type
                if line.startswith("%%%"):
                    # new character speaking
                    character = line[3:-1] # strip out %%% and trailing dot
                    sentencecont = False # new character starts new sentence
                    continue

                elif line.startswith("###"):
                    # line number check
                    if int(line[3:]) != (linenumber + 1):
                        raise Exception("Zeile " + str(linenumber + 1) + ", erwartet " + line[3:])
                    continue

                elif line.startswith("+++"):
                    # continued line with different character, line number does not change
                    line = line[3:]

                else:
                    # normal line
                    linenumber += 1

                # write line to faustdb
                if len(line) == 0:
                    continue

                if not sentencecont:
                    # no continued sentence: put sentence into database with current line number
                    if linenumber not in faustdb:
                        faustdb[linenumber] = []
                    faustdb[linenumber].append((character, [line]))
                else:
                    # continued sentence: append line to what the last character said in line "contline"
                    faustdb[contline][-1][1].append(line)

                # Check whether the sentence ends at the end of the current line.
                if line[-1] in ["!", ".", "?"]:
                    sentencecont = False
                else:
                    # do not update contline if the current sentence is already a continued sentence
                    if not sentencecont:
                        contline = linenumber
                    sentencecont = True

        self.faustdb = faustdb

    @botcmd
    def faust(self, mess, args):
        """ Print a random line from Goethe's "Faust" in sentence context """
        argss = args.split(' ')
        line = 0
        err = ""
        if len(argss) != 0:
            if argss[0] == "help":
                return "!faust für einen zufälligen Vers. !faust [1.." + str(len(self.faustdb)) + "]\
 für einen bestimmten und !faust [-" + str(len(self.faustdb)) + ",-1] für einen bestimmten von hinten."
            try:
                i = int(argss[0])
                if abs(i) > len(self.faustdb):
                    err += "Faust hat nur " + str(len(self.faustdb)) + " Verse. Du kriegst einen anderen:\n"
                elif i == 0:
                    line = 1
                else:
                    if i < 0:
                        line = len(self.faustdb) - i + 1
                    else:
                        line = i
            except ValueError:
                err += "Das ist keine Zahl. Ich bin mir sicher. Nimm einen zufälligen Vers:\n"

        if line == 0:
            line = random.randint(0, len(self.faustdb))

        actual_line = self.getnextsmallerkey(self.faustdb, line)
        sentences = self.faustdb[actual_line]

        # TODO only the first/last sentence on this line will be printed.
        if actual_line < line:
            sentence = sentences[-1]
        else:
            sentence = sentences[0]

        return err + '"{0}", gesprochen von {1} in Vers {2}'.format(" / ".join(sentence[1]), sentence[0].upper(), actual_line)

    def getnextsmallerkey(self, d, i):
        last = -1
        for j in iter(sorted(d.keys())):
            if j > i:
                break
            last = j
        return last