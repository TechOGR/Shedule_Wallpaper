from subprocess import Popen

LINKS = {
    'youtube': 'https://www.youtube.com/@OnelCrack'
}

def openLinks(name):
    
    if name == 'youtube':
        Popen([LINKS[name]])