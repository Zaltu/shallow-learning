from random import randint as guess

# TODO IS_NOT

vocabulary = {
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

structures = [
	["article", "noun", "verb", "adjective"],
	["verb", "article", "noun", "adjective"],
	["pronoun", "verb", "noun"],
	["pronoun", "verb", "article", "noun"]
]

word_types = {
	"article":["the"],
	"noun":["sky", "grass", "trains"],
	"verb":["is", "like"],
	"adjective":["blue", "green", "tall"],
	"pronoun":["I"]
}

def speak():
	# Pick random sentence structure
	struc = structures[3]
	sentence = ""
	flw_possibilities = []
	is_possibilities = []
	last_word = None
	for word_type in struc:
		for word in word_types[word_type]:
			if last_word and word in vocabulary[last_word]["follow_weight"]:
				flw_possibilities.append(word)
		for possible in flw_possibilities:
			if set(vocabulary[possible]["is"]).intersection(set(sentence.split(" "))):
				is_possibilities.append(possible)
		if not last_word and not flw_possibilities:
			last_word = word_types[word_type][guess(0, len(word_types[word_type])-1)]
			sentence+= last_word
		elif is_possibilities:
			last_word = is_possibilities[guess(0, len(is_possibilities)-1)]
			sentence+= last_word
		elif flw_possibilities:
			last_word = flw_possibilities[guess(0, len(flw_possibilities)-1)]
			sentence+= last_word
		flw_possibilities = []
		is_possibilities = []
		sentence+= " "
		
	sentence = sentence[0].upper() + sentence[1:-1] + "."
	return sentence

def listen(input):
	pass
	
print speak()