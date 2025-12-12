import random

def skapa_kortlek():
    kort_värden = [2, 3, 4, 5 , 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    random.shuffle(kort_värden)
    return kort_värden

def beräkna_poäng(hand):
    temp_hand = hand[:]
    summa = sum(temp_hand)
    while summa > 21 and 11 in temp_hand:
        temp_hand[temp_hand.index(11)]= 1
        summa = sum(temp_hand)
    return summa

def spelarens_tur (kortlek, spelarens_hand, spelarnummer):
    print(f"\n--- Spelare{spelarnummer}s tur")
    while True:
        poäng = beräkna_poäng(spelarens_hand)
        print(f"Dina kort: {spelarens_hand}(totalt: {poäng}")

        if poäng == 21:
            print(f"Blackjack!{spelarnummer} fick blackjack!")
            break
        elif poäng > 21:
            print(f"Tjock! {spelarnummer} är tjock")
            break
        val = input("Vill du dra ett til kort ('hit') eller ('stanna')? [h/s]").lower()

        if val =='h':
            if not kortlek:
                print("Kortleken e slut")
                break
            nytt_kort = kortlek.pop(0)
            spelarens_hand.append(nytt_kort)
            print(f"Du drog ett kort: {nytt_kort}")
        elif val == 's':
            print(f"Spelare{spelarnummer} stannar med poäng: {poäng}")
            break   
        else:
            print("Ogiltigt val. Vänligen välj 'h' eller 's'.")
        
    return beräkna_poäng(spelarens_hand)

def jämför_resultat(spelare_1_poäng, spelare_2_poäng, namn1, namn2):
    spelare_1_TJOCK = spelare_1_poäng > 21
    spelare_2_TJOCK = spelare_2_poäng > 21

    if spelare_1_TJOCK and spelare_2_TJOCK:
        print(f"Båda spelarna är tjocka! Oavgjort!")
        return
    
    elif spelare_1_TJOCK:
        print(f"{namn1} är tjock! {namn2} vinner!")
        return
    elif spelare_2_TJOCK:
        print(f"{namn2} är tjock! {namn1} vinner!")
        return
    elif spelare_1_poäng > spelare_2_poäng:
        print(f"{namn1} vinner!")
        
    elif spelare_2_poäng > spelare_1_poäng:
        print(f"{namn2} vinner!")
        
    else:
        print("Oavgjort!")


def starta_spelet():
    print("Enkel blackjack")
    namn1 = input("Namn för spelare 1")
    namn2 = input("Namn för spelare 2")
    runda = 1
    while True: 
        print(f"\n === Runda {runda}===")

        kortlek = skapa_kortlek()

        spelare1_hand = [kortlek.pop(0), kortlek.pop(0)]
        spelare2_hand = [kortlek.pop(0), kortlek.pop(0)]

        spelare1_resultat = spelarens_tur(kortlek, spelare1_hand, namn1)
        spelare2_resultat = spelarens_tur(kortlek, spelare2_hand, namn2)

        print("\n--- Resultat ---")
        print(f"{namn1}s kort: {spelare1_hand} (totalt: {spelare1_resultat})")
        print(f"{namn2}s kort: {spelare2_hand} (totalt: {spelare2_resultat})")
        print("========")
        
        jämför_resultat(spelare1_resultat, spelare2_resultat, namn1, namn2)

        spela_igen = input("Vill ni spela igen? (j/n): ").lower()
        if spela_igen != 'j':
            print("Tack för att ni spelade!")
            break
        runda += 1  

starta_spelet()
