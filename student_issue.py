def student_issue_followup1(req):
	output = '''I understand that you are stressed because of an exam. Sometimes when we are facing an obstacle,
				we feel alone even if we are not. Do you study with anyone? If so, what is their name?'''
	return output

def student_issue_followup2(req):
	output = '''It's good to hear that you are studying with ''' + req['slots']['_NAME_']['values'][0] + '''!
				I suggest quizzing each other and you will quickly see that the studying is taking effect, especially
				because we can learn the most from teaching another person.'''
	return output

def student_issue_followup3(req):
	output = '''If you are having difficulty studying by yourself, may I suggest reaching out to someone in your class?
				You may find that people are willing to help you and it will be easier to share the stress with 
				someone else. If you are uncomfortable studying with someone else, then perhaps you can set a more
				reasonable studying schedule, such as studying for 50 minutes and taking a 10 minute break 
				by walking outside.'''
	return output
