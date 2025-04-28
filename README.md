#  Keylogger Detection and Alert System

A lightweight Python-based tool to **detect keyloggers** and **suspicious processes** in real-time on Windows machines.  
The system features a **live GUI monitor**, **manual kill options**, and **email alerting** through Mailtrap SMTP.


## Features

- **Suspicious Process Detection**  
  Scans running processes for keylogger patterns (`pynput`, `keyboard`, etc.).

- **Graphical User Interface (GUI)**  
  Lists detected suspicious processes in a simple Tkinter-based GUI.

- **Manual Process Termination**  
  Select a detected process and manually kill it safely.

- **Email Alerts**  
  Sends a full detailed report of detections via email (using Mailtrap SMTP server).

- **Portable Executable**  
  Can be packaged as a `.exe` file for standalone Windows deployment.

![image](https://github.com/user-attachments/assets/7154d68e-92d6-4a25-89ed-0d0587ef976b)


## Technologies Used

- Python 3.x
- Tkinter (GUI)
- Psutil (process management)
- Smtplib (email sending)
- Mailtrap (safe email testing)


## Setup Instructions

1. Clone the Project
```bash
git clone https://github.com/your-username/keylogger-detector.git
cd keylogger-detector
```

2. Install Required Libraries
```bash
pip install psutil
pip install pynput
```
(Note: Tkinter comes preinstalled with Python.)

3. Setup Email Alert Configuration
Inside ```detector.py```, update these lines with your Mailtrap credentials:
```
EMAIL_ADDRESS = "your_mailtrap_username"
EMAIL_PASSWORD = "your_mailtrap_password"
SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525
```
(Mailtrap credentials can be found under SMTP Settings.)

4. Run the Detector
```bash
python detector.py
```
 A GUI window will open.
 
 Suspicious processes will appear if detected.

## How It Works
<b>1. Scanning</b>: Every 10 seconds (default), the program scans all running processes.

<b>2. Matching:</b> Processes using suspicious modules (pynput, keyboard) are flagged.

<b>3. Reporting:</b>

  - Displays in GUI.
  
  - Sends full process details to Mailtrap inbox.

<b>4. Manual Action:</b> User can select a process and terminate it directly from the GUI.

## Building as Executable (.exe)
1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the .exe:
```bash
pyinstaller --onefile --noconsole detector.py
```
The ```.exe``` will be available in the ```/dist/``` folder.

## Example Email Alert
```
Keylogger Detector Alert

PID=1234 | Name=python.exe | Cmdline=python fake_keylogger.py
PID=5678 | Name=pythonw.exe | Cmdline=python hidden_logger.py
```
Emails are safely captured inside Mailtrap, not sent to real email accounts.

![image](https://github.com/user-attachments/assets/08d50ce5-f927-48a0-b498-6240f4ed996d)


## Testing with a Fake Keylogger
You can simulate an attacker by running this fake script:
```
from pynput import keyboard

def on_press(key):
    print(f"Key pressed: {key}")

listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
```
Run:
```
python fake_keylogger.py
```
Your detector will immediately detect and report it.

## Testing with a Fake File Modifier
Another way to simulate suspicious behavior is to create a script that frequently modifies a file — similar to how some keyloggers save logs.

Fake File Modifier Script:
```
import time

while True:
    with open("testfile.txt", "a") as f:
        f.write("Simulated log entry...\n")
    time.sleep(2)  # Modify file every 2 seconds
```
- Save it as file_modifier.py.
- Run it in a separate terminal:

```
python file_modifier.py
```
#### What Happens:

  - Your Keylogger Detector will notice frequent file modifications.

  - It will flag testfile.txt as suspicious activity.

## Important Notes
  - ONLY for educational purpose.

  - Always test suspicious software inside a virtual machine.

  - Not a replacement for full antivirus software — this is a focused keylogger detection tool.

## Future Enhancements (Ideas)
  - Detect screen recording and microphone recording processes.

  - Automatically quarantine detected files.

  - Real-time notifications via desktop pop-ups or Slack.


## Author
Vinu Varshith Alagappan

M.Sc., Cybersecurity



