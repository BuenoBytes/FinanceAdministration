# python -m streamlit run app.py

# STARTERS AND INITIAL CHECK ----------------------------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import time
import os
import traceback

check_code = [item for item in ['core.py', 'tools.py','_settings.json', '_root.json'] if not os.path.exists(item)]
if check_code:
    missing = '\n     '.join(check_code)
    st.error(f"Missing core files:\n   {missing}\nThe system cannot start. Check the github for missing py files and (Re)Install folders and '_x.json' files with 'install.py'.")
    st.stop()

import core
import tools
import ofx

@st.cache_data
def load_root() -> core.RootFile:
    try:
        x: core.RootFileSchema = tools.FilesManagers.get_json('_root.json')
        return core.RootFile(x)
    except Exception as e:
        st.error(f"!!! Fatal error starting the system core:\n{e}\n{traceback.format_exc()}")
        st.stop()

rf = load_root()


# FRONT-END FUNCTIONS -----------------------------------------------------------------------------------------------------

def save_root(rf: core.RootFile) -> None:
    tools.FilesManagers.save_json('_root.json', rf.to_dict())
    st.success('Saved with success! Please wait while the system reloads...')
    st.cache_data.clear()
    st.cache_resource.clear()
    time.sleep(1)
    st.rerun()

def save_entries(ef: core.EntriesFile) -> None:
    tools.FilesManagers.save_json(os.path.join('entries', f"{ef.year}.json"), ef.to_dict())
    st.success('Saved with success! Please wait while the system reloads...')
    time.sleep(1)
    st.rerun()
                
def entity_details(entity: core.Entity) -> core.Entity:
    st.subheader('Business Details')
    
    st.write("**Identification**")

    max_id = int(core.Entity.settings('ID ITEMS MAX LENGTH'))
    id_type = st.text_input(label='Document type: ', value= entity.id_info[0], max_chars= max_id)
    id_number = st.text_input('Document number: ', value= entity.id_info[1], max_chars= max_id)
    name = st.text_input('Registered name: ', value= entity.name, max_chars= core.Entity.settings('NAME MAX LENGTH'))

    st.divider()

    st.write("**Address and Contact Information**")

    max_contact = core.Entity.settings('CONTACT ITEMS MAX LENGTH')
    address = st.text_input('📍 Address: ', value= entity.address, max_chars= core.Entity.settings('ADDRESS MAX LENGTH'), help= 'Use commas.')
    email = st.text_input('✉ Email: ', value= entity.contact_info[0], max_chars= max_contact)
    phone = st.text_input('📞 Phone: ', value= entity.contact_info[1], max_chars= max_contact)

    return core.Entity((id_type, id_number), name, address, (email, phone))

def accounts_list(rf: core.RootFile) -> None:
    accounts = rf.filter_accounts()
    st.subheader('Registered accounts list')
    def body(branch: str) -> None:
        c1, c2, c3, c4 = st.columns([1,2,1,1])
        with c1:
            st.caption('🗝 Key')
        with c2:
            st.caption('＃ Name')
        with c3:
            st.caption('</> Nature')
        for key in accounts[branch]:
            c1, c2, c3, c4 = st.columns([1,2,1,1])
            acc = rf.accounts[key]
            with c1:
                st.write(key)
            with c2:
                nname = st.text_input('', value= acc.name, max_chars= core.Account.settings('NAME MAX LENGTH'), key= f"name_{acc.key}", label_visibility="collapsed")
            with c3:
                nnature = st.checkbox('', value= acc.nature, key= f"nature_{acc.key}")
            with c4:
                if st.button('📝 Save', use_container_width=True, key=f"button_{key}"):
                    try:
                        obj = [key, nname, nnature]
                        rf.edit('accounts', obj)
                        save_root(rf)
                    except Exception as e:
                        st.error(f"Saving failed: {e}\n{traceback.format_exc()}")
    st.write('**Cash accounts**')
    body('cash')
    st.divider()
    st.write('**Credit card accounts**')
    body('credit_cards')

def revexp_list(rf: core.RootFile, switch: bool) -> None:
    operational_categories = core.RevExp.settings('OPREV CATEGORIES') if switch else core.RevExp.settings('OPEXP CATEGORIES')
    nonoperational_categories = core.RevExp.settings('NON-OP CATEGORIES')
    selection = rf.filter_revexp(switch)
    string = 'revenues' if switch else 'expenses'
    st.subheader(f"Registered {string} list")
    def body(branch: str) -> None:
        c1, c2, c3, c4, c5 = st.columns([1,2,1,1,1])
        with c1:
            st.caption('🗝 Key')
        with c2:
            st.caption('＃ Name')
        with c3:
            st.caption('🛠 Operational')
        with c4:
            st.caption('🏷 Category')
        for key, item in selection[branch].items():
            c1, c2, c3, c4, c5 = st.columns([1,2,1,1,1])
            with c1:
                st.write(key)
            with c2:
                nname = st.text_input('', value= item.name, max_chars= core.RevExp.settings('NAME MAX LENGTH'), key= f"name_{item.key}_{switch}", label_visibility= 'collapsed')
            with c3:
                noperational = st.checkbox('', value= item.operational, label_visibility= 'collapsed', key= f"operational_{item.key}_{switch}")
            with c4: 
                if noperational:
                    original_category = operational_categories.index(item.category) if item.category in operational_categories else 0
                    ncategory = st.selectbox('', operational_categories, index= original_category, label_visibility='collapsed', key= f"category_{item.key}_{switch}")
                else:
                    original_category = nonoperational_categories.index(item.category) if item.category in nonoperational_categories else 0
                    ncategory = st.selectbox('', nonoperational_categories, index= original_category, label_visibility='collapsed', key= f"category_{item.key}_{switch}")
            with c5:
                if st.button('📝 Save', use_container_width=True, key=f"button_{key}_{switch}"):
                    try:
                        obj = [key, nname, noperational, ncategory]
                        revexp_branch_str = 'revenues' if switch else 'expenses'
                        rf.edit(revexp_branch_str, obj)
                        save_root(rf)
                    except Exception as e:
                        st.error(f"Saving failed: {e}\n{traceback.format_exc()}")
    st.write(f"**Operational {string}**")
    body('operational')
    st.divider()
    st.write(f"**Non-operational {string}**")
    body('financing')
    body('investing')

def new_revexp(rf: core.RootFile, switch: bool) -> None:
    string = 'revenue' if switch else 'expense'
    st.write(f"**New {string}**")
    key = st.text_input('🗝 Key: ', max_chars= core.RevExp.settings('KEY LENGTH'),help="Has to have 7 digits.\nIt has to be an unused {string} key.", key=f"key_{switch}")
    name = st.text_input('＃ Name: ', max_chars= core.RevExp.settings('NAME MAX LENGTH'), key=f"name_{switch}")
    operational = st.checkbox('🛠 Is it Operational? ', value= True, key=f"operational_{switch}")
    if operational:
        categories = 'OPREV' if switch else 'OPEXP'
    else:
        categories = 'NON-OP'
    categories = core.RevExp.settings(f"{categories} CATEGORIES")
    category = st.selectbox('🏷 Category: ', categories, index= 0, key=f"category_{switch}")
    st.divider()
    if st.button('📝 Save', use_container_width=True, key=f"button_{switch}"):
        try:
            obj = [key, name, operational, category]
            revexp_branch_str = 'revenues' if switch else 'expenses'
            rf.new(revexp_branch_str, obj)
            save_root(rf)
            st.success(f"Saved with success!")
        except Exception as e:
            st.error(f"Saving failed: {e}\n{traceback.format_exc()}")

def entries_dataframe(ef: core.EntriesFile, rf: core.RootFile) -> None:
    if not ef.entries:
        st.info("No entries found.")
    else:
        df_entries = pd.DataFrame([
            {
                "Status": "🟢" if item.valid else "🔴",
                "Key": item.key,
                "Account": item.account,
                "Counterparty": item.nature[1],
                "Date": item.dt.date(),
                "Value": item.value if item.flow else -item.value,
                "Notes": item.notes
            } for key, item in ef.entries.items()])
        st.data_editor(df_entries,
            column_config={
            "Status": st.column_config.TextColumn(width="small"),
            "Key": st.column_config.TextColumn(width="small"),
            "Account": st.column_config.TextColumn(width="small"),
            "Counterparty": st.column_config.TextColumn(width="small"),
            "Date": st.column_config.DateColumn(format="YYYY-MM-DD"),
            "Value": st.column_config.NumberColumn(format="%.2f", help="Negative values are outflows."),
            "Notes": st.column_config.TextColumn(width="large")
            }, disabled=True, hide_index=True)

def record_entry(ef: core.EntriesFile, rf: core.RootFile, new: bool) -> None:
    natures = core.Entry.settings('NATURES')
    accounts_list = list(rf.accounts.keys())
    revenues_list = list(rf.revenues.keys())
    expenses_list = list(rf.expenses.keys())
    key = '0'
    if not new:
        key = st.text_input('Entry key: ')
        if key in ef.entries.keys():
            entry = ef.entries[key]
            st.divider()
        else:
            st.error(f"Key {key} not found.")
            return None
    else:
        entry = core.Entry(key, accounts_list[0], True, (natures[0], ''), '2000-01-01', 0.0, '', True)
    st.write(f"🗝 Key: {entry.key}")
    naccount = st.selectbox('🏛 Account: ', accounts_list, index= accounts_list.index(entry.account))
    st.caption(f"{rf.accounts[naccount].display()}")
    nflow = st.checkbox('↳↰ Flow (Check if it is an inflow, uncheck if it is an outflow): ', value= entry.flow, key=f"flow_{new}")
    nnature0 = st.selectbox('</> Nature: ', natures, index= natures.index(entry.nature[0]), key=f"nature0_{new}")
    nnature1 = ''
    if nnature0 == natures[1]:
        original_index = accounts_list.index(entry.nature[1]) if entry.nature[1] in accounts_list else 0
        nnature1 = st.selectbox('</>* Counter account: ', accounts_list, index= original_index, key=f"nature1_{new}")
        st.caption(f"{rf.accounts[nnature1].display()}")
    elif (nnature0 == natures[2] and nflow is True) or (nnature0 == natures[3] and nflow is False):
        original_index = revenues_list.index(entry.nature[1]) if entry.nature[1] in revenues_list else 0
        nnature1 = st.selectbox('</>* Revenue: ', revenues_list, index= original_index, key=f"nature1_{new}")
        st.caption(f"{rf.revenues[nnature1].display()}")
    elif (nnature0 == natures[2] and nflow is False) or (nnature0 == natures[3] and nflow is True):
        original_index = expenses_list.index(entry.nature[1]) if entry.nature[1] in expenses_list else 0
        nnature1 = st.selectbox('</>* Expense: ', expenses_list, index= original_index, key=f"nature1_{new}")
        st.caption(f"{rf.expenses[nnature1].display()}")
    ndate = st.date_input(label= '🗓 Date[ISO]: ', value= entry.dt, format= 'YYYY-MM-DD', max_value= tools.today())
    nvalue = st.number_input(label= '💲 Value: ', min_value= 0.0, value= entry.value, step= 0.01, format= '%.2f')
    nnotes = st.text_input('📋 Notes', value= entry.notes)
    nvalid = st.checkbox('🟢 Status(Check if valid, uncheck if invalid): ', value= entry.valid, key=f"valid_{new}")
    st.divider()
    if nnature0 == "Transaction btw accounts" and new:
        if st.button("Create Counterpart Entry", use_container_width=True, key=f"counterpart"):
            try:
                counter_entry = core.Entry('0', nnature1, not nflow, (nnature0, naccount), ndate.isoformat(), float(nvalue), f"(Counterpart of entry {key}) {nnotes}", nvalid)
                ef.new(counter_entry)
                st.success(f"Counterpart entry created with success! File not saved yet!")
            except Exception as e:
                st.error(f"Creating counterpart failed: {e}\n{traceback.format_exc()}")
        st.divider()
    if st.button('📝 Save', use_container_width=True, key=f"save_{new}"):
        try:
            obj = core.Entry(key, naccount, nflow, (nnature0, nnature1), ndate.isoformat(), float(nvalue), nnotes, nvalid)
            if new:
                ef.new(obj)
            else:
                ef.edit(obj, key)
            save_entries(ef)
        except Exception as e:
            st.error(f"Saving failed: {e}\n{traceback.format_exc()}")

def income_st(balances: core.Balances) -> None:
    st.markdown("""
        <style>
        .report-font { font-family: 'Source Code Pro', monospace; font-size: 14px; }
        /* Classe para a linha separadora sutil que substitui o divider */
        .total-header {
            border-bottom: 2px solid #333; 
            margin-bottom: 10px;
            margin-top: 5px;
        }
        </style>""", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Income Statement</h2>", unsafe_allow_html=True)
    st.markdown("<div class='total-header'></div>", unsafe_allow_html=True)    
    def render_block(data_structure):
        descriptions, values, block_total = data_structure
        for desc, val in zip(descriptions, values):
            col1, col2 = st.columns([3, 1])
            with col1:
                if "**" in desc:
                    st.markdown(f"{desc}")
                else:
                    st.markdown(f"<div class='report-font'>{desc}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='report-font' style='text-align: right;'>{val}</div>", unsafe_allow_html=True)
    operational_data = balances.income_st_structure(True)
    render_block(operational_data)
    st.markdown("<div class='total-header'></div>", unsafe_allow_html=True)
    nonop_data = balances.income_st_structure(False)
    render_block(nonop_data)
    st.markdown("<div class='total-header'></div>", unsafe_allow_html=True)
    net_total = operational_data[2] + nonop_data[2]
    c1, col_val = st.columns([3, 1])
    with c1:
        st.markdown("***= Net Income / Loss***")
    with col_val:
        formatted_net = tools.format_value(net_total, True)
        st.markdown(f"<div class='report-font' style='text-align: right;'>{formatted_net}</div>", unsafe_allow_html=True)
    st.markdown("<div style='border-bottom: 3px double #333;'></div>", unsafe_allow_html=True)

def flow_summary(balances: core.Balances) -> None:
    st.markdown("""
        <style>
        .flow-font { font-family: 'Source Code Pro', monospace; font-size: 13px; }
        .header-row { 
            font-weight: bold; 
            border-bottom: 2px solid #333; 
            margin-bottom: 10px; 
            padding-bottom: 5px;
        }
        .account-row { border-bottom: 1px solid #eee; padding: 4px 0; }
        .val-align { text-align: right; }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Accounts Flow Summary</h3>", unsafe_allow_html=True)
    h1, h2, h3 = st.columns([3, 1, 1], gap="small")
    with h1:
        st.markdown("<div class='header-row'>Account Description</div>", unsafe_allow_html=True)
    with h2:
        st.markdown("<div class='header-row val-align'>Opening</div>", unsafe_allow_html=True)
    with h3:
        st.markdown("<div class='header-row val-align'>Closing</div>", unsafe_allow_html=True)
    for key, item in balances.data['accounts'].items():
        opening = item[0]
        closing = item[0] + item[1] - item[2]
        if opening != 0.0 or item[1] != 0.0 or item[2] != 0.0:
            c1, c2, c3 = st.columns([3, 1, 1], gap="small")            
            with c1:
                acc_name = balances.rf.accounts[key].display()
                st.markdown(f"<div class='account-row flow-font'>{acc_name}</div>", unsafe_allow_html=True)            
            with c2:
                val_open = tools.format_value(opening, True)
                st.markdown(f"<div class='account-row flow-font val-align'>{val_open}</div>", unsafe_allow_html=True)            
            with c3:
                val_close = tools.format_value(closing, True)
                st.markdown(f"<div class='account-row flow-font val-align'>{val_close}</div>", unsafe_allow_html=True)
    st.markdown("<div style='border-top: 2px solid #333; margin-top: 5px;'></div>", unsafe_allow_html=True)
    
def date_interval() -> tuple[str, str]:
    x = st.date_input(label='Type the open date of the report: ', format='YYYY-MM-DD').isoformat()
    y = st.date_input(label='Type the close date of the report: ', format='YYYY-MM-DD').isoformat()
    return x, y

def import_ofx_file(ef: core.EntriesFile) -> None:
    natures = core.Entry.settings('NATURES')
    accounts_list = list(rf.accounts.keys())
    revenues_list = list(rf.revenues.keys())
    expenses_list = list(rf.expenses.keys())
    parameters = tools.FilesManagers.get_json('_ofxparameters.json')
    st.subheader('Import OFX file')
    ofx_file = st.file_uploader('Upload the OFX file to import: ', type=['ofx'])
    if ofx_file is not None:
        account_key = st.selectbox('Select the account to import the transactions to: ', list(rf.accounts.keys()), key= 'ofx_account_key')
        st.divider()
        if st.button('⚙️ Process OFX file', use_container_width=True, key= 'process_ofx_file'):
            try:
                parsed_ofx = ofx.inital_proccess(ofx_file, parameters, account_key)
                st.success(f"OFX file processed successfully!\nNumber of unresolved entries: {len(parsed_ofx['unresolved'])}")
            except Exception as e:
                st.error(f"Processing failed: {e}\n{traceback.format_exc()}")
    if os.path.exists('temp_ofx_parsed.json'):
        parsed_ofx = tools.FilesManagers.get_json('temp_ofx_parsed.json')
        if parsed_ofx['unresolved']:
            with st.expander("🔧 Fix unresolved entries", expanded=True):
                st.info(f"**Resolving item 1 of {len(parsed_ofx['unresolved'])}**")
                entry_obj = core.Entry(*parsed_ofx['unresolved'][0])
                st.write(f"🏛 Account: {entry_obj.account} --> {rf.accounts[entry_obj.account].display()}")
                st.write(f"↳↰ Flow: {'Inflow' if entry_obj.flow else 'Outflow'}")
                st.write(f"🗓 Date[ISO]: {entry_obj.dt.isoformat()}")
                st.write(f"💲 Value: {tools.format_value(entry_obj.value, True)}")
                st.write(f"📋 Notes: {entry_obj.notes}")
                st.divider()
                nature0 = st.selectbox('</> Nature: ', natures, key= f"nature0_ofx_{entry_obj.key}")
                nature1 = ''
                if nature0 == natures[1]:
                    nature1 = st.selectbox('</>* Counter account: ', accounts_list, key=f"nature1_ofx{entry_obj.key}")
                    st.caption(f"{rf.accounts[nature1].display()}")
                elif (nature0 == natures[2] and entry_obj.flow is True) or (nature0 == natures[3] and entry_obj.flow is False):
                    original_index = revenues_list.index(entry_obj.nature[1]) if entry_obj.nature[1] in revenues_list else 0
                    nature1 = st.selectbox('</>* Revenue: ', revenues_list, index= original_index, key=f"nature1_ofx{entry_obj.key}")
                    st.caption(f"{rf.revenues[nature1].display()}")
                elif (nature0 == natures[2] and entry_obj.flow is False) or (nature0 == natures[3] and entry_obj.flow is True):
                    original_index = expenses_list.index(entry_obj.nature[1]) if entry_obj.nature[1] in expenses_list else 0
                    nature1 = st.selectbox('</>* Expense: ', expenses_list, index= original_index, key=f"nature1_ofx{entry_obj.key}")
                    st.caption(f"{rf.expenses[nature1].display()}")
                if st.button('Save this parameter assignment', key= f"save_parameter_ofx_{entry_obj.key}"):
                    try:
                        ofx.new_parameter(entry_obj, rf, parameters, (nature0, nature1), True)
                        tools.FilesManagers.save_json('_ofxparameters.json', parameters)
                        st.success("Parameter assignment saved!")
                    except Exception as e:
                        st.error(f"Saving failed: {e}\n{traceback.format_exc()}")
                if st.button('Resolve entry and continue', key= f"resolve_ofx_{entry_obj.key}", use_container_width=True):
                    ofx.new_parameter(entry_obj, rf, parameters, (nature0, nature1), False)
                    parsed_ofx['resolved'].append(entry_obj.to_list())
                    parsed_ofx['unresolved'].pop(0)
                    ofx.check_unresolved(parsed_ofx, parameters)
                    tools.FilesManagers.save_json('temp_ofx_parsed.json', parsed_ofx)
                    st.rerun()
        else:
            st.success("All entries have been resolved!")
            if st.button('📥 Import entries', use_container_width=True):
                try:
                    ofx.import_ofx(parsed_ofx, ef)
                    os.remove('temp_ofx_parsed.json')
                    save_entries(ef)
                except Exception as e:
                    st.error(f"Importing failed: {e}\n{traceback.format_exc()}")
                    
# FRONT-END STRUCTURE------------------------------------------------------------------------------------------------------

st.sidebar.title('Business Manegement System')
st.sidebar.caption('A study project')
with st.sidebar.expander('+ About'):
    st.caption('Status: In development')
    st.caption('ianbueno.work@gmail.com')
    st.caption('GitHub: BuenoBytes')

st.sidebar.divider()

menu = st.sidebar.radio('Modules:', ['💼 Business info', '🏛 Accounts', '💰 Revenues/expenses', '📜 Entries', '📈 Reports', '🔒 Lock a year'], index=0)

if menu == '💼 Business info':
    tabs = st.tabs(['📝 Edit & View'])    
    with tabs[0]:
        try:
            obj = entity_details(rf.own)
            if st.button('📝 Save', use_container_width=True):
                rf.own = obj
                save_root(rf)                
        except Exception as e:
            st.error(f"An error occurred: {e}\n{traceback.format_exc()}")

elif menu == '🏛 Accounts':
    tabs = st.tabs(['☰ List', '✚ New'])
    with tabs[0]:
        accounts_list(rf)
    with tabs[1]:
        st.write('**New account**')
        key = st.text_input('🗝 Key: ', max_chars= core.Account.settings('KEY LENGTH'), help='The key length has to be 7.\nIt has to be a unused account key.')
        name = st.text_input('＃ Name', max_chars= core.Account.settings('NAME MAX LENGTH'))
        nature = st.checkbox('</> Nature', help = "Check if it is a cash account, don't if it is a credit card account.")
        st.divider()
        if st.button('📝 Save', use_container_width=True):
            try:
                obj = [key, name, nature]
                rf.new('accounts', obj)
                st.success('Saved with success!')
                time.sleep(1)
                save_root(rf)
            except Exception as e:
                st.error(f"Saving failed: {e}\n{traceback.format_exc()}")

elif menu == '💰 Revenues/expenses':
    tabs = st.tabs(['💲☰ Revenues list', '💲✚ New revenue','💸☰ Expenses list', '💸✚ New expense'])
    with tabs[0]:
        revexp_list(rf, True)
    with tabs[2]:
        revexp_list(rf, False)
    with tabs[1]:
        new_revexp(rf, True)
    with tabs[3]:
        new_revexp(rf, False)

elif menu == '📜 Entries':
    year = st.number_input(label= 'Type the year that you desire to manipulate: ' , min_value= 0, step=1, value= core.settings['LOCK']+1)
    if year <= core.settings['LOCK']:
        st.warning(f"Year {year} is locked and cannot be edited or receive new data.")
    try:
        ef: core.EntriesFileSchema = tools.FilesManagers.get_json(os.path.join('entries', f"{year}.json"))
    except FileNotFoundError:
        ef: core.EntriesFileSchema = {'entries': {}, 'open_balance': {}}
    ef_file = core.EntriesFile(ef, rf, year)
    tabs = st.tabs(['☰ List', '📝 Edit & View', '✚ New', '📥 Import from a ofx file'])
    with tabs[0]:
        st.write('**Entries on the file**')
        entries_dataframe(ef_file, rf)
    with tabs[1]:
        st.write('**Edit and view a specific entry**')
        record_entry(ef_file, rf, False)
    with tabs[2]:
        st.write('**Record a new entry**')
        record_entry(ef_file, rf, True)
    with tabs[3]:
        import_ofx_file(ef_file)

elif menu == '📈 Reports':
    tabs = st.tabs(['🚩 Summary'])
    with tabs[0]:
        interval = date_interval()
        balances = core.BalancesBase.build_ef(rf, interval[0], interval[1])
        balances = core.Balances.process_entries(balances)
        st.divider()
        income_st(balances)
        flow_summary(balances)

elif menu == '🔒 Lock a year':
    st.warning("⚠️ Locking a year is an irreversible action. Make sure you have backed up all necessary data before proceeding.")
    st.warning("⚠️ Locks should be created yearly after closing the books for the year and before starting to record data for the new year.")
    year = st.number_input(label='Type the year that you desire to lock: ', min_value=0, step=1)
    if st.button('🔒 Lock'):
        try:
            core.lock_year(year, rf)
            st.success(f"Year {year} locked successfully.")
        except Exception as e:
            st.error(f"Failed to lock year {year}: {e}")