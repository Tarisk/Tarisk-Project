import pyautogui
from pygetwindow import PyGetWindowException
import time
import random
from positions import private_14

# To do
# 1. Create an simple version
# 2. Upgrade the version and consider delays


# Finds the Dofus window and resize it
def start():
    windows = pyautogui.getAllTitles()
    for win in windows:
        if WIN_NAME in win:
            win_dofus = pyautogui.getWindowsWithTitle(win)
            win_dofus[0].size = (1080, 1080)
            time.sleep(random.uniform(1, 1.5))
            return win_dofus[0]



def place(obj):
    for pos in POSITIONS:
        pyautogui.press("i")
        time.sleep(random.uniform(1, 1.5))
        pyautogui.click(INV_SEARCH)
        pyautogui.write(obj, interval=0.11)
        time.sleep(0.25)
        pyautogui.doubleClick(INVENTORY_SLOT)
        time.sleep(random.uniform(0.25, 0.5))
        pyautogui.click(x=pos[0] + win.left, y=pos[1] + win.top)
        time.sleep(random.uniform(0.5, 1))


def remove():
    x_off = (20, 40)
    y_off = (10, 16)
    for pos in reversed(POSITIONS):
        x = pos[0] + win.left
        y = pos[1] + win.top
        pyautogui.click(x=x, y=y)
        time.sleep(random.uniform(0.25, 0.5))
        pyautogui.click(x=x + random.randint(x_off[0], x_off[1]), y=y + random.randint(y_off[0], y_off[1]))
        time.sleep(random.uniform(0.5, 0.75))


def check_pos_inventory():
    inv = pyautogui.locateOnScreen("images/inventory.PNG", region=dofus_region, confidence=0.9)
    return (inv.left, inv.top) == (POS_INV[0], POS_INV[1]) or (inv.left, inv.top) == (POS_INV[0] - 1, POS_INV[1])


def set_pos_inventory():
    pyautogui.click(DOFUS_WIN)
    time.sleep(0.25)
    pyautogui.press("i")
    time.sleep(random.uniform(2, 3))
    in_place = check_pos_inventory()
    attempt = 0
    while in_place is False:
        inv = pyautogui.locateOnScreen("images/inventory.PNG", region=dofus_region, confidence=0.9)
        pyautogui.moveTo((inv.left - 100, inv.top))
        time.sleep(random.uniform(1, 1.25))
        pyautogui.dragTo(760 + win.left, 760 + win.top, button="left")

        time.sleep(1)

        if check_pos_inventory():
            pyautogui.press("i")
            time.sleep(1)
            in_place = True
        else:
            attempt += 1
            if attempt > 3:
                raise Exception("Was not able to move the inventory tab")
    else:
        print("In place")
        pyautogui.press("i")
        time.sleep(2)


def open_enclos():
    pyautogui.click(DOOR)
    time.sleep(5)


def close_enclos():
    pyautogui.press("esc")
    time.sleep(3)


def find_filter(image, region, search, reset=False):
    location = None
    pyautogui.click(search)
    time.sleep(1)
    if reset:
        for i in range(0, 5):
            pyautogui.scroll(150)
    for i in range(0, 5):
        location = pyautogui.locateOnScreen(f"images/{image}", region=region, confidence=0.85)
        if location is not None:
            time.sleep(2)
            return location
        pyautogui.scroll(-150)
        time.sleep(1)
    return location


def emote():
    pyautogui.press("5")
    time.sleep(random.uniform(3, 4))
    pyautogui.press("6")
    time.sleep(random.uniform(3, 4))


def transfert_etable_enclos():
    pyautogui.click(ETABLE_TRANSFERT_BUTTON)
    time.sleep(0.5)
    pyautogui.click(ETABLE_TRANSFERT_ENC)
    time.sleep(random.uniform(2, 3))


def transfert_enclos_inv():
    pyautogui.click(ENCLOS_TRANSFERT_BUTTON)
    time.sleep(0.5)
    pyautogui.click(ENCLOS_TRANSFERT_INV)
    time.sleep(random.uniform(2, 3))


def transfert_enclos_etable():
    pyautogui.click(ENCLOS_TRANSFERT_BUTTON)
    time.sleep(0.5)
    pyautogui.click(ENCLOS_TRANSFERT_ETABLE)
    time.sleep(random.uniform(2, 3))


def setup_maturite():
    obj = ""
    open_enclos()
    maturite = find_filter("bes_mat.PNG", ETABLE_REGION, ETABLE_SEARCH_1)
    if maturite is None:
        print("Besoin de maturite introuvable")
        return
    else:
        pyautogui.click(maturite)
        time.sleep(random.uniform(0.5, 1))

    pyautogui.click(ETABLE_ADD_SEARCH)
    time.sleep(random.uniform(0.5, 1))

    seren_pos = find_filter("seren_pos.PNG", ETABLE_REGION, ETABLE_SEARCH_2)
    if seren_pos is None:
        print("Serenite Positive Introuvable")

        pyautogui.click(ETABLE_SEARCH_2)
        seren_neg = find_filter("seren_neg.PNG", ETABLE_REGION, ETABLE_SEARCH_2)
        if seren_neg is None:
            print("Serenite Negative Introuvable")
        else:
            pyautogui.click(seren_neg)
            time.sleep(random.uniform(0.5, 1))
            close_enclos()
            obj = "caresseur"
            place(obj)
    else:
        pyautogui.click(seren_pos)
        time.sleep(random.uniform(0.5, 1))
        close_enclos()
        obj = "baffeur"
        place(obj)

    open_enclos()

    pyautogui.screenshot("filters.png", region=ETABLE_SEARCH_2_REGION)

    pyautogui.click(find_filter("seren_moy.PNG", ENCLOS_REGION, ENCLOS_SEARCH))
    time.sleep(1)

    transfert_etable_enclos()

    empty = False
    is_on = True
    count = 0
    while is_on:
        count += 1
        print(count)

        emote()

        if pyautogui.locateOnScreen(f"images/empty_enc.PNG", region=ENCLOS_REGION) is None:
            transfert_enclos_inv()
            if pyautogui.locateOnScreen("filters.png", region=ETABLE_SEARCH_2_REGION) is not None:
                transfert_etable_enclos()
            elif count % 30 == 0:
                pyautogui.click(find_filter("all.PNG", ENCLOS_REGION, ENCLOS_SEARCH, reset=True))
                time.sleep(1)
                if pyautogui.locateOnScreen(f"images/empty_enc.PNG", region=ENCLOS_REGION) is not None:
                    is_on = False
                    print("Finished")
                else:
                    pyautogui.click(find_filter("seren_moy.PNG", ENCLOS_REGION, ENCLOS_SEARCH))
                    time.sleep(1)
            else:
                empty = True

        if count % 100 == 0:
            pyautogui.click(find_filter("all.PNG", ENCLOS_REGION, ENCLOS_SEARCH, reset=True))
            time.sleep(1)
            transfert_enclos_etable()
            close_enclos()
            remove()
            place(obj)
            open_enclos()
            transfert_etable_enclos()
            pyautogui.click(find_filter("seren_moy.PNG", ENCLOS_REGION, ENCLOS_SEARCH))
            time.sleep(1)

        if count % 75 == 0:
            pyautogui.click(find_filter("exhausted.PNG", ENCLOS_REGION, ENCLOS_SEARCH))
            time.sleep(1)
            if pyautogui.locateOnScreen(f"images/empty_enc.PNG", region=ENCLOS_REGION) is None:
                transfert_enclos_inv()
            pyautogui.click(find_filter("seren_moy.PNG", ENCLOS_REGION, ENCLOS_SEARCH, reset=True))
            time.sleep(1)
            if empty is False:
                transfert_etable_enclos()


WIN_NAME = input("Nom du Personnage: ")

print("Avant de commencer, assurer vous de completer les etapes suivantes:")
print("1. Etre dans la section consommable dans votre inventaire")
print("2. Avoir l'emote pour repousser sur le raccourci '5' et celui pour attirer sur '6'")
print("3. Avoir aucun filtre dans l'enclos et etable")

ready = input("Entrer 'y' quand vous etes pret: ")

win = start()
time.sleep(2)
dofus_region = (win.left, win.top, win.width, win.height)
DOFUS_WIN = (300 + win.left, 10 + win.top)

# Pos Enclos Exterieur
POSITIONS = list(private_14.values())
DOOR = (397 + win.left, 588 + win.top)

# Pos inventaire
INVENTORY_SLOT = (805 + win.left, 415 + win.top)
POS_INV = (645 + win.left, 302 + win.top)
INV_SEARCH = (900 + win.left, 910 + win.top)

# Pos Etable
ETABLE_REGION = (46 + win.left, 168 + win.top, 343, 385)
ETABLE_SEARCH_2_REGION = (103 + win.left, 204 + win.top, 227, 55)
ETABLE_SEARCH_1 = (295 + win.left, 218 + win.top)
ETABLE_SEARCH_2 = (295 + win.left, 248 + win.top)
ETABLE_SEARCH_3 = (295 + win.left, 278 + win.top)
ETABLE_ADD_SEARCH = (66 + win.left, 216 + win.top)
ETABLE_TRANSFERT_BUTTON = (367 + win.left, 217 + win.top)
ETABLE_TRANSFERT_ENC = (415 + win.left, 229 + win.top)

# Pos Enclos Interieur
ENCLOS_REGION = (46 + win.left, 571 + win.top, 343, 265)
ENCLOS_SEARCH = (295 + win.left, 618 + win.top)
ENCLOS_TRANSFERT_BUTTON = (367 + win.left, 620 + win.top)
ENCLOS_TRANSFERT_INV = (415 + win.left, 653 + win.top)
ENCLOS_TRANSFERT_ETABLE = (415 + win.left, 632 + win.top)


# pyautogui.screenshot("test.png", region=dofus_region)

set_pos_inventory()

setup_maturite()
