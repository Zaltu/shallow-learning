from random import randint as guess
import json

# TODO IS_NOT

class Mind(object):
    def __init__(self):
        self.vocabulary = {
            "sky":{"function":"noun", "follow_type":[], "follow_weight":["is", "blue"], "is":["blue"]},
            "is":{"function":"verb", "follow_type":[], "follow_weight":["the", "blue", "green", "tall"], "is":[]},
            "blue":{"function":"adjective", "follow_type":[], "follow_weight":[], "is":["sky"]},
            "the":{"function":"article", "follow_type":[], "follow_weight":["sky", "grass"], "is":[]},
            "green":{"function":"adjective", "follow_type":[], "follow_weight":[], "is":["grass"]},
            "grass":{"function":"noun", "follow_type":[], "follow_weight":["is", "green", "tall"], "is":["green", "tall"]},
            "tall":{"function":"adjective", "follow_type":[], "follow_weight":[], "is":["grass"]},
            "trains":{"function":"noun", "follow_type":[], "follow_weight":[], "is":[]},
            "I":{"function":"pronoun", "follow_type":[], "follow_weight":["like"], "is":["trains"]}, # "I" has as property user attributes.
            "like":{"function":"verb", "follow_type":[], "follow_weight":["trains", "the"], "is":[]}
        }

        self.structures = [
            ["article", "noun", "verb", "adjective"],
            ["verb", "article", "adjective", "noun"],
            ["pronoun", "verb", "noun"],
            ["pronoun", "verb", "article", "noun"],
            ["pronoun", "verb", "article", "adjective", "noun"]
        ]

        self.word_types = {
            "article":["the"],
            "noun":["sky", "grass", "trains"],
            "verb":["is", "like"],
            "adjective":["blue", "green", "tall"],
            "pronoun":["I"],
            None: []
        }


    def memorize(self):
        with open('memory.json', 'w') as memory:
            memory.write(json.dumps({'vocabulary':self.vocabulary,
                                     'structures':self.structures,
                                     'word_types':self.word_types}))
        print "Got it!"


    def remember(self):
        #thoughts = []
        with open('memory.json', 'r') as memory:
            thoughts = json.loads(memory.read())
            self.vocabulary = thoughts['vocabulary']
            self.structures = thoughts['structures']
            self.word_types = thoughts['word_types']



    def speak(self):
        # Pick random sentence structure
        struc = self.structures[guess(0, len(self.structures)-1)]
        sentence = ""
        flw_possibilities = []
        is_possibilities = []
        last_word = None
        for word_type in struc:
            for word in self.word_types[word_type]:
                if last_word and word in self.vocabulary[last_word]["follow_weight"]:
                    flw_possibilities.append(word)
            for possible in flw_possibilities:
                if set(self.vocabulary[possible]["is"]).intersection(set(sentence.split(" "))):
                    is_possibilities.append(possible)
            if not last_word and not flw_possibilities:
                last_word = self.word_types[word_type][guess(0, len(self.word_types[word_type])-1)]
                sentence += last_word
            elif is_possibilities:
                last_word = is_possibilities[guess(0, len(is_possibilities)-1)]
                sentence += last_word
            elif flw_possibilities:
                last_word = flw_possibilities[guess(0, len(flw_possibilities)-1)]
                sentence += last_word
            flw_possibilities = []
            is_possibilities = []
            sentence += " "

        sentence = sentence[0].upper() + sentence[1:-1] + "."
        return sentence

    def listen(self, sentence):
        new_words = []
        sentenceL = sentence.split(" ")
        for word in sentenceL:
            structurematch = []
            if word in self.vocabulary:
                structurematch.append(self.vocabulary[word]["function"])
            else:
                self.vocabulary[word] = {"function":"", "follow_type":[], "follow_weight":[], "is":[]}
                structurematch.append(None)
                new_words.append(word)  # TEMP
            if sentenceL.index(word) != 0:
                self.vocabulary[sentenceL[sentenceL.index(word)-1]]["follow_weight"].append(word)

        for word in new_words:
            self.learn(word)

        thisStructure = []
        for word in sentenceL:
            thisStructure.append(self.vocabulary[word]['function'])
        if thisStructure not in self.structures:
            self.structures.append(thisStructure)


    def learn(self, word):
        wtype = raw_input("What word type is this? \""+word+"\":\n")
        self.word_types[wtype].append(word)
        self.vocabulary[word]['function'] = wtype



MIND = Mind()

MIND.remember()

print MIND.speak()
MIND.listen("I like cars")
print MIND.speak()

MIND.memorize()
