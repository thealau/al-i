import json
from watson_developer_cloud import ToneAnalyzerV3

# Returns a sentiment: anger, disgust, fear, joy, sadness, neutral
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


    # Variables for extracting predicted tone
    mytones = tone_analysis['document_tone']['tones']
    highest = 0
    predict = 'neutral'
    valid = ['anger', 'fear', 'joy', 'sadness']

    #  Go through all identified tones
    for tone in mytones:

        cur = tone['tone_id']
        score = tone['score']

        # only report the highest tone
        if cur in valid and score > highest:
            highest = score
            predict = cur

    return predict, highest


def get_complex_tone(text):
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

    mytones = tone_analysis['document_tone']['tones']

    analysis = {}
    
    for tone in mytones:
        analysis[tone['tone_id']] = tone['score']

    return analysis


