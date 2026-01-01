import json
import os
import core

print('Installing starting.')
rootfile = core.RootFile({
    'own': [['ID_type', 'ID_number'], 'Placeholder', ',,,,,,', ['', '']],
    'accounts': {
        'MOVCASH': ['MOVCASH', 'Cash (movement)', True],
        'SAVCASH': ['SAVCASH', 'Cash (savings)', True],
        'CREDCAR': ['CREDCAR', 'Credit card', False]},
    'revenues': {
        'GRSALES': ['GRSALES', 'Gross sales revenue', True, 'Sales'],
        'GRSERVI': ['GRSERVI', 'Gross services revenue', True, 'Services'],
        'GRCONTR': ['GRCONTR', 'Gross contracts revenue', True, 'Contracts'],
        'INCONTR': ['INCONTR', "Contract's interest", False, 'Financing'],
        'INVARIO': ['INVARIO', 'Interest from various fonts', False, 'Financing'],
        'DIVIDEN': ['DIVIDEN', 'Dividends', False, 'Financing'],
        'ASSETWO': ['ASSETWO', 'Gains on assets write-offs', False, 'Investing']},
    'expenses': {
        'SUPPLIE': ['SUPPLIE', 'Supplies purchases', True, 'Supplies'],
        'EPWAGES': ['EPWAGES', 'Salaries and benefits', True, 'Employee'],
        'EPBENEF': ['EPBENEF', 'Post-employment benefits', True, 'Employee'],
        'FCRENTX': ['FCRENTX', 'Rent', True, 'Facilities'],
        'FCUTILI': ['FCUTILI', 'Utilities', True, 'Facilities'],
        'FCMAINT': ['FCMAINT', 'Maintenance', True, 'Facilities'],
        'TRFUELX': ['TRFUELX', 'Fuel', True, 'Transport'],
        'TRMAINT': ['TRMAINT', 'Maintenance', True, 'Transport'],
        'TRTOLLS': ['TRTOLLS', 'Tolls and parking', True, 'Transport'],
        'TRFREIG': ['TRFREIG', 'Freight charges', True, 'Transport'],
        'TRPEOPL': ['TRPEOPL', 'People transp. charges', True, 'Transport'],
        'ISSALES': ['ISSALES', 'Insurance on sales', True, 'Insurance'],
        'ISPROPE': ['ISPROPE', 'Facilities insurance', True, 'Insurance'],
        'ISVEHIC': ['ISVEHIC', 'Vehicles insurance', True, 'Insurance'],
        'ISVTRAV': ['ISVTRAV', 'Travels insurance', True, 'Insurance'],
        'MKWEBSI': ['MKWEBSI', 'Website hosting', True, 'Marketing'],
        'MKTRAFF': ['MKTRAFF', 'Paid traffic', True, 'Marketing'],
        'MKPROMO': ['MKPROMO', 'Promotional events', True, 'Marketing'],
        'UNIDENT': ['UNIDENT', 'Unidentified expenses', True, 'Others'],
        'INCONTR': ['INCONTR', "Contract's interest", False, 'Financing'],
        'INVARIO': ['INVARIO', 'Interest of various fonts', False, 'Financing'],
        'ASSETWO': ['ASSETWO', 'Loss on assets write-offs', False, 'Investing']}})
ofx_parameters = {
    'MEMO EXAMPLE': ['Other transactions', '']}
with open('_root.json', 'w', encoding='utf-8') as f:
    json.dump(rootfile.to_dict(), f, indent=4, ensure_ascii=False)
with open('_ofxparameters.json', 'w', encoding='utf-8') as f:
    json.dump(ofx_parameters, f, indent=4, ensure_ascii=False)
os.makedirs('entries')
print('Installed with success.')
