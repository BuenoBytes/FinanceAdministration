import core
import tools
import files
import os
import analysis

def gen_output(data: str) -> None:
    with open(os.path.join('in_out', f"output.txt"),'w', encoding='utf-8') as f:
        f.write(data)

print('Wellcome to my simple finnancing and admnistration system. An study project.')
rootfile = files.get_rootfile()
while True:
    match tools.SpInputs("Choose one module [E to exit]: \n [ 1 ] Accounts and revenues/expenses \n [ 2 ] Entities \n [ 3 ] Entries \n [ R ] Reports \n").withoptions(['E', 'R', '1', '2', '3']):
        case 'E':
            print('Bye!')
            break
        case '1':
            manager = core.RootManager(rootfile)
            while True:
                match tools.SpInputs("Choose an action [R to return | S to save]: \n [ 1 ] New account \n [ 2 ] Edit account \n [ 3 ] New revenue \n [ 4 ] Edit revenue \n [ 5 ] New expense \n [ 6 ] Edit expense").withoptions(['R', 'S', '1', '2', '3', '4', '5', '6']):
                    case 'R':
                        break
                    case 'S':
                        files.savejson(rootfile, '_root.json')
                    case '1':
                        manager.new_account()
                    case '2':
                        manager.edit_account()
                    case '3':
                        manager.new_revexp(True)
                    case '4':
                        manager.edit_revexp(True)
                    case '5':
                        manager.new_revexp(False)
                    case '6':
                        manager.edit_revexp(False)
        case '2':
            entitiesfile = files.get_entitiesfiles()
            manager = core.EntitiesManager(rootfile, entitiesfile)
            while True:
                match tools.SpInputs("Choose an action [R to return | S to save]: \n [ 1 ] New \n [ 2 ] Edit \n").withoptions(['R', 'S', '1', '2']):
                    case 'R':
                        break
                    case 'S':
                        files.savejson(rootfile, '_root.json')
                        files.savejson(entitiesfile, '_entities.json')
                    case '1':
                        manager.new()
                    case '2':
                        manager.edit()
        case '3':
            year = tools.SpInputs("Type the year that you desire to manage: ").int_number()
            path = os.path.join('entries', f"{year}.json")
            if os.path.exists(path):
                entriesfile = files.get_entriesfiles([year])
            else:
                entriesfile = core.EntriesFile({
                    'entries': {},
                    'open': {}})
            manager = core.EntriesManager(rootfile, entriesfile, year)
            while True:
                match tools.SpInputs("Choose an action [R to return | S to save]: \n [ 1 ] New \n [ 2 ] Edit \n [ 3 ] Lock year \n").withoptions(['R', 'S', '1', '2']):
                    case 'R':
                        break
                    case 'S':
                        files.savejson(entriesfile, path)
                    case '1':
                        if rootfile.lock is None or rootfile.lock < year:
                            manager.new()
                        else:
                            print('This year is locked, therefore cannot receive new entries.')
                    case '2':
                        if rootfile.lock is None or rootfile.lock < year:
                            manager.edit()
                        else:
                            print("This year is locked, therefore have it's entries edited.")
                    case '3':
                        if tools.SpInputs('Do you really desire to lock the year? Locked years cannot receive new entries neither have it edited.\nEach year has to be locked when ended.').yesorno():
                            start = f"{year}-01-01"
                            end = f"{year}-12-31"
                            processed_accounts = analysis.Balances(rootfile, start, end)['accounts']
                            processed_accounts = {key: (item[0] + item[1] - item[2]) for key, item in processed_accounts.items()}
                            following_path = os.path.join('entries', f"{year+1}.json")
                            if os.path.exists(following_path):
                                following_file = files.get_entriesfile([year+1])
                                following_file.open = processed_accounts
                            else:
                                following_file = core.EntriesFile({
                                    'entries': {},
                                    'open': processed_accounts})
                            files.savejson(following_file, following_path)
                            rootfile.lock = year
                            print(f"{year} locked with success.")
        case 'R':
            while True:
                match tools.SpInputs("Choose a report [R to return]: \n [ 1 ] Financial summary \n").withoptions(['R', '1']):
                    case 'R':
                        break
                    case '1':
                        x = analysis.Balances(rootfile, tools.SpInputs('Report open date:').dt(), tools.SpInputs('Report close date:').dt()).summary()
                        gen_output(x)
