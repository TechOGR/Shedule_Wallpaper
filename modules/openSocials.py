from os import system

LINKS = {
    'youtube': 'https://www.youtube.com/@OnelCrack',
    'github': 'https://www.github.com/TechOGR',
    'instagram': 'https://www.instagram.com/onel_crack/',
    'facebook': 'https://www.facebook.com/profile.php?id=100092376152191',
    'twitter': 'https://x.com/Onel_Crack'
}

def startLinks(name):
    system(f"start {LINKS[name]}")

def openLinks(name):
    print(name)
    if name == 'youtube':
        startLinks(name)
    elif name == 'twitter':
        startLinks(name)
    elif name == 'instagram':
        startLinks(name)
    elif name == 'facebook':
        startLinks(name)
    elif name == 'github':
        startLinks(name)