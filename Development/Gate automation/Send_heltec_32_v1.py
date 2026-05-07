# This app is for the picocalc to be set on the SD
# It will send a string to UART which will be read by a Heltev 32 v3
# which is configured a Serial textmsg so it will send the UART string
# to the mesh default channel

uart_comm = None
led = None
_textbox = None


def start(view_manager):
    """Start the app"""
    from picoware.system.uart import UART
    import time
    from machine import Pin
    from picoware.gui.textbox import TextBox
    global led, uart_comm, _textbox
    uart_comm = UART(1, baud_rate=115200, tx_pin=Pin(8), rx_pin=Pin(9))
    led = Pin("LED", Pin.OUT)

    if _textbox is None:
        draw = view_manager.draw
        _textbox = TextBox(draw, 0, draw.size.y)
        _textbox.set_text("UART Monitor Started...\n")

    return True


def run(view_manager):
    """Run the app"""
    from picoware.system.buttons import BUTTON_UP, BUTTON_DOWN, BUTTON_BACK, BUTTON_RIGHT
    import time
    global uart_comm, led, _textbox

    inp = view_manager.input_manager
    button = inp.button

    # Check for incoming UART data
    if uart_comm.has_data:
        data = uart_comm.read_line()
        if data:
            _textbox.set_text(_textbox.text + data)

    if button == BUTTON_UP:
        inp.reset()
        _textbox.scroll_up()

    elif button == BUTTON_DOWN:
        inp.reset()
        _textbox.scroll_down()

    elif button == BUTTON_BACK:
        inp.reset()
        view_manager.back()

    elif button == BUTTON_RIGHT:
        inp.reset()
        led.value(1)
        time.sleep(0.2)
        uart_comm.println("salut")
        led.value(0)
        time.sleep(0.2)


def stop(view_manager):
    """Stop the app"""
    from gc import collect

    global uart_comm, _textbox

    del uart_comm
    uart_comm = None

    if _textbox:
        del _textbox
        _textbox = None

    collect()
