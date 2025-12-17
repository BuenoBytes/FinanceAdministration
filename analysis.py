import core
import files
from datetime import datetime
import tools

class Balances:
    def __init__(self, rootfile: core.RootFile, open_dt: str, close_dt: str) -> None:
        self.open_dt = datetime.fromisoformat(open_dt)
        self.close_dt = datetime.fromisoformat(close_dt)
        self.rf = rootfile
        self.ef = files.get_entriesfiles(files.years_select(open_dt, close_dt))
        self.open_dt_str = open_dt
        self.close_dt_str = close_dt

    def process_entries(self) -> object:

        def revexp_cat_match(index: int) -> str:
            if index == 1:
                return 'op'
            elif index == 2:
                return 'fi'
            elif index == 3:
                return 'in'
            
        x = {
            'accounts': {},
            'op': [
                {
                    0: {},
                    1: {},
                    2: {},
                    3: {}},
                {
                    0: {},
                    1: {},
                    2: {},
                    3: {},
                    4: {},
                    5: {},
                    6: {}}],
            'fi': [{0: {}}, {0: {}}],
            'in': [{0: {}}, {0: {}}],
            'ot': [0.0, 0.0]}
        for key, item in self.rf.accounts.items():
            x['accounts'][key] = [self.ef.open.get(key, 0.0), 0.0, 0.0]
        for key, item in self.rf.revenues.items():
            x[revexp_cat_match(item.category)][0][item.sub][key] = [0.0, 0.0] # [value, allowance]
        for key, item in self.rf.expenses.items():
            x[revexp_cat_match(item.category)][1][item.sub][key] = [0.0, 0.0] # [value, allowance]
        for key, item in self.ef.entries.items():
            if item.valid:
                acc = x['accounts'][item.account]
                if item.dt < self.open_dt:
                    if item.flow:
                        acc[0] += item.value
                    else:
                        acc[0] -= item.value
                elif item.dt <= self.close_dt:
                    if item.flow:
                        switch = 0
                    else:
                        switch = 1
                    if item.nature[0] == 2:
                        revexp = self.rf.revenues[item.nature[1]] if switch == 0 else self.rf.expenses[item.nature[1]]
                        index = revexp_cat_match(revexp.category)
                        x[index][switch][revexp.sub][revexp.key][0] += item.value
                    elif item.nature[0] == 0:
                        x['ot'][switch] += item.value
                    elif item.nature[0] == 3:
                        if switch == 0:
                            revexp = self.rf.expenses[item.nature[1]]
                            z = 1
                        else:
                            revexp = self.rf.revenue[item.nature[1]]
                            z = 0
                        index = revexp_cat_match(revexp.category)
                        x[index][z][revexp.sub][revexp.key][1] += item.value
                    acc[switch+1] += item.value
        return x

    def revexp_subcategory_total(self, data: dict[str, float]) -> float: # data = process_entries()['op'|'fi'|'in'][0|1][subcategory key]
        x = 0.0
        for key, item in data.items():
            x += (item[0] - item[1])
        return x          

    def summary(self) -> str:
        data = self.process_entries()

        def format_values(value: float, index: int) -> str:
            if index != 0:
                value = - value
            return f"({-value:,.2f})" if value < 0 else f"{value:,.2f}"

        def build_revexp(branch: str, index: int, subcategory: int) -> tuple[list[str], float]:
            match subcategory:
                case 1:
                    text = 'SALES OF GOODS' if index == 0 else 'SUPPLIES PURCASHES'
                case 2:
                    text = 'SERVICES RENDERING' if index == 0 else 'EMPLOYEE EXPENSES'
                case 3:
                    text = "CONTRACT'S RENDERING" if index == 0 else 'FACILITIES EXPENSES'
                case 4:
                    text = 'TRANSPORT EXPENSES'
                case 5:
                    text = 'INSURANCE EXPENSES'
                case 6:
                    text = 'MARKETING EXPENSES'
                case 0:
                    if branch == 'op':
                        text = 'OTHER OP. REVENUES' if index == 0 else 'OTHER OP. EXPENSES'
                    else:
                        text = 'REVENUES' if index == 0 else 'EXPENSES'
            y = []
            z = 0.0
            for key, item in data[branch][index][subcategory].items():
                name = self.rf.revenues[key].name if index == 0 else self.rf.expenses[key].name
                if item[0] > 0 or item[1] > 0:
                    y += [f"{' '*18}{'('+key+')'+name:.<40} {format_values(item[0], index)}"]
                    z += item[0]
                if item[1] > 0:
                    y += [f"{' '*18}{'Allowance/refunds':>39}  {format_values(-item[1], index)}"]
                    z -= item[1]
            x = []
            if len(y) > 0:
                x += [f"{' '*12}{text}"]
                x += y
            return x, z
        
        x = [
            '='*tools.pt,
            f"From {self.open_dt_str} to {self.close_dt_str}".center(tools.pt),
            '='*tools.pt,
            '',
            self.rf.own.display(),
            '_'*tools.pt,
            '',
            'F I N A N C I A L   S U M M A R Y   R E P O R T'.center(tools.pt),
            '_'*tools.pt,
            '',
            'OPERATIONAL RESULTS']
        y = [f"{' '*6}OPERATIONAL REVENUES"]
        ope = 0.0
        subcategories = [1, 2, 3, 0]
        for item in subcategories:
            processed = build_revexp('op', 0, item)
            y += processed[0]
            ope += processed[1]
        if len(y)>1:
            x += y
        y = [f"{' '*6}OPERATIONAL EXPENSES"]
        subcategories = [1, 2, 3, 4, 5, 6, 0]
        for item in subcategories:
            processed = build_revexp('op', 1, item)
            y += processed[0]
            ope -= processed[1]
        if len(y)>1:
            x += y
        x += [f"{' '*58}{'-'*12}", f"{'= NET OPERATIONAL INCOME: ':.<58} {format_values(ope, 0)}", '', 'FINANCING RESULTS']
        y = [f"{' '*6}FINANCE REVENUES"]
        fin = 0.0
        processed = build_revexp('fi', 0, 0)
        y += processed[0]
        fin += processed[1]
        if len(y)>1:
            x += y
        y = [f"{' '*6}FINANCE EXPENSES"]
        processed = build_revexp('fi', 1, 0)
        y += processed[0]
        fin -= processed[1]
        if len(y)>1:
            x += y
        x += [f"{' '*58}{'-'*12}", f"{'= NET FINANCE INCOME: ':.<58} {format_values(fin, 0)}", '', 'INVESTING RESULTS']   
        y = [f"{' '*6}INVESTING REVENUES"]
        inv = 0.0
        processed = build_revexp('in', 0, 0)
        y += processed[0]
        fin += processed[1]
        if len(y)>1:
            x += y
        y = [f"{' '*6}INVESTING EXPENSES"]
        processed = build_revexp('in', 1, 0)
        y += processed[0]
        inv -= processed[1]
        if len(y)>1:
            x += y
        net = ope + fin + inv
        x += [f"{' '*58}{'-'*12}", f"{'= NET INVESTING INCOME: ':.<58} {format_values(inv, 0)}", '', '-'*tools.pt, f"NET PROFIT (LOSS): {format_values(net, 0)}", '-'*tools.pt, '', f"{'':<35}{'OPEN BALANCE':>15}{'INFLOWS':>15}{'OUTFLOWS':>15}{'CLOSE BALANCE':>15}"]
        for key, item in data['accounts'].items():
            if item[0]!=0 or item[1]!=0 or item[2]!=0:
                z = item[0] + item[1] - item[2]
                x += [f"{key + ' ' + self.rf.accounts[key].name:<34} {format_values(item[0], 0):>15}{format_values(item[1], 0):>15}{format_values(item[2], 0):>15}{format_values(z, 0):>15}"]
        x += ['', '='*tools.pt, 'E N D   O F   T H E   R E P O R T'.center(tools.pt), '='*tools.pt]
        return '\n'.join(x)
