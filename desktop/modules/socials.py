from os import system

LINKS = {
    'youtube': 'https://www.youtube.com/@OnelCrack',
    'github': 'https://www.github.com/TechOGR',
    'instagram': 'https://www.instagram.com/onel_crack/',
    'facebook': 'https://www.facebook.com/profile.php?id=100092376152191',
    'twitter': 'https://x.com/Onel_Crack'
}


def open_link(name):
    if name in LINKS:
        system(f"start {LINKS[name]}")
