from tools import SpInputs
from datetime import datetime

def build_adress() -> list[str]:
    while True:
        x = input("Entity's adress in the following format: \n number, street, complementary info (apt number, etc), city, state, postal code, country \n")
        x = x.split(',')
        if len(x) != 7:
            print('Invalid input, please pay atention to the number of arguments (separated by commas).')
        else:
            return x

class Entity:

    def __init__(self, key: str, name: str, adress: list[str], contact: tuple[str, str]) -> None:
        key_array = key.split('$')
        if len(key_array) != 2:
            raise ValueError(f"Insufficient or too much data on the following Entity's id_key: {key_array}.\nIt should have 2.")
        
        self.key = key # 'id document type'$'id document number/code'
        self.name = name
        self.adress = adress # (number, street, complementary info, city, state, postal code, country) *complementary info = apt number, etc
        self.contact = contact # (phone, email)

    def id_info(self) -> tuple[str, str]:
        return tuple(self.key.split('$')) # ('id document type', 'id document number/code' )

    def to_list(self) -> list[str]:
        return [
            self.key,
            self.name,
            self.adress,
            self.contact]

    def __str__(self) -> str:
        y = 'Own' if self.tp else 'Supplier/client'
        x = [
            f" [ 1 ] Key: {self.key}",
            f" [ 2 ] Name: {self.name}",
            f" [ 3 ] Adress (number, street, complementary info, city, state, postal code, country):",
            f"         {self.adress}",
            f" [ 4 ] Phone, email: {self.contact}",]
        return '\n'.join(x)

    def display(self) -> str:
        x = [
            f"Name: {self.name}",
            f"ID({self.id_info()[0]}): {self.id_info()[1]}",
            f"Adress: {self.adress[0]} {self.adress[1]}, {self.adress[2]}, {self.adress[3]}, {self.adress[4]} {self.adress[5]}, {self.adress[6]}",
            f"Phone: {self.contact[0]}",
            f"Email: {self.contact[1]}"]
        return '\n'.join(x)

class Account:

    def __init__(self, key: str, name:str, nature: bool) -> None:
        self.key = key
        self.name = name
        self.nature = nature # True = cash account | False = credit card account

    def to_list(self) -> list:
        return [self.key, self.name, self.nature]

    def __str__(self) -> str:
        y = 'Movement' if self.nature is True else 'Savings'
        x = [
            f" [ 1 ] Key: {self.key}",
            f" [ 2 ] Name: {self.name}",
            f" [ 3 ] Nature: {y}"]
        return '\n'.join(x)

    def display(self) -> str:
        return f"({self.key}) {self.name}"

class Rev_Exp:

    def __init__(self, key: str, name: str, nature: bool, category: int, sub: int) -> None:
        self.key = key
        self.name = name
        self.nature = nature # True = Revenue | False = Expense
        self.category = category # 1 = Operational | 2 = Financing | 3 = Investing
        self.sub = sub
            # About sub:
                # Revenue: 0 = Others | 1 = Sales | 2 = Services | 3 = Contracts
                # Expense: 0 = Others | 1 = Supplies | 2 = Employee | 3 = Facilities | 4 = Transport | 5 = Insurance | 6 = Marketing

    def to_list(self) -> list:
        return [self.key, self.name, self.nature, self.category, self.sub]

    def naturestr(self) -> str:
        return 'Revenue' if self.nature else 'Expense'

    def categorystr(self) -> str:
        match self.category:
            case 1:
                return 'Operational'
            case 2:
                return 'Financing'
            case 3:
                return 'Investing'

    def substr(self) -> str:
        match self.sub:
            case 0:
                return 'Others'
            case 1:
                return 'Sales' if self.nature else 'Supplies'
            case 2:
                return 'Services' if self.nature else 'Employee'
            case 3:
                return 'Contracts' if self.nature else 'Facilities'
            case 4:
                return 'Transport'
            case 5:
                return 'Insurance'
            case 6:
                return 'Marketing'
            
    def __str__(self) -> str:
        x = [
            f" [ 1 ] Key: {self.key}",
            f" [ 2 ] Name: {self.name}",
            f" [ 3 ] Nature: {self.naturestr()}",
            f" [ 4 ] Category: {self.categorystr()}",
            f" [ 5 ] Subcategory: {self.substr()}"]
        return '\n'.join(x)

    def display(self) -> str:
        return f"({self.key}) {self.name}"

class RootFile:

    def __init__(self, data: dict[str, object]) -> None:
        self.own = Entity(*data['own'])
        self.accounts = {key: Account(*item) for key, item in data['accounts'].items()}
        self.revenues = {key: Rev_Exp(*item) for key, item in data['revenues'].items()}
        self.expenses = {key: Rev_Exp(*item) for key, item in data['expenses'].items()}
        self.lock = data['lock']

    def to_dict(self) -> dict[str, object]:
        return {
            'own': self.own.to_list(),
            'accounts': {key: item.to_list() for key, item in self.accounts.items()},
            'revenues': {key: item.to_list() for key, item in self.revenues.items()},
            'expenses': {key: item.to_list() for key, item in self.expenses.items()},
            'lock': self.lock}

class EntitiesFile:
    
    def __init__(self, data: dict[str, object]) -> None:
        self.entities = {key: Entity(*item) for key, item in data.items()}

    def to_dict(self) -> dict[str, object]:
        x = {key: item.to_list() for key, item in self.entities.items()}
        return x

class EntitiesManager:

    def __init__(self, rf: RootFile, ef: EntitiesFile) -> None:
        self.rf = rf
        self.ef = ef

    def entities_keys(self) -> list[str]:
        x = [self.rf.own.key]
        x += list(self.ef.entities.keys())
        return x

    def build_key(self) -> str:
        while True:
            key = (input('Type the ID docuemnt type: ').strip().upper(), input('Dcoument number: ').strip())
            key = '$'.join(key)
            if len(key.split('$')) != 2:
                print("Please, refrain for using '$' in the input.")
            elif key in self.entities_keys():
                print('This entitiy is already recorded.')
            else:
                return key

    def new(self) -> None:
        x = Entity(self.build_key(), input("Entity's name: ").strip(), build_adress(), (input('Phone number: ').strip(), input('Email: ').strip()))
        print(x)
        if SpInputs('Confirm the recording?').yesorno():
            self.ef.entities[x.key] = x
        else:
            print('Recording cancelled.')

    def edit(self) -> None:
        keys = self.entities_keys()
        selected = SpInputs('Type the key of the entity that you desire to edit: ').withoptions(keys)
        if selected == keys[0]:
            selected = self.rf.own
            switch = True
        else:
            selected = self.ef.entities[selected]
            switch = False
        while True:
            print(selected)
            match SpInputs("Type the corresponding index of what you desire to edit [R to return]:").withoptions('R', '1', '2', '3', '4'):
                case 'R':
                    break
                case '1':
                    oldkey = selected.key
                    x = self.build_key()
                    selected.key = x
                    if not switch:
                        self.ef.entities[x] = selected
                        del self.ef.entities[oldkey]
                        break
                case '2':
                    selected.name = input("Entity's name: ").strip()
                case '3':
                    selected.adress = build_adress()
                case '4':
                    selected.contact = (input('Phone number: ').strip(), input('Email: ').strip())

class RootManager:

    def __init__(self, rf: RootFile) -> None:
        self.rf = rf
                    
    def new_account(self) -> None:
        keys = self.rf.accounts.keys()
        nature = SpInputs('It will be a cash [Y] or a credit card [N] account? ').yesorno()
        key = input('Type a key for the new cash account that you desire to record: ').strip().upper()
        if key in keys:
            print('This account key already exists.')
        else:
            x = Account(key, input('Account name: ').strip(), nature)
            print(x)
            if SpInputs('Confirm the recording?').yesorno():
                self.rf.accounts[key] = x
            else:
                print('Recording cancelled.')

    def edit_account(self) -> None:
        keys = self.rf.accounts.keys()
        selected = SpInputs('Type the key of the account that you desire to record: ').withoptions(keys)
        selected = self.rf.accounts[selected]
        while True:
            print(selected)
            match SpInputs("Type the corresponding index of what you desire to edit [R to return] (keys aren't editable): ").withoptions(['R', '2', '3']):
                case 'R':
                    break
                case '2':
                    selected.name = input('New account name: ').strip()
                case '3':
                    selected.nature = SpInputs('It should be a cash [Y] or a credit card [N] account? ').yesorno()

    def revexp_select(self, switch: bool) -> tuple[dict[str,object], str, list[str], str, list[str]]:
        if switch:
            sel = self.rf.revenues
            txt = 'Revenue'
            subquestion = f"Select the corresponding {txt} subcategory: \n [ 1 ] Sales \n [ 2 ] Services \n [ 3 ] Contracts \n [ 0 ] Others \n"
            subopt = ['0', '1', '2', '3']
        else:
            sel = self.rf.expenses
            txt = 'Expense'
            subquestion = f"Select the corresponding {txt} subcategory: \n [ 1 ] Supplies \n [ 2 ] Employee \n [ 3 ] Facilities \n [ 4 ] Transport \n [ 5 ] Insurance \n [ 6 ] Marketing \n [ 0 ] Others \n"
            subopt = ['0', '1', '2', '3', '4', '5', '6', '7']
        lis = list(sel.keys())
        return sel, txt, lis, subquestion, subopt

    def new_revexp(self, switch: bool) -> None: # True for revenue | False for expenses
        sel = self.revexp_select(switch)
        key = input(f"Type a key for the new {sel[1]} that you desire to record: ").strip().upper()
        if key in sel[2]:
            print(f"This {sel[1]} already exists.")
        else:
            cat = int(SpInputs('Corresponing revenue/expense category: \n [ 1 ] Operational \n [ 2 ] Financing \n [ 3 ] Investing \n').withoptions(['1', '2', '3']))
            x = Rev_Exp(
                key,
                input(f"{sel[1]} name: ").strip(),
                switch,
                cat,
                int(SpInputs(sel[3]).withoptions(sel[4]) if cat == 1 else 0))
            print(x)
            if SpInputs('Confirm the recording?').yesorno():
                sel[0][key] = x
            else:
                print('Recording cancelled.')

    def edit_revexp(self, switch: bool) -> None: # True for revenue | False for expenses
        sel = self.revexp_select(switch)
        selected = SpInputs(f"Type the key of the {sel[1]} that you desire to edit: ").withoptions(sel[2])
        selected = sel[0][selected]
        while True:
            print(selected)
            match SpInputs("Type the corresponding index of what you desire to edit [R to return] (keys and nature aren't editable): ").withoptions(['R', '2', '4', '5']):
                case 'R':
                    break
                case '2':
                    selected.name = input('New name: ').strip()
                case '4':
                    selected.category = int(SpInputs('New corresponing revenue/expense category: \n [ 1 ] Operational \n [ 2 ] Financing \n [ 3 ] Investing \n').withoptions(['1', '2', '3']))
                case '5':
                    if selected.category == 1:
                        selected.sub = int(SpInputs(sel[3]).withoptions(sel[4]))
                    else:
                        print('Only operational expenses can have a subcategory.')

class Entry:

    def __init__(self, key: str, flow: bool, account: str, nature: tuple[int, str], dt: str, value: float, notes: str, valid: bool) -> None:
        self.key = key
        self.flow = flow # True for inflows, False for outflows
        self.account = account # Account key
        self.nature = nature # [0] is a nature identifier (0 = Others | 1 = Transaction btw accounts | 2 = Direct revenue/expense | 3 = Allowance/refund) and [1] is its key
        self.dt = datetime.fromisoformat(dt)
        self.value = value
        self.notes = notes
        self.valid = valid
            # OBS: In case of the self.natue[0] == 3 (allowance or refund), self.nature[1] should be the key of the associeted revenue/expense

    def to_list(self) -> list:
        return [self.key, self.flow, self.account, self.nature, self.dt.isoformat(), self.value, self.notes, self.valid]

    def __str__(self) -> str:
        flow = 'Inflow' if self.flow else 'Outflow'
        match self.nature[0]:
            case 0:
                nat = 'Other transactions'
            case 1:
                nat = 'Transaction btw accounts'
            case 2:
                nat = 'Revenue' if self.flow else 'Expense'
            case 3:
                nat = 'Allowance/refund'
        x = [
            f" [ 1 ] Key: {self.key}",
            f" [ 2 ] Flow: {flow}",
            f" [ 3 ] Account key: {self.account}",
            f" [ 4 ] Nature: ({self.nature[0]}){nat} - {self.nature[1]}",
            f" [ 5 ] Date: {self.dt.date().isoformat()}",
            f" [ 6 ] Value: {self.value:,.2f}",
            f" [ 7 ] Notes: {self.notes}",
            f" [ 8 ] Valid: {self.valid}"]
        return '\n'.join(x)

class EntriesFile:

    def __init__(self, data: dict[str, object]) -> None:
        self.entries = {key: Entry(*item) for key, item in data['entries'].items()}
        self.open = data['open'] # cash accounts open balance: dict[account key, value]

    def to_dict(self) -> dict[str, list]:
        return {
            'entries': {key: item.to_list() for key, item in self.entries.items()},
            'open': self.open}

class EntriesManager:

    def __init__(self, rf: RootFile, ef: EntriesFile, year: int) -> None:
        self.rf = rf
        self.ef = ef
        self.year = year
                        
    def new(self) -> None:
        n = len(self.ef.entries.keys())
        flow = SpInputs('It is a inflow[Y] or outflow[N] entry?').yesorno()
        acc = SpInputs('Type the referent account key: ').withoptions(self.rf.accounts.keys())
        nature_zero = int(SpInputs("Type the entry's nature: \n [ 0 ] Others \n [ 1 ] Transaction btw accounts \n [ 2 ] Direct revenue/expense \n [ 3 ] Direct refund \n").withoptions(['0', '1', '2', '3']))
        match nature_zero:
            case 0:
                nature_one = ''
            case 1:
                while True:
                    nature_one = SpInputs("Type the entry's counter account key: ").withoptions(self.rf.accounts.keys())
                    if nature_one == acc:
                        print("A transaction btw accounts cannot happen btw the same account.")
                    else:
                        break
            case 2:
                select = RootManager(self.rf).revexp_select(flow)
                nature_one = SpInputs(f"Type the referent {select[1]} key: ").withoptions(select[2])
            case 3:
                select = RootManager(self.rf).revexp_select(not flow)
                nature_one = SpInputs(f"Type the targeted {select[1]} key for the refund/allowance: ").withoptions(select[2])
        nature = (nature_zero, nature_one)
        dt = SpInputs("Entry's date:").dt()
        value = SpInputs("Entry's value:").floating()
        notes = input('Notes: ').strip()
        x = Entry(f"{self.year}-{n+1}", flow, acc, nature, dt, value, notes, True)
        print(x)
        if SpInputs('Confirm the recording?').yesorno():
            self.ef.entries[x.key] = x
            print('Recorded with success.')
        if nature[0] == 1 and SpInputs('Do you desire to already record the counter entry for the transaction btw accounts?').yesorno():
            y = Entry(f"{self.year}-{n+2}", not flow, nature_one, (nature_zero, acc), dt, value, notes, True)
            print('')
            print(y)
            if SpInputs('Confirm the recording?').yesorno():
                self.ef.entries[y.key] = y
                print('Recorded with success.')

    def edit(self) -> None:
        select = SpInputs("Type the key of the year's entry that you desire to edit: ").withoptions(self.ef.entries.keys())
        select = self.ef.entries[select]
        while True:
            print(select)
            match SpInputs("Type the corresponding index of what you desire to edit [R to return] (Keys aren't editable):").withoptions(['R', '2', '3', '4', '5', '6', '7', '8']):
                case 'R':
                    break
                case '2':
                    select.flow = SpInputs('It is a inflow[Y] or outflow[N] entry?').yesorno()
                case '3':
                    select.account = SpInputs('Type the referent account key: ').withoptions(self.rf.accounts.keys())
                    if self.nature[0] == 1:
                        print("Remember to check the counter account in the entry's nature.")
                case '4':
                    zero =  int(SpInputs("Type the entry's nature: \n [ 0 ] Others \n [ 1 ] Transaction btw accounts \n [ 2 ] Direct revenue/expense \n [ 3 ] Direct refund \n").withoptions(['0', '1', '2', '3']))
                    match zero:
                        case 0:
                            one = ''
                        case 1:
                            while True:
                                one = SpInputs("Type the entry's counter account key: ").withoptions(self.rf.accounts.keys())
                                if one == select.account:
                                    print("A transaction btw accounts cannot happen btw the same account.")
                                else:
                                    break
                        case 2:
                            z = RootManager(self.rf).revexp_select(select.flow)
                            one = SpInputs(f"Type the referent {z[1]} key: ").withoptions(z[2])
                        case 3:
                            z = RootManager(self.rf).revexp_select(not select.flow)
                            one = SpInputs(f"Type the targeted {z[1]} key for the allowance: ").withoptions(z[2])
                    select.nature = [zero, one]
                case '5':
                    select.dt = datetime.fromisoformat(SpInputs("Entry's date: ").dt())
                case '6':
                    select.value = SpInputs("Entry's value: ").floating()
                case '7':
                    select.notes = input('Notes: ').strip()
                case '8':
                    select.valid = SpInputs('The entry is valid?').yesorno()
