import numpy as np
from sqlmodel import Session

from app.models import Mission
from app.services.missions import create_mission

items = [
    "sword",
    "amulet",
    "ring",
    "necklace",
    "relic",
    "artifact",
    "scroll",
    "chalice",
    "staff",
    "orb",
    "tome",
    "crown",
    "gauntlet",
    "mask",
    "blade",
    "crystal",
    "dagger",
    "shield",
    "lance",
    "grimoire",
    "sigil",
    "pendant",
    "helm",
    "bracer",
    "phoenix feather",
    "dragon scale",
]

item_actions = [
    "Find",
    "Destroy",
    "Recover",
    "Protect",
    "Retrieve",
    "Steal",
    "Unlock",
    "Uncover",
    "Repair",
    "Seal",
    "Restore",
    "Bury",
    "Enchant",
    "Forge",
    "Purify",
    "Corrupt",
    "Empower",
    "Offer",
]

item_adjectives = [
    "lost",
    "ancient",
    "enchanted",
    "mystical",
    "cursed",
    "stolen",
    "hidden",
    "forbidden",
    "forgotten",
    "sacred",
    "legendary",
    "mythical",
    "arcane",
    "divine",
    "damned",
    "haunted",
    "shattered",
    "burned",
    "blessed",
    "accursed",
    "desecrated",
    "twilight-forged",
    "eldritch",
]

enemies = [
    "bandit",
    "dragon",
    "goblin",
    "sorcerer",
    "troll",
    "witch",
    "demon",
    "zombie",
    "warlock",
    "vampire",
    "necromancer",
    "werewolf",
    "lich",
    "gargoyle",
    "dark knight",
    "shadow fiend",
    "wraith",
    "chimera",
    "kraken",
    "beholder",
    "djinn",
    "harbinger",
    "fallen paladin",
    "bone golem",
]

enemy_actions = [
    "Defeat",
    "Slay",
    "Banish",
    "Destroy",
    "Overcome",
    "Exorcise",
    "Eradicate",
    "Annihilate",
    "Eliminate",
    "Subdue",
    "Seal Away",
    "Break the Curse of",
    "Trap",
    "Hunt",
    "Cleanse",
    "Decipher",
    "Challenge",
    "Outwit",
]

enemy_adjectives = [
    "dark",
    "evil",
    "mysterious",
    "powerful",
    "enchanted",
    "cursed",
    "ancient",
    "forbidden",
    "demonic",
    "shadowy",
    "twisted",
    "malevolent",
    "undead",
    "chaotic",
    "sinister",
    "accursed",
    "plague-ridden",
    "fallen",
    "vile",
    "unholy",
    "spectral",
    "hellbound",
]

locations = [
    "forest",
    "cave",
    "castle",
    "temple",
    "mountain",
    "village",
    "swamp",
    "dungeon",
    "crypt",
    "catacomb",
    "ruins",
    "fortress",
    "tower",
    "island",
    "underworld",
    "graveyard",
    "desert",
    "labyrinth",
    "volcano",
    "oasis",
    "floating city",
    "dimensional rift",
    "lost kingdom",
]

location_actions = [
    "Explore",
    "Enter",
    "Investigate",
    "Search",
    "Scout",
    "Traverse",
    "Descend Into",
    "Break Into",
    "Unveil",
    "Conquer",
    "Cleanse",
    "Defile",
    "Navigate",
    "Survive",
    "Reclaim",
    "Chart",
    "Escape",
    "Unravel",
]

location_adjective = [
    "mysterious",
    "dangerous",
    "enchanted",
    "cursed",
    "abandoned",
    "haunted",
    "forbidden",
    "hidden",
    "desolate",
    "forgotten",
    "ruined",
    "desecrated",
    "shadowy",
    "twisted",
    "sacred",
    "corrupted",
    "blighted",
    "sealed",
    "floating",
    "eternal",
    "void-touched",
    "illusionary",
]

fractions = [
    "Brotherhood of Shadows",
    "Order of the Phoenix",
    "Crimson Legion",
    "Silver Hand",
    "Emerald Druids",
    "The Arcane Council",
    "The Black Sun",
    "The Forgotten Ones",
    "The Hollow Knights",
    "The Burning Fangs",
    "The Serpent Cult",
    "The Revenant Order",
    "The Veiled Watchers",
]

names = []

with open("../data/raw/names.txt") as file:
    names = file.read().splitlines()

person_actions = [
    "Befriend",
    "Betray",
    "Spy on",
    "Rescue",
    "Convince",
    "Challenge",
    "Train under",
    "Swear allegiance to",
    "Break free from",
    "Negotiate with",
    "Steal from",
    "Expose the lies of",
    "Compete against",
    "Hunt down",
    "Investigate",
    "Seek revenge on",
    "Forge an alliance with",
    "Recruit",
    "Interrogate",
    "Assist",
    "Track down",
    "Outwit",
    "Deceive",
    "Swindle",
]

after_actions = [
    "to change the fate of the kingdom",
    "to unlock a hidden power",
    "to prevent a war",
    "to gain their loyalty",
    "to uncover a dark secret",
    "to reclaim your lost honor",
    "to prove your worth",
    "to set things right",
    "to break an ancient curse",
    "to fulfill an old prophecy",
    "to obtain forbidden knowledge",
    "to seek redemption",
    "to ascend to a higher power",
    "to gain a powerful ally",
    "to restore balance to the world",
    "to protect the innocent",
    "to prepare for the final battle",
    "to overthrow a tyrant",
    "to uncover a hidden conspiracy",
    "to rewrite history",
]


# ======================
#   Mission patterns
# ======================

# item, item_action, item_adjective
# enemy, enemy_action, enemy_adjective
# location, location_action, location_adjective,
# names, fractions, person_actions, after_action?


patterns = [
    "{item_action} the {name}'s {item}",
    "{item_action} the {item_adjective} {item}",
    "{item_action} the {fraction}'s {item}",
    "{item_action} the {item_adjective} {item} at {location_adjective} {location}",
    "{item_action} the {name}'s {item} at {location_adjective} {location}",
    "{item_action} the {fraction}'s {item} at {location_adjective} {location}",
    "{enemy_action} the {enemy_adjective} {enemy}",
    "{enemy_action} the {enemy_adjective} {enemy} at {location_adjective} {location}",
    "{enemy_action} the {enemy_adjective} {enemy} at {location_adjective} {location} {after action}",
    "{enemy_action} the {enemy_adjective} {enemy} with {name}",
    "{enemy_action} the {enemy_adjective} {enemy} with {name} at {location_adjective} {location}",
    "{enemy_action} the {enemy_adjective} {enemy} with {name} at {location_adjective} {location} {after action}",
    "{enemy_action} the {enemy_adjective} {enemy} with {fraction}",
    "{enemy_action} the {enemy_adjective} {enemy} with {fraction} at {location_adjective} {location}",
    "{enemy_action} the {enemy_adjective} {enemy} with {fraction} at {location_adjective} {location} {after action}",
    "{location_action} the {location_adjective} {location}",
    "{location_action} the {location_adjective} {location} with {name}",
    "{location_action} the {location_adjective} {location} with {fraction}",
    "{person_action} {name} at {location_adjective} {location}",
    "{person_action} {fraction} at {location_adjective} {location}"
    "{person_action} {name} with {fraction} at {location_adjective} {location}",
    "{person_action} {fraction} with {name} at {location_adjective} {location}",
]


def generate_random_mission(session: Session) -> Mission:
    import random

    pattern = random.choice(patterns)
    mission = pattern.format(
        item=random.choice(items),
        item_action=random.choice(item_actions),
        item_adjective=random.choice(item_adjectives),
        location=random.choice(locations),
        location_action=random.choice(location_actions),
        location_adjective=random.choice(location_adjective),
        name=random.choice(names),
        fraction=random.choice(fractions),
        enemy=random.choice(enemies),
        enemy_action=random.choice(enemy_actions),
        enemy_adjective=random.choice(enemy_adjectives),
        after_action=random.choice(after_actions),
    )

    min_champions = max(sum([1 for i in pattern if i == "{"]) - 2, 1)
    max_champions = np.random.randint(min_champions, min_champions * 4)
    duration = int(max_champions**1.618)
    mu = 75
    sigma = 100
    power = 0
    for _ in range(min_champions):
        power += int(abs(np.random.normal(mu, sigma)))

    return create_mission(
        session,
        description=mission,
        level=power,
        total_duration=duration,
        min_champions=min_champions,
        max_champions=max_champions,
    )
