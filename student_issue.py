def student_issue_followup1(req):
	output = '''I understand that you are stressed because of an exam. Sometimes when we are facing an obstacle, we feel alone even if we are not. Do you study with anyone? If so, what is their name?'''
	return output

def student_issue_followup2(req):
	output = '''It's good to hear that you are studying with ''' + req['slots']['_STUDENT_NAME_']['values'][0]['tokens'] + '''! I suggest quizzing each other and you will quickly see that the studying is taking effect, especially because we can learn the most from teaching another person.'''
	return output

def student_issue_followup3(req):
	output = '''If you are having difficulty studying by yourself, may I suggest reaching out to someone in your class? You may find that people are willing to help you and it will be easier to share the stress with someone else. If you are uncomfortable studying with someone else, then perhaps you can set a more reasonable studying schedule, such as studying for 50 minutes and taking a 10 minute break by walking outside.'''
	return output

def student_issue_homework_worried(req):
	output = '''Remember that the goal of homework is to only help you build foundations. Not being able to complete it will not be the end of the world! What course is this assignment for?'''
	return output

def student_issue_homework(req):
	output = '''I have got some advice that can help out with homework! What type of course is this?'''
	return output

def student_issue_homework_webwork(req):
	output = '''A great strategy to handle webwork is to tackle it with other friends so you can conserve the number of attempts you have! What type of course is this for?'''
	return output

def student_issue_homework_math(req):
	output = '''The Math Lab at East Hall has a lot of free student tutoring during the week! I would suggest that you hit them up from 11 to 4 and 7 to 10 on the week days for homework help.'''
	return output

def student_issue_homework_science(req):
	output = '''The chemistry building has something called the science learning center which has free tutoring sessions for Chemistry and Biology. It as a great resource to help out with your homework and understanding'''
	return output

def student_issue_homework_eecs(req):
	output = '''Computer science coursework can definitely be challenging, but there are many helpful intructor aids holding office hours that are a great resource'''
	return output

def student_issue_unknown(req):
	output = '''I'm not familiar with that type of work, but I will say that sometimes the best thing we can do if we are facing a lot of stress is to take a break and walk around.'''
	return output