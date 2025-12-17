import json
import os
from tools import SpInputs
import core

print("Wellcome to the system modularized installer. It creates some files and architeture needed for everything to work.")
while True:
    match SpInputs("Choose the corresponding index of the module that you desire to install [C to close]: \n [ 1 ] Core (Files: root, entities / Folders: entries, in_out) \n").withoptions(['C', '1']):
        case 'C':
            print("Installer closed. Bye!")
            break
        case '1':
            print('Insert data about the entity that will be the pilot of the system.')
            rootfile = core.RootFile({
                'own': [
                    '$'.join((input('Type the ID docuemnt type: ').strip().upper(), input('Dcoument number: ').strip())),
                    input("Entity's name: ").strip(),
                    core.build_adress(),
                    (input('Phone number: ').strip(), input('Email: ').strip())],
                'accounts': {
                    'MOVCASH': ['MOVCASH', 'Cash (movement)', True],
                    'SAVCASH': ['SAVCASH', 'Cash (savings)', True],
                    'CREDCAR': ['CREDCAR', 'Credit card', False]},
                'revenues': {
                    'GRSALES': ['GRSALES', 'Gross sales revenue', True, 1, 1],
                    'GRSERVI': ['GRSERVI', 'Gross services revenue', True, 1, 2],
                    'GRCONTR': ['GRCONTR', 'Gross contracts revenue', True, 1, 3],
                    'INCONTR': ['INCONTR', "Contract's interest", True, 2, 0],
                    'INVARIO': ['INVARIO', 'Interest from various fonts', True, 2, 0],
                    'DIVIDEN': ['DIVIDEN', 'Dividends', True, 2, 0],
                    'ASSETWO': ['ASSETWO', 'Gains on assets write-offs', True, 3, 0]},
                'expenses': {
                    'SUPPLIE': ['SUPPLIE', 'Supplies purchases', False, 1, 1],
                    'EPWAGES': ['EPWAGES', 'Salaries and benefits', False, 1, 2],
                    'EPBENEF': ['EPBENEF', 'Post-employment benefits', False, 1, 2],
                    'FCRENTX': ['FCRENTX', 'Rent', False, 1, 3],
                    'FCUTILI': ['FCUTILI', 'Utilities', False, 1, 3],
                    'FCMAINT': ['FCMAINT', 'Maintenance', False, 1, 3],
                    'TRFUELX': ['TRFUELX', 'Fuel', False, 1, 4],
                    'TRMAINT': ['TRMAINT', 'Maintenance', False, 1, 4],
                    'TRTOLLS': ['TRTOLLS', 'Tolls and parking', False, 1, 4],
                    'TRFREIG': ['TRFREIG', 'Freight charges', False, 1, 4],
                    'TRPEOPL': ['TRPEOPL', 'People transp. charges', False, 1, 4],
                    'ISSALES': ['ISSALES', 'Insurance on sales', False, 1, 5],
                    'ISPROPE': ['ISPROPE', 'Facilities insurance', False, 1, 5],
                    'ISVEHIC': ['ISVEHIC', 'Vehicles insurance', False, 1, 5],
                    'ISVTRAV': ['ISVTRAV', 'Travels insurance', False, 1, 5],
                    'MKWEBSI': ['MKWEBSI', 'Website hosting', False, 1, 6],
                    'MKTRAFF': ['MKTRAFF', 'Paid traffic', False, 1, 6],
                    'MKPROMO': ['MKPROMO', 'Promotional events', False, 1, 6],
                    'UNIDENT': ['UNIDENT', 'Unidentified expenses', False, 1, 0],
                    'INCONTR': ['INCONTR', "Contract's interest", False, 2, 0],
                    'INVARIO': ['INVARIO', 'Interest of various fonts', False, 2, 0],
                    'ASSETWO': ['ASSETWO', 'Loss on assets write-offs', False, 3, 0]},
                'lock': None})
            entitiesfile = core.EntitiesFile({'$': ['$', 'Non identified', ['','','','','','','',], ('', '')]})
            with open('_root.json', 'w', encoding='utf-8') as f:
                json.dump(rootfile.to_dict(), f, indent=4, ensure_ascii=False)
            with open('_entities.json', 'w', encoding='utf-8') as f:
                json.dump(entitiesfile.to_dict(), f, indent=4, ensure_ascii=False)
            os.makedirs('entries')
            os.makedirs('in_out')
            print('Core module installed with success.')
