from SerializeFile import *
from Customer import *
import PySimpleGUI as sg
import re
import operator

fCustomer = 'Customer.json'
lCustomer = []
pattern_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
pattern_ID = r"\d{3}"
pattern_phone = r"\d{3}-\d{6}"

def addCustomer(l_Customer, t_CustomerInterfaz, oCustomer, fCustomer):
    last_pos = l_Customer[-1].posFile if l_Customer else 0
    new_pos = last_pos + 1
    oCustomer.posFile = new_pos
    l_Customer.append(oCustomer)
    saveCustomer(fCustomer, oCustomer)
    t_CustomerInterfaz.append(
        [oCustomer.ID, oCustomer.name, oCustomer.color, oCustomer.mode, oCustomer.type, oCustomer.posFile])

def delCustomer(l_Customer, t_CustomerInterfaz, posinTable):
    if 0 <= posinTable < len(t_CustomerInterfaz):
        l_Customer.pop(posinTable)
        t_CustomerInterfaz.pop(posinTable)
        deleteCustomer(fCustomer, posinTable)

def updateCustomer(l_Customer, t_row_CustomerInterfaz, posinFile):
    cdel = next((customer for customer in l_Customer if customer.customerinPos(posinFile)), None)
    if cdel is not None:
        cdel.setCustomer(t_row_CustomerInterfaz[1], t_row_CustomerInterfaz[2], t_row_CustomerInterfaz[3],
                         t_row_CustomerInterfaz[4])
        modifyCustomer(fCustomer, cdel.posFile, cdel)

def sort_table(table, cols):
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table

def interfaz():
    font1, font2 = ('Roboto', 14), ('Roboto', 16)
    sg.theme('DarkGrey6')
    sg.set_options(font=font1)
    table_data = []
    rowToUpdate = []
    readCustomer(fCustomer, lCustomer)
    for o in lCustomer:
        if not o.erased:
            table_data.append([o.ID, o.name, o.color, o.mode, o.type, o.posFile])

    layout = [
        [sg.Push(), sg.Text('Game Create'), sg.Push()]] + [
                 [sg.Text(text), [sg.Push()], sg.Push(), sg.Input(key=key)] for key, text in
                 Customer.fields.items()] + [

        [sg.Button('Add', size=(10, 1), border_width=4), sg.Button('Delete', size=(10, 1), border_width=4),
         sg.Button('Modify', size=(10, 1), border_width=4), sg.Button('Clean', size=(10, 1), border_width=4)],
        [sg.Table(values=table_data, headings=Customer.headings, max_col_width=50, num_rows=10,
                  display_row_numbers=False, justification='center', enable_events=True,
                  enable_click_events=True, vertical_scroll_only=False,
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE, expand_x=True, bind_return_key=True, key='-Table-')],
        [sg.Button('Purge'), sg.Button('Sort File')]
             ]
    sg.theme('Reddit')
    window = sg.Window('Customer Management with Files', layout, finalize=True)
    window['-PosFile-'].update(disabled=True)
    window['-Table-'].bind("<Double-Button-1>", " Double")
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Add':
            valida = True
            if valida:
                addCustomer(lCustomer, table_data,
                            Customer(values['-ID-'], values['-Name-'], values['-Color-'], values['-Mode-'],
                                     values['-Type-'], -1), fCustomer)
                window['-Table-'].update(table_data)
        if event == 'Delete':
            if len(values['-Table-']) > 0:
                selected_index = int(values['-Table-'][0])
                delCustomer(lCustomer, table_data, selected_index)
                window['-Table-'].update(table_data)

        if (event == '-Table- Double'):
            if len(values['-Table-']) > 0:
                row = values['-Table-'][0]
                window['-ID-'].update(disabled=True)
                window['-ID-'].update(str(table_data[row][0]))
                window['-Name-'].update(str(table_data[row][1]))
                window['-Color-'].update(str(table_data[row][2]))
                window['-Mode-'].update(str(table_data[row][3]))
                window['-Type-'].update(str(table_data[row][4]))
                window['-PosFile-'].update(str(table_data[row][5]))
            pass
        if event == 'Clean':
            window['-ID-'].update(disabled=False)
            window['-ID-'].update('')
            window['-Name-'].update('')
            window['-Color-'].update('')
            window['-Mode-'].update('')
            window['-Type-'].update('')
            window['-PosFile-'].update('')
        if event == 'Modify':
            valida = True
            if valida:
                for t in table_data:
                    if t[-1] == int(values['-PosFile-']):
                        rowToUpdate = t
                        t[1], t[2], t[3], t[4] = values['-Name-'], values['-Color-'], values['-Mode-'], values['-Type-']
                        break
                updateCustomer(lCustomer, rowToUpdate, int(values['-PosFile-']))
                window['-Table-'].update(table_data)
                window['-ID-'].update(disabled=False)
                sg.popup("Customer with ID: " + values['-ID-'] + " has been modified", title="Alert")

        if event == 'Purge':
            purgue_data(fCustomer)
            window['-ID-'].update(disabled=False)
            sg.popup("Deleted customers has been purged.", title="Alert")

        if isinstance(event, tuple):
            if event[0] == '-Table-':
                if event[2][0] == -1:
                    col_num_clicked = event[2][1]
                    table_data = sort_table(table_data, (col_num_clicked, 0))
                    window['-Table-'].update(table_data)

    window.close()


interfaz()
