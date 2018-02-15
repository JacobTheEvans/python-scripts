import requests
import json
import random

base_api_url = "https://api.deckbrew.com/mtg/cards"


def get_cards(color, card_format):
    cards = []
    page = 0
    while True:
        req_url = base_api_url + "?"
        req_url += "&page=%s" % page
        req_url += "&color=%s" % color
        req_url += "&format=%s" % card_format
        req = requests.get(req_url)
        if req.status_code != 200:
            print("[-] Error API failed")
            break
        if len(json.loads(req.text)) != 0:
            cards += json.loads(req.text)
            page += 1
        else:
            break
    return cards


def get_land_cards(color):
        cards = []
        page = 0
        while True:
            req_url = base_api_url + "?"
            req_url += "&page=%s" % page
            req_url += "&type=land"
            req = requests.get(req_url)
            if req.status_code != 200:
                print("[-] Error API failed")
            if len(json.loads(req.text)) != 0:
                cards_copy = json.loads(req.text)
                for card in cards_copy:
                    if ("{%s}" % color[0].upper()) in card["text"]:
                        cards.append(card)
                page += 1
            else:
                break
        return cards


def gen_land(limit, cards):
    result = []
    while len(result) < limit:
        for card in cards:
            if "land" in card["types"] and not ("tapped" in card["text"]):
                result.append(card)
                break
        random.shuffle(cards)
    return result


def gen_mana_curve(already_used, limit):
    curve = {}
    amount_in_deck = already_used

    #gen amount for 2 drops
    amount = random.randint(7, 10)
    amount_in_deck += amount
    curve["2"] = amount

    #gen amount for 3 drops
    amount = random.randint(6, 8)
    amount_in_deck += amount
    curve["3"] = amount

    #gen amount for 4 drops
    amount = random.randint(3, 4)
    amount_in_deck += amount
    curve["4"] = amount

    #gen amount for 5 drops
    amount = 3
    amount_in_deck += 3
    curve["5"] = 2

    #if to many cards remove 4 drops until limit is reached
    while amount_in_deck > limit:
        curve["4"] -= 1
        amount_in_deck -= 1

    #if to little cards in deck add higher cost until limit is reached
    while amount_in_deck < limit:
        try:
            curve["6"]
        except:
            curve["6"] = 0

        curve["6"] += 1
        amount_in_deck += 1

    return curve

def gen_main_deck(cards, curve):
    result = []
    for sect in curve:
        amount = 0
        while amount < curve[sect]:
            for card in cards:
                if(card["cmc"] == int(sect) and len(card["colors"]) == 1):
                    result.append(card)
                    amount += 1
                    break
            random.shuffle(cards)
    return result


def main():
    deck = []
    print("[+] Starting magic deck building bot")
    print("[+] Generating random color for deck...")
    print("[*] Please input color")
    color = raw_input(">> ")
    print("[+] Success color is %s" % color)
    print("[*] Please input format")
    card_format = raw_input(">> ")
    print("[+] Gathering land cards to power deck")
    land_cards = get_land_cards(color)
    print("[+] Success %s land cards were loaded in" % str(len(land_cards)))
    print("[+] Generating random land limit")
    land_limit = random.randint(17, 21)
    print("[+] Land limit is %s" % str(land_limit))
    print("[+] Selecting land for deck")
    deck = deck + gen_land(land_limit, land_cards)
    print("[+] Success land added to deck")
    print("[+] Gathering non land cards to generate deck")
    cards = get_cards(color, card_format)
    print("[+] Success %s cards were loaded in" % str(len(cards)))
    print("[+] Generating mana curve")
    curve = gen_mana_curve(len(deck), 40 + 1)
    print("[+] Success mana curve is ")
    print(curve)
    print("[+] Selecting non land cards for deck")
    deck = deck + gen_main_deck(cards, curve)
    print("[+] Success non land cards added to deck")
    print("[+] Deck size is %s" %  str(len(deck)))
    print("[+] Writing file as JSON to deck.json")
    f = open("deck.json","w")
    f.write(json.dumps(deck))
    f.close()
    print("[+] Success and may you draw well")


if __name__ == "__main__":
    main()
