from TemperatureMonitor import TemperatureMonitor
from TemperatureDisplayer import TemperatureDisplayer
from LocalDbHandler import LocalDbHandler
from OnlineDbHandler import OnlineDbHandler


def main():
    tempMonitor = TemperatureMonitor()
    tempDisplayer = TemperatureDisplayer()
    localDbHandler = LocalDbHandler()
    onlineDbHandler = OnlineDbHandler()
    
    tempMonitor.start()
    tempDisplayer.start()
    localDbHandler.start()
    onlineDbHandler.start()
    
if __name__ == "__main__":
    main()       