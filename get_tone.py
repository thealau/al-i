import json
from watson_developer_cloud import ToneAnalyzerV3



# create client

def get_tone(text):
    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        iam_apikey='Lp6lyTak20TWGCNTXyG2pAbzBPNLV5dERhclC439s3f9',
        url='https://gateway.watsonplatform.net/tone-analyzer/api'
        
    )

    tone_analysis = tone_analyzer.tone(
        {'text': text},
        'application/json',
        False
    ).get_result()

    if len(tone_analysis['document_tone']['tones']) == 0:
        print('neutral')
    else:
        print(tone_analysis['document_tone']['tones'])

    return

text = 'I am not sure what to do'
get_tone(text)