import tkinter as tk
from tkinter import messagebox
import psutil
import threading
import time
import smtplib
from email.mime.text import MIMEText

# === CONFIGURATIONS ===
SCAN_INTERVAL = 10  # seconds
EMAIL_ALERT_ENABLED = True

EMAIL_ADDRESS = "0e89a05f130260"     # 🔥 change this
EMAIL_PASSWORD = "ba158391162c01"     # 🔥 use an App Password if Gmail
SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 587

# === EMAIL ALERT FUNCTION ===
def send_email_alert(subject, body):
    if not EMAIL_ALERT_ENABLED:
        return
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("[+] Email alert sent.")
    except Exception as e:
        print(f"[!] Failed to send email alert: {e}")

# === DETECTOR LOGIC ===
class KeyloggerDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger Detector GUI")
        self.root.geometry("700x450")

        self.process_listbox = tk.Listbox(root, width=100, height=20)
        self.process_listbox.pack(pady=20)

        self.kill_button = tk.Button(root, text="Kill Selected Process", command=self.kill_selected_process)
        self.kill_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Idle")
        self.status_label.pack()

        self.suspicious_processes = []
        self.update_processes()

    def detect_suspicious_processes(self):
        suspicious = []
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                cmdline = " ".join(proc.info['cmdline']) if proc.info['cmdline'] else ""
                if proc.info['name'] and ("python" in proc.info['name'].lower() or "pynput" in cmdline.lower() or "keyboard" in cmdline.lower()):
                    suspicious.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return suspicious

    def update_processes(self):
        self.process_listbox.delete(0, tk.END)
        self.suspicious_processes = self.detect_suspicious_processes()

        if self.suspicious_processes:
            for proc in self.suspicious_processes:
                cmdline = proc.info['cmdline']
                cmdline_str = ' '.join(cmdline) if isinstance(cmdline, list) else "N/A"
                self.process_listbox.insert(tk.END, f"PID={proc.pid} | {proc.name()} | {cmdline_str}")
            self.status_label.config(text="Status: Suspicious processes detected! 🚨")
            send_email_alert("Keylogger Detector Alert", "Suspicious process(es) found!")
        else:
           self.status_label.config(text="Status: All clean. ✅")

        self.root.after(SCAN_INTERVAL * 1000, self.update_processes)

    def update_processes(self):
        self.process_listbox.delete(0, tk.END)
        self.suspicious_processes = self.detect_suspicious_processes()

        if self.suspicious_processes:
            email_body = ""
            for proc in self.suspicious_processes:
                cmdline = proc.info['cmdline']
                cmdline_str = ' '.join(cmdline) if isinstance(cmdline, list) else "N/A"
                proc_details = f"PID={proc.pid} | Name={proc.name()} | Cmdline={cmdline_str}\n"
                self.process_listbox.insert(tk.END, proc_details)
                email_body += proc_details

            self.status_label.config(text="Status: Suspicious processes detected! 🚨")
            send_email_alert("Keylogger Detector Alert", email_body)

        else:
            self.status_label.config(text="Status: All clean. ✅")

        self.root.after(SCAN_INTERVAL * 1000, self.update_processes)


    def kill_selected_process(self):
        selected = self.process_listbox.curselection()
        if selected:
            idx = selected[0]
            proc = self.suspicious_processes[idx]
            try:
                proc.terminate()
                messagebox.showinfo("Success", f"Terminated PID {proc.pid}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

# === MAIN ===
if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerDetectorApp(root)
    root.mainloop()
