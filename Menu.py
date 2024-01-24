import PySimpleGUI as sg

import DisplayGrapher as graph
from Tracker import MonteSim

"""
This clas controls all functionality of the tracker application
It allows us to be able to either plot, table, or do both operations
on the tracker data.

To construct the menus for selection, we have utilized the PySimpleGUI 
library. We ask whether the user would like to simple see stock trends and histories,
or would like predictions on tickers.

There are additional menus that are created in response to the user's specified demand
"""


def beginApp():
    sg.theme('DarkTeal9')
    mainLayout = [[sg.Text("Stock History and Analysis")],
                  [sg.Button("Ticker Histories")],
                  [sg.Button("Monte Carlo on Ticker")]]

    main_window = sg.Window("History", mainLayout, font = 'Times', element_justification = 'c')
    while True:
        event, values = main_window.read()
        if event == 'Ticker Histories':
            main_window.disable()
            multipleTracker()
            main_window.enable()
        elif event == 'Monte Carlo on Ticker':
            main_window.disable()
            monteMenu()
            main_window.enable()
        elif event == sg.WINDOW_CLOSED:
            break
    main_window.close()


def multipleTracker():
    multiLayout = [[sg.Text("List all stocks and the time period for the history")],
                   [sg.Text('Name of ticker 1'), sg.InputText()],
                   [sg.Text('Name of ticker 2'), sg.InputText()],
                   [sg.Text('Name of ticker 3'), sg.InputText()],
                   [sg.Text('Name of ticker 4'), sg.InputText()],
                   [sg.Text("Time"), sg.Slider(range = (1, 30),
                                               orientation = 'h',
                                               default_value = 15)], [sg.Text('')],
                   [sg.Text("Time increment")],
                   [sg.Button("Days"), sg.Button("Months"), sg.Button("Years")],
                   [sg.Text('')],
                   [sg.Checkbox(text = 'Singular graph', default = False)],
                   [sg.Text('')],
                   [sg.Button("SUBMIT"), sg.Button("EXIT")]
                   ]
    # Assigning the layout to the window, providing a title as well
    multiWindow = sg.Window('Multiple Ticker History', multiLayout, element_justification = 'c')
    timeTrack: str = ""
    while True:
        event, values = multiWindow.read()
        if event == 'Days':
            timeTrack = 'd'
        elif event == 'Months':
            timeTrack = 'mo'
        elif event == 'Years':
            timeTrack = 'y'
        elif event == 'SUBMIT':
            # Create a new window providing the graph
            # Assume default time option is days
            tickerNames: list[str] = []
            for i in range(0, 3):
                if values[i] != '':
                    tickerNames.append(values[i])
            timeTrack = str(int(values[4])) + ('d' if timeTrack == '' else timeTrack)
            graph.showGraphMulti(tickerNames, timeTrack) \
                if values[5] is False \
                else graph.showGraphSing(tickerNames, timeTrack)
        elif event == 'EXIT' or event == sg.WINDOW_CLOSED:
            break
        multiWindow.close()


def monteMenu():
    monteLayout = [[sg.Text("List the stock, as well as how many simulations you would like done")],
                   [sg.Text('Name of ticker'), sg.InputText()],
                   [sg.Text()],
                   [sg.Text("Amount of Simulations")],
                   [sg.Text('Select the amount of simulations'),
                    sg.Combo(['LOW', 'MEDIUM', 'HIGH'])],
                   [sg.Text()],
                   [sg.Text("How many days should the simulation predict"), sg.Slider(range = (1, 50),
                                                                                      orientation = 'h',
                                                                                      default_value = 25)],
                   [sg.Text('')],
                   [sg.Button("SUBMIT"), sg.Button("EXIT")]]
    monteWindow = sg.Window('Monte Carlo Creation', monteLayout, element_justification = 'c')
    while True:
        event, values = monteWindow.read()
        if event == "SUBMIT":
            MonteSim.runSim('AAPL' if values[0] == '' else values[0],
                            50000 if values[1] == 'LOW' else
                            10000 if values[1] == 'MEDIUM' else 5000, int(values[2]))
        elif event == 'EXIT' or event == sg.WINDOW_CLOSED:
            break
    monteWindow.close()