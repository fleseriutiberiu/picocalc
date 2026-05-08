# This app is for the picocalc to be set on the SD
# It will send a string to UART which will be read by a Heltev 32 v3
# which is configured a Serial textmsg so it will send the UART string
# to the mesh default channel

uart_comm = None
led = None
draw = None
last_check_time = 0
square_color = 0xFFFF  # Start with white
_textbox = None
timer_seconds = 60  # 60 second countdown timer
timer_last_update = 0  # Last time timer was updated
print('ciuriburi')


def start(view_manager):
    """Start the app"""
    from picoware.system.uart import UART
    import time
    from machine import Pin
    print('ciuriburi')
    global led, uart_comm, draw, _textbox, timer_seconds, timer_last_update
    uart_comm = UART(1, baud_rate=115200, tx_pin=Pin(8), rx_pin=Pin(9))
    led = Pin("LED", Pin.OUT)
    draw = view_manager.draw

    # Initialize timer
    timer_seconds = 60
    timer_last_update = time.time()

    if _textbox is None:
        from picoware.gui.textbox import TextBox
        from picoware.system.colors import TFT_YELLOW
        # Position textbox at the bottom of the screen
        textbox_height = draw.size.y // 2  # Use bottom half of screen
        textbox_y = draw.size.y - textbox_height
        _textbox = TextBox(draw, textbox_y, textbox_height,
                           foreground_color=TFT_YELLOW)
        _textbox.set_text("UART Monitor Started...\n")

    return True


def run(view_manager):
    """Run the app"""
    from picoware.system.buttons import BUTTON_UP, BUTTON_DOWN, BUTTON_BACK, BUTTON_RIGHT
    from picoware.system.vector import Vector
    import time
    from picoware.system.colors import (
        TFT_GREEN,
        TFT_WHITE,
    )
    global uart_comm, led, draw, last_check_time, square_color, _textbox, timer_seconds, timer_last_update

    current_time = time.time()

    # Update timer countdown every second
    if current_time - timer_last_update >= 1:
        timer_last_update = current_time
        if timer_seconds > 0:
            timer_seconds -= 1

    # Check for UART data
    if uart_comm.has_data:
        data = uart_comm.read_line()
        _textbox.set_text(_textbox.text + data)
        if data and "af4c: GateKeepAlive" in data:
            square_color = TFT_GREEN
            # Reset timer when keep-alive is received
            timer_seconds = 60
            timer_last_update = current_time
        else:
            square_color = TFT_WHITE
    else:
        square_color = TFT_WHITE

    # Draw the square with the current color
    square_size = 50
    square_x = 50
    square_y = 60
    draw.fill_rectangle(Vector(square_x, square_y), Vector(
        square_size, square_size), square_color)

    # Draw the timer countdown
    draw.text(Vector(10, 10), f"Timer: {timer_seconds}s", TFT_WHITE)

    # Draw a square border around the textbox
    border_color = TFT_WHITE
    border_thickness = 2
    # Draw top border
    draw.fill_rectangle(Vector(_textbox.position.x, _textbox.position.y),
                        Vector(_textbox.size.x, border_thickness), border_color)
    # Draw bottom border
    draw.fill_rectangle(Vector(_textbox.position.x, _textbox.position.y + _textbox.size.y - border_thickness),
                        Vector(_textbox.size.x, border_thickness), border_color)
    # Draw left border
    draw.fill_rectangle(Vector(_textbox.position.x, _textbox.position.y),
                        Vector(border_thickness, _textbox.size.y), border_color)
    # Draw right border
    draw.fill_rectangle(Vector(_textbox.position.x + _textbox.size.x - border_thickness, _textbox.position.y),
                        Vector(border_thickness, _textbox.size.y), border_color)

    draw.swap()

    inp = view_manager.input_manager
    button = inp.button

    if button == BUTTON_UP:
        inp.reset()
        _textbox.scroll_up()
        print('pressed up')

    elif button == BUTTON_DOWN:
        inp.reset()
        _textbox.scroll_down()
        print('pressed down')
    elif button == BUTTON_BACK:
        inp.reset()
        view_manager.back()
        print('pressed back')

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

    global uart_comm

    del uart_comm
    uart_comm = None

    collect()
