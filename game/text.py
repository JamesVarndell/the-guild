
def sanitise(string):
    words = string.split(' ')
    
    for i, word in enumerate(words):
        if word in ('a', 'an'):
            if any(words[i+1].startswith(vowel) for vowel in 'aeiou'):
                words[i] = 'an'
            else:
                words[i] = 'a'
    
    return ' '.join(words)