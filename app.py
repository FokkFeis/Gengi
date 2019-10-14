import urllib.request
import json
import PySimpleGUI as sg
import locale
locale.setlocale(locale.LC_ALL, 'is_IS')
'is_IS'
locale.format_string('%f', 0, grouping=True)

sg.ChangeLookAndFeel('SystemDefault')
valin_gengi = [{'shortName': 'ISK', 'longName': 'Íslensk Króna', 'value': 1, 'askValue': 1, 'bidValue': 1, 'changeCur': 0.22, 'changePer': 0}]   # Preset ISK kr
shortNames = {'ISK'}

try:
    with open('shortNames.txt', 'r') as f:
        data = f.read()
        for x in data.split():
            if x not in shortNames:
                shortNames.add(x)
except:
    pass

with urllib.request.urlopen("https://apis.is/currency/lb") as url:
    gengi = json.loads(url.read())
    gengi = gengi["results"]


def addToFile():
    with open('shortNames.txt', 'w') as f:
        f.write(' '.join(shortNames))


def addToGengi(gengi):
    if gengi not in valin_gengi:
        valin_gengi.append(gengi)
        shortNames.add(gengi['shortName'])


def removeFromGengi(gengi):
    if gengi in valin_gengi:
        valin_gengi.remove(gengi)
        shortNames.remove(gengi['shortName'])


def l2():
    lay = [[sg.Text('Gjaldmiðill', size=(10, 1)), sg.Text('Kaup', size=(8, 1)), sg.Text('Sala', size=(8, 1)),
               sg.Text('Upphæð', size=(10, 1))]]
    lay += [[sg.Text(x['shortName'], size=(10, 1)), sg.Text('{:.2f}'.format(x['value']), size=(8, 1)),
             sg.Text('{:.2f}'.format(x['askValue']), size=(8, 1)), sg.Input('{:n}'.format(round(1000 / x['askValue'], 2)), size=(12, 1),
            key=x['shortName'], enable_events=True)] for x in valin_gengi]
    lay += [[sg.Button('Baka')]]
    return lay


def l1():
    lay = [
        [sg.Checkbox(x['shortName'], key='_check_' + x['shortName'], size=(5, 1), enable_events=True, default=True if x['shortName'] in shortNames else False) for x in
         gengi[:5]],
        [sg.Checkbox(x['shortName'], key='_check_' + x['shortName'], size=(5, 1), enable_events=True, default=True if x['shortName'] in shortNames else False) for x in
         gengi[5:10]],
        [sg.Checkbox(x['shortName'], key='_check_' + x['shortName'], size=(5, 1), enable_events=True, default=True if x['shortName'] in shortNames else False) for x in
         gengi[10:15]],
        [sg.Checkbox(x['shortName'], key='_check_' + x['shortName'], size=(5, 1), enable_events=True, default=True if x['shortName'] in shortNames else False) for x in
         gengi[15:20]],
        [sg.Button('Vista')]
    ]
    return lay


def calculate(window, org):
    try:
        values[org] = float(values[org])
        if values[org] != '' and type(values[org]) is float:
            land = None
            for x in valin_gengi:
                if x['shortName'] == org:
                    land = x
                    break
            new_isk = float(values[org]) * land['askValue']
            for x in valin_gengi:
                if x['shortName'] == org:
                    continue
                calc = new_isk / float(x['askValue'])
                window.Element(x['shortName']).Update('{:n}'.format(round(calc, 2)))
    except:
        pass


layout = l1()
windowName = 'Gengi'
# Create the Window
window = sg.Window(windowName, layout, keep_on_top=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break

    if windowName == 'Gengi':
        for x in gengi:
            check = window.FindElement('_check_' + x['shortName'])
            if check.get():
                check.Update(addToGengi(x))
            else:
                check.Update(removeFromGengi(x))
            addToFile()
    print(shortNames)
    if event == 'Baka':
        windowName = 'Gengi'
        layout = l1()
        window1 = sg.Window(windowName, layout, keep_on_top=True)
        window.close()
        window = window1
    if event == 'Vista':
        windowName = 'Gengi reiknivél'
        layout = l2()
        window1 = sg.Window(windowName, layout, keep_on_top=True)
        window.Close()
        window = window1
    if event in shortNames:
        window.Element(event).Update(calculate(window, event))


window.close()
