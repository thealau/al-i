from get_tone import get_tone

def mindfulness(req):
	# print (req['payload']['inputs']['rawInputs']['query'])
	return {'fulfillmentText':"Let’s try an observation exercise. It can be hard to be present in the moment, especially when we’re feeling anxious or overwhelmed with emotions. Let’s try and get back to the present and tackle the issues causing our anxiety later. Can you tell me about the environment around you? Describe it in depth, even as far as telling me the colors of the walls, and the physical sensations that you’re feeling in the moment."}

def mindfulness_first(req):
	query = req.get('queryResult').get('queryText')

	# if get_tone
	# get_tone()
	# Get 
	sentences = query.split(".")
	maxscore = 0
	maxsentence = ""
	for s in sentences:
		tone_dict = get_tone(s)
		# if not tone_dict == "neutral":
		if tone_dict['score'] > maxscore:
			maxscore = tone_dict['score']
			maxsentence = s


	print(maxsentence)
	# print(tone)
	return {'fulfillmentText':maxsentence}