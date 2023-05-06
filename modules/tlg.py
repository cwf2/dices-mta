'''Ancillary code for working with TLG results'''

from dicesapi import Speech, Work
import re


loc_patterns = [re.compile(pat) for pat in [
    r'Book (\d+) line (\d+)',            # book.line
    r'Book (\d+) \w+ (\d+) line (\d+)',  # book.poem.line
    r'\w+ (\d+) line (\d+)',             # poem.line
    r'Line (\d+)',                       # line
]]

def getTLG(work):
    '''extract the TLG identifier from DICES work record'''
    
    if isinstance(work, Speech):
        work = work.work
    
    if hasattr(work, '_attributes'):
        tlg = work._attributes.get('tlg', '')
        
        if tlg is not None and tlg != '':
            tlg = tlg.replace('_', '.')
            return tlg
        
        
def extractLoc(string):
    '''Try to generate locus in DICES format'''
    
    for pat in loc_patterns:
        m = pat.match(string)
        if m:
            return '.'.join(m.groups())
        
        
def lineIsInSpeech(line, speech):
    '''True if line is within the bounds of speech'''
    target_units = [unit.strip() for unit in line.split('.')]
    left_units = [unit.strip() for unit in speech.l_fi.split('.')]
    right_units = [unit.strip() for unit in speech.l_la.split('.')]
    
    if not len(target_units) == len(left_units) == len(right_units):
        print(f"Can't parse loci: {line}, {speech.l_fi}-{speech.l_la}")
        return None
    
    for target, left, right in zip(target_units, left_units, right_units):
        if left != right:
            if re.search(r'\D+\d', left) or re.search(r'\D+\d', right):
                print(f'Non-numeric bounds: {left}, {right}')
            elif re.search('\D+\d', target):
                print(f'Non-numeric target: {target}')
        if not (compareLocUnits(left, target) and compareLocUnits(target, right)):
            return False
    
    return True


def lineIsSpeechIntro(line, speech, window=1):
    '''True if line is within window of speech first line'''
    
    target_units = [unit.strip() for unit in line.rsplit('.')]
    left_units = [unit.strip() for unit in speech.l_fi.rsplit('.')]
    
    if target_units[0] != left_units[0]:
        return False
    
    target = target_units[1]
    left = left_units[1]
    
    if re.search(r'\D', target) or re.search(r'\D', left):
        print(f'Non-numeric line comparison {target}, {left}:', end=' ')
        if re.fullmatch(r'\d+\D*', target) and re.fullmatch(r'\d+\D*', left):
            target = re.sub('\D*$', '', target)
            left = re.sub('\D*$', '', left)
            print(f'comparing {target} {left}')
        else:
            print(f'skipping')
            return None
    
    target = int(target)
    left = int(left)
    
    success = 0 < (left - target) <= window
    
    return success


def compareLocUnits(left, right):
    '''True if left seems to come before right'''
    
    # nothing but numeric digits
    if not re.search(r'\D', left + right):
        return int(left) <= int(right)
    
    # no numeric digits at all
    if not re.search(r'\d', left + right):
        return left <= right
    
    # possible prefix, numeric part, possible suffix
    m_left = re.search(r'(\D*)(\d+)(\D*)', left)
    m_right = re.search(r'(\D*)(\d+)(\D*)', right)
    
    if not m_left and m_right:
        print(f"Can't compare {left} and {right}")
        return None
    
    pref_l, dig_l, suff_l = m_left.groups()
    pref_r, dig_r, suff_r = m_right.groups()
    
    dig_l = int(dig_l)
    dig_r = int(dig_r)
    
    return (pref_l, dig_l, suff_l) <= (pref_r, dig_r, suff_r)
    