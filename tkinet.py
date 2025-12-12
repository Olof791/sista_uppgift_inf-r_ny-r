import tkinter as tk
from tkinter import ttk
import random

# --- 1. Data och Huvudlogik (Den Enkla Versionen) ---

# Ess ('A') har fast värde 11.
KORT_VARDEN = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}
KORT = list(KORT_VARDEN.keys())

def skapa_kortlek():
    kortlek = KORT * 4
    random.shuffle(kortlek)
    return kortlek

# Enkel poängberäkning (Ess = 11 fast värde)
def beräkna_poäng(hand):
    poäng = 0
    # Enkel FOR-LOOP för att summera värdena
    for kort in hand:
        poäng += KORT_VARDEN[kort]
    return poäng

# --- 2. Spelklassen (Tkinter GUI och Händelsehantering) ---

class BlackjackApp:
    def __init__(self, master):
        self.master = master
        master.title("Tkinter Blackjack Simulator")
        
        self.pengar = 1000
        self.insats = 0
        self.kortlek = []
        self.spelare_hand = []
        self.dealer_hand = []
        
        self.skapa_widgets()
        self.starta_ny_hand()

    def skapa_widgets(self):
        # Använd grid för enkel layout
        
        # Pengar/Insats Visning
        self.pengar_etikett = ttk.Label(self.master, text=f"Pengar: {self.pengar} kr")
        self.pengar_etikett.grid(row=0, column=0, columnspan=3, pady=10)

        self.insats_etikett = ttk.Label(self.master, text="Insats:")
        self.insats_etikett.grid(row=1, column=0, padx=5, sticky='w')

        self.insats_ruta = ttk.Entry(self.master)
        self.insats_ruta.grid(row=1, column=1, padx=5)
        
        self.insats_knapp = ttk.Button(self.master, text="Satsa", command=self.placera_insats)
        self.insats_knapp.grid(row=1, column=2, padx=5)

        # Hand-visningar
        self.dealer_hand_etikett = ttk.Label(self.master, text="Dealer: [?]")
        self.dealer_hand_etikett.grid(row=2, column=0, columnspan=3, pady=5)
        
        self.spelare_hand_etikett = ttk.Label(self.master, text="Spelare: []")
        self.spelare_hand_etikett.grid(row=3, column=0, columnspan=3, pady=5)
        
        # Resultat/Status
        self.status_etikett = ttk.Label(self.master, text="Välkommen till Blackjack!")
        self.status_etikett.grid(row=4, column=0, columnspan=3, pady=10)

        # Spelknappar
        self.hit_knapp = ttk.Button(self.master, text="Hit", command=self.hit)
        self.hit_knapp.grid(row=5, column=0, padx=5, pady=10)
        self.hit_knapp["state"] = "disabled"

        self.stand_knapp = ttk.Button(self.master, text="Stand", command=self.stand)
        self.stand_knapp.grid(row=5, column=1, padx=5, pady=10)
        self.stand_knapp["state"] = "disabled"

        self.ny_hand_knapp = ttk.Button(self.master, text="Ny Hand", command=self.starta_ny_hand)
        self.ny_hand_knapp.grid(row=5, column=2, padx=5, pady=10)
        self.ny_hand_knapp["state"] = "disabled"

    def uppdatera_gui(self, dölj_dealer_kort=True):
        sp_poang = beräkna_poäng(self.spelare_hand)
        dl_poang = beräkna_poäng(self.dealer_hand)
        
        self.pengar_etikett.config(text=f"Pengar: {self.pengar} kr (Insats: {self.insats} kr)")

        if dölj_dealer_kort and self.dealer_hand and len(self.dealer_hand) > 1:
            # Visa bara dealerns första kort i början av handen
            dealer_text = f"Dealer: [{self.dealer_hand[0]}, ?]"
        else:
            dealer_text = f"Dealer: {self.dealer_hand} (Poäng: {dl_poang})"

        self.dealer_hand_etikett.config(text=dealer_text)
        self.spelare_hand_etikett.config(text=f"Spelare: {self.spelare_hand} (Poäng: {sp_poang})")

    def starta_ny_hand(self):
        if self.pengar <= 0:
             self.status_etikett.config(text="GAME OVER! Du är pank.")
             return

        self.insats = 0
        self.spelare_hand = []
        self.dealer_hand = []
        self.status_etikett.config(text="Ange insats för nästa hand.")
        
        # Återställ knappar för satsning
        self.insats_knapp["state"] = "normal"
        self.insats_ruta["state"] = "normal"
        self.hit_knapp["state"] = "disabled"
        self.stand_knapp["state"] = "disabled"
        self.ny_hand_knapp["state"] = "disabled"
        self.uppdatera_gui()

    def placera_insats(self):
        try:
            insats = int(self.insats_ruta.get())
            if insats <= 0 or insats > self.pengar:
                self.status_etikett.config(text="Ogiltig insats!")
                return
            
            self.insats = insats
            self.status_etikett.config(text="Insats placerad. Välj Hit eller Stand.")
            
            # Förbered kort och händer
            self.kortlek = skapa_kortlek()
            self.spelare_hand = [self.kortlek.pop(), self.kortlek.pop()]
            self.dealer_hand = [self.kortlek.pop(), self.kortlek.pop()]
            
            # Aktivera spelknappar, inaktivera insats
            self.insats_knapp["state"] = "disabled"
            self.insats_ruta["state"] = "disabled"
            self.hit_knapp["state"] = "normal"
            self.stand_knapp["state"] = "normal"
            
            self.uppdatera_gui()

        except ValueError:
            self.status_etikett.config(text="Ange ett heltal som insats.")

    # --- Spelarens Händelser (Händelsedriven Loop-ersättning) ---

    def hit(self):
        self.spelare_hand.append(self.kortlek.pop())
        self.uppdatera_gui()
        
        sp_poang = beräkna_poäng(self.spelare_hand)

        # VILLKOR: Bust check
        if sp_poang > 21:
            self.status_etikett.config(text="Bust! Dealern vinner.")
            self.avsluta_hand("DEALER")

    def stand(self):
        self.hit_knapp["state"] = "disabled"
        self.stand_knapp["state"] = "disabled"
        self.status_etikett.config(text="Spelare stannade. Dealers tur...")
        self.dealer_tur() # Starta dealerns logik

    # --- Dealerns Logik ---

    def dealer_tur(self):
        # Dealerns loop/regel: Dra tills poängen är minst 17
        while beräkna_poäng(self.dealer_hand) < 17:
            self.dealer_hand.append(self.kortlek.pop())

        # Jämförelse och utbetalning
        sp_poang = beräkna_poäng(self.spelare_hand)
        dl_poang = beräkna_poäng(self.dealer_hand)
        
        self.uppdatera_gui(dölj_dealer_kort=False)

        # STORA VILLKORSBLOCKET för vinst
        vinnare = None
        
        if dl_poang > 21:
            vinnare = "SPELARE"
            text = "Dealer Bust! Du vinner!"
        elif dl_poang > sp_poang:
            vinnare = "DEALER"
            text = f"Dealer vinner med {dl_poang}."
        elif sp_poang > dl_poang:
            vinnare = "SPELARE"
            text = f"Du vinner med {sp_poang}!"
        else:
            vinnare = "PUSH"
            text = "Push (Oavgjort)."

        self.status_etikett.config(text=text)
        self.avsluta_hand(vinnare)
        
    def avsluta_hand(self, resultat):
        self.hit_knapp["state"] = "disabled"
        self.stand_knapp["state"] = "disabled"
        self.ny_hand_knapp["state"] = "normal"
        
        # Utbetalning
        if resultat == "SPELARE":
            self.pengar += self.insats
        elif resultat == "DEALER":
            self.pengar -= self.insats
        
        self.uppdatera_gui(dölj_dealer_kort=False)

        # VILLKOR: Game Over
        if self.pengar <= 0:
            self.status_etikett.config(text="GAME OVER! Du har förlorat alla dina pengar.")
            self.ny_hand_knapp["state"] = "disabled"
            
# --- 3. Programstart ---

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackApp(root)
    root.mainloop()