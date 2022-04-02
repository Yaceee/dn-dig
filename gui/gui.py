import eel
import eel.browsers
import sys

eel.init('views')

@eel.expose
def startSimulationPy(json):
    print(json)

eel.browsers.set_path('electron', './node_modules/electron/dist/electron')

eel.start('main.html', mode="electron", host="localhost", port=8000, disable_cache=True)