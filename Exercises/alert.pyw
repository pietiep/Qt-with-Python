import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

app = QApplication(sys.argv) #PyQt object; sys.argv passes command line arguments to pyqt

try:
    due = QTime.currentTime()
    message = "Alert!"
    if len(sys.argv) < 2:
        raise ValueError
    hours, mins = sys.argv[1].split(":")
    due = QTime(int(hours), int(mins))
    if not due.isValid():
        raise ValueError
    if len(sys.argv) > 2:
        message = " ".join(sys.argv[2:])
except ValueError:
    message = "Usage: alert.pyw HH:MM [optional message]" # 24hr clock

while QTime.currentTime() < due:
    time.sleep(20) # 20 seconds

label = QLabel("<font color=red size=72><b>" + message + "</b></font>") # HTML string
#red text of size 72 points
label.setWindowFlags(Qt.SplashScreen) # removes title bar
label.show() # schedules paint event
QTimer.singleShot(60000, app.quit) # 1 minute in milliseconds -> how long to time out; 2nd argument: function, that is
# after timeout called
app.exec_()
