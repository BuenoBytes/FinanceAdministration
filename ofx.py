from ofxparse import OfxParser
import json
import core

def inital_proccess(ofx_file, parameters: dict, account_key: str) -> dict:
    ofx_obj = OfxParser.parse(ofx_file)   
    unresolved_transactions = []
    resolved_transactions = []
    i = 0
    account = ofx_obj.account # type: ignore
    statement = account.statement    
    for transaction in statement.transactions:
        flag = True
        if transaction.amount < 0:
            flow = False
            value = - transaction.amount
        else:
            flow = True
            value = transaction.amount
        memo_value = transaction.memo or transaction.payee or ""       
        if not memo_value.strip() or memo_value not in parameters:
            flag = False
            param = parameters['MEMO EXAMPLE']
        else:
            param = parameters[memo_value]
        entry_obj = core.Entry(f"{i}", account_key, flow, (param[0], param[1]), transaction.date.isoformat(), value, memo_value, True)       
        if flag:
            resolved_transactions.append(entry_obj.to_list())
        else:
            unresolved_transactions.append(entry_obj.to_list())
        i += 1       
    x = {
        "account_key": account_key,
        "resolved": resolved_transactions,
        "unresolved": unresolved_transactions
    }    
    with open('temp_ofx_parsed.json', 'w', encoding='utf-8') as f:
        json.dump(x, f, ensure_ascii=False, indent=4)
    return x

def new_parameter(entry_obj: core.Entry, rf: core.RootFile, parameters_dict: dict, assigned_parameter: tuple[str, str], save: bool) -> None:
    if assigned_parameter[0] == "Other transactions":
        parameters_dict[entry_obj.notes] = ["Other transactions", ""]
    elif assigned_parameter[0] == "Transaction btw accounts":
        if assigned_parameter[1] not in rf.accounts.keys():
            raise ValueError(f"The assigned account key {assigned_parameter[1]} does not exist in the system.")
    elif entry_obj.flow:
        if assigned_parameter[0] == "Direct revenue/expense" and assigned_parameter[1] not in rf.revenues.keys():
            raise ValueError(f"The assigned revenue key {assigned_parameter[1]} does not exist in the system.")
        elif assigned_parameter[0] == "Revenue/expense refund" and assigned_parameter[1] not in rf.expenses.keys():
            raise ValueError(f"The assigned expense key {assigned_parameter[1]} does not exist in the system.")
    elif not entry_obj.flow:
        if assigned_parameter[0] == "Direct revenue/expense" and assigned_parameter[1] not in rf.expenses.keys():
            raise ValueError(f"The assigned expense key {assigned_parameter[1]} does not exist in the system.")
        elif assigned_parameter[0] == "Revenue/expense refund" and assigned_parameter[1] not in rf.revenues.keys():
            raise ValueError(f"The assigned revenue key {assigned_parameter[1]} does not exist in the system.")
    if save:
        parameters_dict[entry_obj.notes] = [assigned_parameter[0], assigned_parameter[1]]
    entry_obj.nature = assigned_parameter

def import_ofx(parsed_ofx: dict, ef: core.EntriesFile) -> None:
    while parsed_ofx['resolved']:
        entry = parsed_ofx['resolved'][0]
        try:
            entry_obj = core.Entry(*entry)
            ef.new(entry_obj)
            parsed_ofx['resolved'].pop(0)
        except Exception as e:
            with open('temp_ofx_parsed.json', 'w', encoding='utf-8') as f:
                json.dump(parsed_ofx, f, ensure_ascii=False, indent=4)
            raise e

def check_unresolved(parsed_ofx: dict, parameters_dict: dict) -> None:
    still_unresolved = []
    for entry in parsed_ofx['unresolved']:
        entry_obj = core.Entry(*entry)
        if entry_obj.notes in parameters_dict:
            assigned_parameter = parameters_dict[entry_obj.notes]
            entry_obj.nature = (assigned_parameter[0], assigned_parameter[1])
            parsed_ofx['resolved'].append(entry_obj.to_list())
        else:
            still_unresolved.append(entry)
    parsed_ofx['unresolved'] = still_unresolved