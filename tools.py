from datetime import datetime

pt = 95
ls = 141

class SpInputs:

    def __init__(self, text: str) -> None:
        self.text = text
    
    def withoptions(self, options: list[str], up=True) -> str:
        while True:
            x = input(self.text).strip()
            x = x.upper() if up else x
            if x in options:
                return x
            else:
                print('Invalid input.')

    def yesorno(self) -> bool:
        self.text += ' [Y/N]'
        x = self.withoptions(['Y', 'N'], True)
        return True if x == 'Y' else False

    def dt(self) -> str:
        self.text += ' [YYYY-MM-DD] '
        while True:
            x = input(self.text).strip()
            if x == '':
                return x
            else:
                try:
                    datetime.fromisoformat(x)
                    return x
                except:
                    print('Invalid input')

    def floating(self) -> float:
        self.text += ' [0.00] '
        while True:
            x = input(self.text).strip()
            try:
                return float(x)
            except:
                print('Invalid input.')
                
    def int_number(self) -> int:
        x = input(self.text).strip()
        try:
            return int(x)
        except:
            print("Invalid input. Please input a 'int' number.")
