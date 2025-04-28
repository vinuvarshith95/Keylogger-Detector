from pynput import keyboard

def on_press(key):
    print(f"Key pressed: {key}")

# Start the keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
