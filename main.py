from TemperatureMonitor import TemperatureMonitor
from TemperatureDisplayer import TemperatureDisplayer


def main():
    tempMonitor = TemperatureMonitor()
    tempDisplayer = TemperatureDisplayer()
    
    tempMonitor.start()
    tempDisplayer.start()
    
    
if __name__ == "__main__":
    main()       