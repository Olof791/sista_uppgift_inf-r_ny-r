import random

#
KORT_VARDEN = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    '10': 10, 'Joker': 10, 'Drottning': 10, 'Kung': 10, 'Ess': 11
}
KORT = list(KORT_VARDEN.keys())

def skapa_kortlek():
    kortlek = KORT * 4
    random.shuffle(kortlek)
    return kortlek


def beräkna_poäng(hand):
    poäng = 0
    
    for kort in hand:
        poäng += KORT_VARDEN[kort]
    return poäng

def spela_blackjack_enkel():
    pengar = 1000
    
    # HUVUDLOOP
    while pengar > 0:
        print(f"\n--- Ny Hand --- (Pengar: {pengar} kr)")
        
        try:
            insats = int(input("Hur mycket vill du satsa? "))
        except ValueError:
            print("Ogiltig insats.")
            continue
        
        if insats > pengar or insats <= 0:
            print("Ogiltig satsning.")
            continue

        kortlek = skapa_kortlek()
        spelare_hand = [kortlek.pop(), kortlek.pop()]
        dealer_hand = [kortlek.pop(), kortlek.pop()]
        vinnare = None
        
       
        while True:
            sp_poang = beräkna_poäng(spelare_hand)
            dealerns_synliga_kort = dealer_hand[0]
            
            print(f"Din hand: {spelare_hand} (Poäng: {sp_poang})")
            print(f"Dealerns synliga kort: [{dealerns_synliga_kort}]")
            
            if sp_poang > 21:
                print("Du blev Tjock! (Bust)")
                vinnare = "DEALER"
                break
            
            val = input("Vill du 'hit' (ta kort) eller 'stand' (stanna)? ").lower()
            if val == 'hit':
                spelare_hand.append(kortlek.pop())
            elif val == 'stand':
                break
            else:
                print("Ogiltigt val.") 

        
        if vinnare is None:
            print(f"\nDealerns dolda kort var: {dealer_hand[1]}")
            
           
            while beräkna_poäng(dealer_hand) < 17:
                print("Dealern tar kort...")
                dealer_hand.append(kortlek.pop())
                
                
                if beräkna_poäng(dealer_hand) > 21:
                    print(f"Dealerns hand: {dealer_hand} (Poäng: {beräkna_poäng(dealer_hand)})")
                    print("Dealern blev Tjock! (Bust)")
                    vinnare = "SPELARE"
                    break

        
        if vinnare is None:
            sp_poang = beräkna_poäng(spelare_hand)
            dl_poang = beräkna_poäng(dealer_hand)
            print(f"Dealerns sluthand: {dealer_hand} (Poäng: {dl_poang})")

            
            if sp_poang > dl_poang:
                vinnare = "SPELARE"
            elif dl_poang > sp_poang:
                vinnare = "DEALER"
            else:
                vinnare = "PUSH"

        # Utbetalning
        if vinnare == "SPELARE":
            pengar += insats
            print(f"*** SPELAREN VANN! Du vinner {insats} kr. ***")
        elif vinnare == "DEALER":
            pengar -= insats
            print(f"*** DEALERN VANN. Du förlorar {insats} kr. ***")
        elif vinnare == "PUSH":
            print("*** PUSH (Oavgjort). Pengarna tillbaka. ***")

    print("\n--- GAME OVER ---")
    print("Dina pengar är slut!")

if __name__ == "__main__":
    spela_blackjack_enkel()