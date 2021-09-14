TRAITTYPES = {
    "0": "Strength",
    "1": "Agility",
    "2": "Intelligence",
    "8": "Strength Gain",
    "9": "Agility Gain",
    "a": "Intelligence Gain",
    "7": "Primary Attribute",

    "3": "Damage",
    "4": "Damage Type",
    "5": "Armor",
    "6": "Speed",
    "c": "Accuracy",


    "b": "Luck",
    "d": "Exp Gain",
    "e": "Mana Regen Rate",
    "f": "Batch",
}

#  If you pass in a value that's a number and you don't set a display_type, the trait will appear in the Rankings section (top right in the image above).
# Adding an optional max_value sets a ceiling for a numerical trait's possible values. It defaults to the maximum that OpenSea has seen so far on the assets on your contract. If you set a max_value, make sure not to pass in a higher value.

DISPLAYTYPES = [
    "date",
    "number",
    "boost_percentage",
    "boost_number",
]


def json_generate(tokenId, url):
    hexStr = f"0x{tokenId}"

    data = {
        "description": f"# Ultimate Stats NFT\nYour stats are: `{hexStr}`",
        "external_url": f"https://stattz.github.io/nft/{hexStr}",
        "name": hexStr,
        "image": f"{url}/image?tokenId={hexStr}",
        "background_color": "202b38"
    }

    attributes = []

    for i in range(len(tokenId)):
        c = tokenId[i]

        attributes.append({
            "trait_type": TRAITTYPES[c],
            "value": int(c, base=16),
        })

    data["attributes"] = attributes

    return data
