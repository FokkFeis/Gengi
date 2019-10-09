import urllib.request
import json

import PySimpleGUI as sg

# All the stuff inside your window.
gl = []


def addToGengi(shortName):
    if shortName not in gl:
        gl.append(shortName)


def removeFromGengi(shortName):
    if shortName in gl:
        gl.remove(shortName)


def l2():
    l = [
        [sg.Text('Gjaldmiðill', size=(12, 1)), sg.Text('Kaup', size=(5, 1)), sg.Text('Sala', size=(5, 1)), sg.Text('Upphæð', size=(8, 1))],
        [[sg.Text(x['shortName'], size=(12, 1)), sg.Text(x['value'], size=(5, 1)), sg.Text(x['askValue'], size=(5, 1)), sg.Input(x['askValue'], size=(8, 1))] for x in gl]
    ]
    return l


with urllib.request.urlopen("https://apis.is/currency/lb") as url:
    gengi = json.loads(url.read())
    gengi = gengi["results"]
    tab1_layout = [
        [sg.Checkbox(x['shortName'], key='_check_' + x['shortName'], size=(5, 1), enable_events=True) for x in
         gengi[:5]],
        [sg.Checkbox(x['shortName'], key='_check_' + x['shortName'], size=(5, 1), enable_events=True) for x in
         gengi[5:10]],
        [sg.Checkbox(x['shortName'], key='_check_' + x['shortName'], size=(5, 1), enable_events=True) for x in
         gengi[10:15]],
        [sg.Checkbox(x['shortName'], key='_check_' + x['shortName'], size=(5, 1), enable_events=True) for x in
         gengi[15:20]]
    ]

tab2_layout = l2()

layout = [[sg.TabGroup([[sg.Tab('Lönd', tab1_layout), sg.Tab('Gengi', tab2_layout)]])]]
# Create the Window
window = sg.Window('Gengi', layout, keep_on_top=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    for x in gengi:
        check = window.FindElement('_check_' + x['shortName'])
        if check.get():
            check.Update(addToGengi(x))
        else:
            check.Update(removeFromGengi(x))



    print(gl)

window.close()
