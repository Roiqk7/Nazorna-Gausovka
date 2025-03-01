"""
Datum: 15. 12. 2024

Vstupní bod programu
"""

from zpracovaniArgumentu import parser, zpracujArgumenty

def main():
        """
        Vstupní bod programu
        """
        # Zpracování argumentů
        zpracujArgumenty(parser.parse_args())

if __name__ == "__main__":
        main()