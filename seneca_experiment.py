'''seneca_experiment
   
   Ancillary code to make the Seneca passages easier to work with. 
'''
from dicesapi.text import Passage
import re

tagtype = {
    # add special tag for seneca speeches
    'trag': 'tragedy',
    
    # rest are copy-pasted from DICES backend
    'cha': 'Challenge',
    'com': 'Command',
    'con': 'Consolation',
    'del': 'Deliberation',
    'des': 'Desire and Wish',
    'exh': 'Exhortation and Self-Exhortation',
    'far': 'Farewell',
    'gre': 'Greeting and Reception',
    'inf': 'Information and Description',
    'inv': 'Invitation',
    'ins': 'Instruction',
    'lam': 'Lament',
    'lau': 'Praise and Laudation',
    'mes': 'Message',
    'nar': 'Narration',
    'ora': 'Prophecy: Oracular Speech: and Interpretation',
    'per': 'Persuasion',
    'pra': 'Prayer',
    'que': 'Question',
    'req': 'Request',
    'res': 'Reply to Question',
    'tau': 'Taunt',
    'thr': 'Threat',
    'vit': 'Vituperation',
    'vow': 'Promise and Oath',
    'war': 'Warning',
    'und': 'Undefined',
}

def getTags(speech):
    '''extract tag data from DICES records'''
    
    tags = []
    
    if 'tags' in speech._attributes:
        for t in speech._attributes['tags']:
            if t['type'] not in tags:
                tags.append(t['type'])
    
    return tags
                
def buildLineArray(text):
    '''Turn a block of text into a DICES-style line array'''

    # initial line no
    n = '1'

    linearray = []

    for l in text.splitlines():
        m = re.search(r'\s+(\d+)\s*$', l) 
        if m is None:
            n = str(int(n)+1)
        else:
            n = m.group(1)

        l = l.strip()

        if l != '':    
            linearray.append(dict(
                n = n,
                text = l.strip(),
            ))

    return linearray


def buildFeatures(speech, featureset, normalize=True):
    '''extract feature set from a speech'''
    wc = Counter()
    total = 1
    if speech.passage is not None and speech.passage.cltk is not None:
        wc.update([w.lemma for w in speech.passage.cltk])
        if normalize:
            total = sum(wc.values())
    vector = dict()
    for feat in featureset:
        vector[feat] = wc.get(feat, 0) / total
        
    return vector


class SenecaSpeech(object):
    '''A pseudo-speech object to hold senecan passages
    
       This custom class that mimics the DICES `Speech` class,
       at least in some basic ways. This lets me use the same 
       feature extraction methods on both Seneca and the DICES data.
    '''
    
    def __init__(self, text=None, id=None):
        self.passage = None
        self.spkr = None
        self.lang = 'latin'
        self.id = None
        
        if text is not None:
            text = text.strip()

            if text != '':
                m = re.match(r'\s*\[(.+)\]', text)

                if m is not None:
                    self.spkr = m.group(1)
                    text = re.sub(r'^\s*\[(.+)\]', '', text)
                    text = re.sub(r'\d+\s*$', '', text)

                self.passage = Passage()
                self.passage.line_array = buildLineArray(text)
                self.passage.text = ' '.join(l['text'] for l in self.passage.line_array)
                self.passage.speech = self

                self.l_fi = self.passage.line_array[0]['n']
                self.l_la = self.passage.line_array[-1]['n']
                
                self.tags = ['sen']
        
        if id is not None:
            self.id = id
            
    def __repr__(self):
        if self.id is not None:
            id = f' {self.id}'
        else:
            id = ''
        
        return f'<SenecaSpeech{id}: {self.spkr} ({self.l_fi}-{self.l_la})>'