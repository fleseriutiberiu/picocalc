#This app is for the picocalc to be set on the SD
#It will send a string to UART which will be read by a Heltev 32 v3
#which is configured a Serial textmsg so it will send the UART string
#to the mesh default channel

uart_comm = None
led = None 


def start(view_manager):
    """Start the app"""
    from machine import UART
    import time
    from machine import Pin
    global led, uart_comm
    uart_comm = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))
    led = Pin("LED", Pin.OUT)

    return True

def run(view_manager):
    """Run the app"""
    from picoware.system.buttons import BUTTON_UP, BUTTON_DOWN, BUTTON_BACK
    import time
    global uart_comm, led

    inp = view_manager.input_manager
    button = inp.button



    if button == BUTTON_UP:
        inp.reset()
        led.value(1)
        time.sleep(0.2)
        uart_comm.write("salut")
        led.value(0)
        time.sleep(0.2)

    elif button == BUTTON_BACK:
        inp.reset()
        view_manager.back()
    
    
def stop(view_manager):
    """Stop the app"""
    from gc import collect

    global uart_comm

    del uart_comm
    uart_comm = None

    collect()
