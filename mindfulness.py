from get_tone import get_tone

def mindfulness_followup1(req):
	# text = req.get('queryResult').get('parameters')   
	# sentiment = get_tone(text['any'])
	query = req
	# Get overall tone
	overall_tone, _ = get_tone(query)
	# If neutral
	print(overall_tone)
	if overall_tone is 'neutral':
		return {'query': '''Great! How are you feeling now?'''}, True

	# If not neutral
	# Get sentence with most emotion to use in Al-i response (shown in our example script)
	sentences = query.split(".")
	maxscore = 0
	maxsentence = ""
	for s in sentences:
		tone, score = get_tone(s)
		print(score)
		# if not tone_dict == "neutral":
		# tODO: In the case of ties, pick the more negative tone
		if score > maxscore:
			maxscore = score
			maxsentence = s

	print(maxsentence)
	output = '''This time, let's describe our surroundings without any judgement, or any emotion. 
	Describe your surroundings as they are, without communicating any feelings about it. 
	Instead of saying ''' + maxsentence + ''', try describing just the facts, just the physical qualities of the space.'''

	print(output)
	# print(tone)
	return {'query':output}, False



def mindfulness_followup2(req):
	query = req
	# Get overall tone
	overall_tone, _ = get_tone(query)
	# If neutral
	print(overall_tone)
	if overall_tone is 'neutral':
		return {'query': '''Great! How are you feeling now?'''}, True

	# If not neutral
	# Get sentence with most emotion to use in Al-i response (shown in our example script)
	words = query.split()
	maxscore = 0
	maxword = ""
	for w in words:
		tone, score = get_tone(w)
		print(w)
		# if not tone_dict == "neutral":
		# tODO: In the case of ties, pick the more negative tone
		if score > maxscore:
			maxscore = score
			maxword = w

	print(maxword)
	output = '''That was better. I noticed that you're still having feelings about ''' + maxword + '''. 
	Sometimes our emotions can affect our perception of what's going on around us. 
	Let's try one more time, but this time just describe ''' + maxword + ''' without any feeling at all. 
	Describe physical characteristics, and facts about ''' + maxword + '''.'''
	print(output)
	# print(tone)
	return {'query':output}, False

def mindfulness_followup3(req):
	return {'query': '''Great! How are you feeling now?'''}, True

