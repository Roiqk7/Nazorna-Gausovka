""" 
Datum: 16. 12. 2024

Ukázka programu na soustavě rovnic
"""

from matice import Matice
from gauss import reseniSoustavy
from tisk import MiraTisku, pockej, vytiskniChybu
from vektor import Vektor

def mainUkazka():
        """
        Ukázka programu na soustavě rovnic

        Ve skriptech pana prof. Milana Hladíka se jedná o příklad 2.18

        Správné řešení:
        x1 = 5/2x3 - 4
        x2 = -2x3 + 2
        x3 je volná proměnná
        x4 = 1
        """
        print("Ukázka programu na soustavě lineárních rovnic ze skript pana prof. Milana Hladíka (příklad 2.18)")
        pockej()
        prava = Matice(4, 1, [1, 3, 4, 7])
        matice = Matice(4, 4, [2, 2, -1, 5, 4, 5, 0, 9, 0, 1, 2, 2, 2, 4, 3, 7], prava)
        reseni = reseniSoustavy(matice, MiraTisku.MEGA)

        # Kontrola správnosti řešení (viz výše)
        ocekavane = [Vektor(5, [1, 0, 5/2, 0, -4]), Vektor(5, [0, 1, -2, 0, 2]), Vektor(5, [0, 0, 0, 1, 1])]
        if reseni != ocekavane:
                vytiskniChybu("Špatně spočítané řešení. Ukázka se nepovedla... :(")

if __name__ == "__main__":
        mainUkazka()