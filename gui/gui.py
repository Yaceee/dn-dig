from distutils.command import config
import eel
import eel.browsers
import sources
import sources.config
import sys

from sources.simThread import startSimulationThreads

if __name__ == '__main__':
    eel.init('views')

    @eel.expose
    def startSimulationPy(json):
        confs = sources.config.confFromJSON(json)
        startSimulationThreads(confs[0], confs[1])

    eel.browsers.set_path('electron', './node_modules/electron/dist/electron')

    eel.start('main.html', mode="electron", host="localhost", port=8000, disable_cache=True)

    