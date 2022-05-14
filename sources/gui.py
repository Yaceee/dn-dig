import eel
import eel.browsers

from main import record

if __name__ == '__main__':
    eel.init('./gui')

    @eel.expose
    def startSimulationPy(json):
        record(json)

    eel.browsers.set_path('electron', './node_modules/electron/dist/electron')

    eel.start('./views/main.html', mode="electron", host="localhost", port=21445, disable_cache=True)
