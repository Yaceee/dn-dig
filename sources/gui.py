import eel
import eel.browsers
import config
import sys

from simThread import startSimulationThreads

if __name__ == '__main__':
    eel.init('./gui')

    @eel.expose
    def startSimulationPy(json):
        print(json)
        confs = config.confFromJSON(json)
        startSimulationThreads(confs[0], confs[1])
    
    eel.browsers.set_path('electron', './node_modules/electron/dist/electron')

    eel.start('./views/main.html', mode="electron", host="localhost", port=8000, disable_cache=True)

    