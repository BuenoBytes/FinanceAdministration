from copy import deepcopy
from datetime import datetime
from typing import TypedDict
import tools

settings = tools.FilesManagers.get_json('_settings.json')

# Root file classes -----------------------------------------------------------------------------------------------------------
  
class Entity:

    def __init__(self, id_info: tuple[str, str], name: str, address: str, contact_info: tuple[str, str]) -> None:
        self.id_info = tuple([tools.ObjCheck(item).max_length(Entity.settings('ID ITEMS MAX LENGTH')) for item in id_info])
        self.name = tools.ObjCheck(name).max_length(Entity.settings('NAME MAX LENGTH'))
        self.address = self.parse_address(address)
        self.contact_info = tuple([tools.ObjCheck(item).max_length(Entity.settings('CONTACT ITEMS MAX LENGTH')) for item in contact_info])

    @staticmethod
    def settings(key: str):
        return settings['ENTITY'][key]

    @staticmethod
    def parse_address(string: str) -> str:
        address = tools.ObjCheck(string).max_length(Entity.settings('ADDRESS MAX LENGTH'))
        tools.ObjCheck(string.split(',')).length(Entity.settings('ADDRESS PARTS'))
        return address

    def key(self) -> str:
        return '$'.join(self.id_info)

    def display(self) -> str:
        x = [
            f"Name: {self.name}",
            f"ID({self.id_info[0]}): {self.id_info[1]}",
            f"Address: {self.address}",
            f"Phone: {self.contact_info[0]}",
            f"Email: {self.contact_info[1]}"]
        return '\n'.join(x)

    def __str__(self) -> str:
        x = [
            f" [ 1 ] Key: {self.key()}",
            f" [ 2 ] Name: {self.name}",
            f" [ 3 ] Address (number, street, complementary info, city, state, postal code, country):",
            f"         {self.address}",
            f" [ 4 ] Phone, email: {self.contact_info}",]
        return '\n'.join(x)

    def to_list(self) -> list[str | tuple[str, ...]]:
        return [
            self.id_info,
            self.name,
            self.address,
            self.contact_info ]

class Account:

    def __init__(self, key: str, name: str, nature: bool) -> None:
        self.key = tools.ObjCheck(key).length(Account.settings('KEY LENGTH')).upper()
        self.name = tools.ObjCheck(name).max_length(Account.settings('NAME MAX LENGTH'))
        self.nature = bool(nature) # True = cash account | False = credit card account

    @staticmethod
    def settings(key: str):
        return settings['ACCOUNT'][key]
    
    def to_list(self) -> list:
        return [self.key, self.name, self.nature]

    def __str__(self) -> str:
        y = 'Cash account' if self.nature is True else 'Credit card'
        x = [
            f" [ 1 ] Key: {self.key}",
            f" [ 2 ] Name: {self.name}",
            f" [ 3 ] Nature: {y}"]
        return '\n'.join(x)

    def display(self) -> str:
        return f"({self.key}) {self.name}"

class RevExp:

    def __init__(self, key: str, name: str, operational: bool, category: str) -> None:
        self.key = tools.ObjCheck(key).length(RevExp.settings('KEY LENGTH')).upper()
        self.name = tools.ObjCheck(name).max_length(RevExp.settings('NAME MAX LENGTH'))
        self.operational = operational
        self.category = category

    @staticmethod
    def settings(key: str):
        return settings['REVEXP'][key]

    def display(self) -> str:
        return f"({self.key}) {self.name}"

    def __str__(self) -> str:
        x = [
            f" [ 1 ] Key: {self.key}",
            f" [ 2 ] Name: {self.name}",
            f" [ 3 ] Operational: {self.operational}",
            f" [ 4 ] Category: {self.category}"]
        return '\n'.join(x)

    def to_list(self) -> list:
        return [self.key, self.name, self.operational, self.category]

class Revenue(RevExp):
    def __init__(self, key: str, name: str, operational: bool, category: str) -> None:
        super().__init__(key, name, operational, category)
        self.category = Revenue.parse_category(operational, category)
    
    @staticmethod
    def parse_category(operational: bool, category: str) -> str:
        categories = 'OPREV CATEGORIES' if operational else 'NON-OP CATEGORIES'
        return tools.ObjCheck(category).options(RevExp.settings(categories))

class Expense(RevExp):
    def __init__(self, key: str, name: str, operational: bool, category: str) -> None:
        super().__init__(key, name, operational, category)
        self.category = self.parse_category(operational, category)

    @staticmethod
    def parse_category(operational: bool, category: str) -> str:
        categories = 'OPEXP CATEGORIES' if operational else 'NON-OP CATEGORIES'
        return tools.ObjCheck(category).options(RevExp.settings(categories))

# Root file class and build -------------------------------------------------------------------------------------------------

class RootFileSchema(TypedDict):
    own: list
    accounts: dict[str, list]
    revenues: dict[str, list]
    expenses: dict[str, list]

class RootFile:

    def __init__(self, data: RootFileSchema) -> None:
        self.own = Entity(*data['own'])
        self.accounts = {key: Account(*item) for key, item in data['accounts'].items()}
        self.revenues = {key: Revenue(*item) for key, item in data['revenues'].items()}
        self.expenses = {key: Expense(*item) for key, item in data['expenses'].items()}

    def to_dict(self) -> dict[str, object]:
        return {
            'own': self.own.to_list(),
            'accounts': {key: item.to_list() for key, item in self.accounts.items()},
            'revenues': {key: item.to_list() for key, item in self.revenues.items()},
            'expenses': {key: item.to_list() for key, item in self.expenses.items()}}
    
    @staticmethod
    def process_obj(attribute: str, obj: list) -> Account|Revenue|Expense:
        if attribute == 'accounts':
            return Account(*obj)
        elif attribute == 'revenues':
            return Revenue(*obj)
        elif attribute == 'expenses':
            return Expense(*obj)
        else:
            raise ValueError(f"The attribute {attribute} is not valid for rootfile.")

    def new(self, attribute: str, obj: list) -> str:
        processed__obj = RootFile.process_obj(attribute, obj)
        branch = getattr(self, attribute)
        if processed__obj.key not in branch.keys():
            branch[processed__obj.key] = processed__obj
            return "{processed__obj.key} was recorded with success on the {attribute} branch."
        else:
            raise ValueError(f"The {processed__obj.key} already exists on the {attribute} branch of rootfile.")

    def edit(self, attribute: str, obj: list) -> str:
        processed_obj = RootFile.process_obj(attribute, obj)
        branch = getattr(self, attribute)
        if processed_obj.key not in branch.keys():
            raise ValueError(f"The {processed_obj.key} doesn't exists on the {attribute} branch of rootfile.")
        else:
            branch[processed_obj.key] = processed_obj
            return "{processed_obj.key} was edited with success on the {attribute} branch."

    def filter_accounts(self) -> dict[str, list[str]]:
        # return {'cash': [list of accounts keys], 'credit_cards': [list of credit card accounts keys]}
        cash_list = []
        credit_card_list = []
        for key, item in self.accounts.items():
            if item.nature:
                cash_list += [key]
            else:
                credit_card_list += [key]
        return {'cash': cash_list, 'credit_cards': credit_card_list}

    def filter_revexp(self, switch: bool) -> dict[str, dict[str, Revenue|Expense]]: 
        # return {'operational': [dict of operational revexp], 'financing': [dict of financing revexp], 'investing': [dict of investing revexp]}
        # if switch is True it will filter revenues, else expenses
        x = {'operational': {}, 'financing': {}, 'investing': {}}
        branch = self.revenues if switch else self.expenses
        for key, item in branch.items():
            if item.operational:
                x['operational'][key] = item
            else:
                if item.category == 'Financing':
                    x['financing'][key] = item
                else:
                    x['investing'][key] = item
        return x

# Entries class and Entries file class --------------------------------------------------------------------------------------------

class Entry:

    def __init__(self, key: str, account: str, flow: bool, nature: tuple[str, str], dt: str, value: float, notes: str, valid: bool) -> None:
        self.key = key.upper()
        self.account = tools.ObjCheck(account).length(Account.settings('KEY LENGTH')).upper()
        self.flow = bool(flow) # True=Inflow | False=Outflow
        self.nature = (tools.ObjCheck(nature[0]).options(Entry.settings('NATURES')), nature[1])
        self.dt = datetime.fromisoformat(dt)
        self.value = float(value)
        self.notes = notes
        self.valid = bool(valid)

    @staticmethod
    def settings(key: str):
        return settings['ENTRY'][key]

    def to_list(self) -> list:
        return [self.key, self.account, self.flow, self.nature, self.dt.isoformat(), self.value, self.notes, self.valid]

    @staticmethod
    def flow_str(switch: bool) -> str:
        return 'Inflow' if switch else 'Outflow'

    def __str__(self) -> str:
        x = [
            f" [ 1 ] Key: {self.key}",
            f" [ 2 ] Account: {self.account}",
            f" [ 3 ] Flow: {Entry.flow_str(self.flow)}",
            f" [ 4 ] Nature: {self.nature}",
            f" [ 5 ] Date: {self.dt.isoformat()}",
            f" [ 6 ] Value: {self.value:,.2f}",
            f" [ 7 ] Notes: {self.notes}",
            f" [ 8 ] Valid: {self.valid}"]
        return '\n'.join(x)
    
class EntriesFileSchema(TypedDict):
    entries: dict[str, list]
    open_balance: dict[str, float]

class EntriesFile:

    def __init__(self, data: EntriesFileSchema, rootfile: RootFile, year: int) -> None:
        self.year = year
        self.rf = rootfile
        self.prefix = f"ENT{year}"
        self.lock = settings['LOCK']
        self.entries = {key: Entry(*item) for key, item in data['entries'].items()}
        self.open_balance = data['open_balance']
        
    def check_lock(self) -> None:
        if self.year <= self.lock:
            raise ValueError(f"All years equal or before {self.year} are locked.")

    def build(self, obj: Entry) -> Entry:
        self.check_lock()
        obj.key = '/'.join([self.prefix, str(len(self.entries.keys()) +1)])
        if obj.dt.year != self.year:
            raise ValueError(f"Entry year ({obj.dt.year}) different of the manager {self.year}.")
        if obj.account not in self.rf.accounts.keys():
            raise ValueError(f"The account {obj.account} doesn't exist in the rootfile.")
        if obj.nature[0] == 'Transaction btw accounts' and obj.nature[1] not in self.rf.accounts.keys():
            raise ValueError(f"The account {obj.nature[1]} doesn't exist in the rootfile.")
        if obj.nature[0] == 'Direct reveenue/expense':
            if obj.flow:
                branch = self.rf.revenues
                text = 'revenue'
            else:
                branch = self.rf.expenses
                text = 'expense'
            if obj.nature[1] not in branch.keys():
                raise ValueError(f"The {text} {obj.nature[1]} doesn't exist in the rootfile.")
        if obj.nature[0] == 'Revenue/expense refund':
            if obj.flow:
                branch = self.rf.expenses
                text = 'expense'
            else:
                branch = self.rf.revenues
                text = 'revenue'
            if obj.nature[1] not in branch.keys():
                raise ValueError(f"The {text} {obj.nature[1]} doesn't exist in the rootfile.")
        return obj

    def new(self, obj: Entry) -> str:
        obj = self.build(obj)
        if obj.key not in self.entries.keys():
            self.entries[obj.key] = obj
            return f"Entry {obj.key} recorded with success."
        else:
            raise ValueError(f"The Entry {obj.key} already exists on the file.")

    def edit(self, obj: Entry, key: str) -> str:
        obj = self.build(obj)
        obj.key = key
        if obj.key not in self.entries.keys():
            raise ValueError(f"The entry (obj.key) doesn't exists on the file.")
        else:
            self.entries[obj.key] = obj
            return f"Entry {obj.key} edited with success."

    def to_dict(self) -> dict[str, object]:
        return {
            'entries': {key: item.to_list() for key, item in self.entries.items()},
            'open_balance': self.open_balance}
    
# Balances class -------------------------------------------------------------------------------------------------------------

class BalancesBase:

    def __init__(self, rf: RootFile, ef: EntriesFile, open_dt: str, close_dt: str) -> None:
        self.rf = rf
        self.ef = ef
        self.open_dt = datetime.fromisoformat(open_dt)
        self.close_dt = datetime.fromisoformat(close_dt)

    @classmethod
    def build_ef(cls, rf: RootFile, open_dt: str, close_dt: str) -> 'BalancesBase':
        ef: EntriesFileSchema = {'entries': {}, 'open_balance': {}}
        selection = tools.FilesManagers.select_years(open_dt, close_dt)
        for year in selection:
            try:
                data = tools.FilesManagers.get_json(f"entries/{year}.json")
                ef['entries'].update(data['entries'])
                if year == selection[0]:
                    ef['open_balance'].update(data['open_balance'])
            except FileNotFoundError:
                pass
        ef_file = EntriesFile(ef, rf, 0)
        return cls(rf, ef_file, open_dt, close_dt)

class BalancesSchema(TypedDict):
    accounts: dict[str, list[float]]
    revenues: dict[bool, dict[str, dict[str, list[float]]]]
    expenses: dict[bool, dict[str, dict[str, list[float]]]]
    others: list[float]
    # Tree explanation for revenues and expenses:
    # {
    #   True for Operational | False for Non-operational: {
    #     'category': { 'revenue_expense_key': [value, allowance] }
    #   },
    # }

class Balances:
    def __init__(self, data: BalancesSchema, rf: RootFile) -> None:
        self.data = data
        self.rf = rf

    @classmethod
    def process_entries(cls, base_data: BalancesBase) -> 'Balances':
        rev_tree = {
            True: {},  # Operational
            False: {}} # Non-operational
        rev_tree[False] = {item: {} for item in RevExp.settings('NON-OP CATEGORIES')}
        exp_tree = deepcopy(rev_tree)
        rev_tree[True] = {item: {} for item in RevExp.settings('OPREV CATEGORIES')}
        exp_tree[True] = {item: {} for item in RevExp.settings('OPEXP CATEGORIES')}
        x: BalancesSchema = {
            'accounts': {},
            'revenues': rev_tree,
            'expenses': exp_tree,
            'others': [0.0, 0.0]}
        for key in base_data.rf.accounts.keys():
            x['accounts'][key] = [0.0, 0.0, 0.0] # open balance, inflows, outflows
        for key, item in base_data.rf.revenues.items():           
            x['revenues'][item.operational][item.category][key] = [0.0, 0.0] # values, allowances/refunds
        for key, item in base_data.rf.expenses.items():
            x['expenses'][item.operational][item.category][key] = [0.0, 0.0] # values, allowances/refunds
        for key, item in base_data.ef.open_balance.items():
            x['accounts'][key][0] += item
        for key, item in base_data.ef.entries.items():
            if item.valid:
                x_account = x['accounts'][item.account]
                if item.dt < base_data.open_dt:
                    if item.flow:
                        x_account[0] += item.value
                    else:
                        x_account[0] -= item.value
                elif item.dt <= base_data.close_dt:
                    flag = 1 if item.flow else 2
                    x_account[flag] += item.value
                    if item.nature[0] == 'Others':
                        x['others'][int(not item.flow)] += item.value
                    elif item.nature[0] == 'Direct revenue/expense' or item.nature[0] == 'Revenue/expense refund':
                        if item.nature[0] == 'Direct revenue/expense':
                            revexp_flag = 'revenues' if item.flow else 'expenses'
                            value_flag = 0
                        else:
                            revexp_flag = 'expenses' if item.flow else 'revenues'
                            value_flag = 1
                        revexp_branch = base_data.rf.revenues if revexp_flag == 'revenues' else base_data.rf.expenses
                        revexp_obj = revexp_branch[item.nature[1]]
                        x[revexp_flag][revexp_obj.operational][revexp_obj.category][item.nature[1]][value_flag] += item.value
        return cls(x, base_data.rf)
    
    def income_st_structure(self, operational: bool) -> tuple[list[str], list[str], float]:
        # builds income statement structure for operational or non-operational revenues and expensese
        descriptions_list, values_list, total = [], [], 0.0
        if operational:
            revenues_branch = self.data['revenues'][True]
            expenses_branch = self.data['expenses'][True]
            text_string = 'Operational'
        else:
            revenues_branch = self.data['revenues'][False]
            expenses_branch = self.data['expenses'][False]
            text_string = 'Non-operational'
        descriptions_list.append(f"**{text_string} Revenues**")
        values_list.append('\u200b')
        for category in revenues_branch.keys():
            sub_descriptions_list, sub_values_list, sub_total = [], [], 0.0
            for key, item in revenues_branch[category].items():
                if item[0] != 0:
                    sub_total += item[0]
                    sub_descriptions_list.append(f"{'&nbsp;'*20}({key}) {self.rf.revenues[key].name}")
                    sub_values_list.append(tools.format_value(item[0], True))
                if item[1] != 0:
                    sub_total -= item[1]
                    sub_descriptions_list.append(f"{'&nbsp;'*20}Allowances/refunds")
                    sub_values_list.append(tools.format_value(item[1], False))
            if len(sub_descriptions_list) > 0:
                descriptions_list.append(f"{'&nbsp;'*10}{category}")
                values_list.append('\u200b')
                descriptions_list += sub_descriptions_list
                values_list += sub_values_list
                total += sub_total
        descriptions_list.append(f"**{text_string} Expenses**")
        values_list.append('\u200b')
        for category in expenses_branch.keys():
            sub_descriptions_list, sub_values_list, sub_total = [], [], 0.0
            for key, item in expenses_branch[category].items():
                if item[1] != 0:
                    item[0] -= item[1]
                if item[0] != 0:
                    sub_total += item[0]
                    sub_descriptions_list.append(f"{'&nbsp;'*20}({key}) {self.rf.expenses[key].name}")
                    sub_values_list.append(tools.format_value(item[0], False))
            if len(sub_descriptions_list) > 0:
                descriptions_list.append(f"{'&nbsp;'*10}{category}")
                values_list.append('\u200b')
                descriptions_list += sub_descriptions_list
                values_list += sub_values_list
                total -= sub_total
        descriptions_list.append("\u200b")
        values_list.append("----------")
        descriptions_list.append(f"***= Net {text_string} Income / Loss***")
        values_list.append(f"{tools.format_value(total, True)}")
        return descriptions_list, values_list, total 

def lock_year(year: int, rf: RootFile) -> None:
    settings = tools.FilesManagers.get_json('_settings.json')
    if year <= settings['LOCK']:
        raise ValueError(f"The year {year} is already locked.")
    else:
        balances = Balances.process_entries(BalancesBase.build_ef(rf, f"{year}-01-01", f"{year}-12-31"))
        next_year = year + 1
        next_year_filepath = f"entries/{next_year}.json"
        try:
            next_year_file = tools.FilesManagers.get_json(next_year_filepath)
        except FileNotFoundError:
            next_year_file = {'entries': {}, 'open_balance': {}}
        for key, item in balances.data['accounts'].items():
            next_year_file['open_balance'][key] = round(item[0] + item[1] - item[2], 2)
        tools.FilesManagers.save_json(next_year_filepath, next_year_file)
        settings['LOCK'] = year
        tools.FilesManagers.save_json('_settings.json', settings)