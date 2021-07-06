import socket
import time
import pygame

# touch event types
TOUCH_UP = 0
TOUCH_DOWN = 1
TOUCH_MOVE = 2
SET_SCREEN_SIZE = 9

# you can copy and paste these methods to your code
def formatSocketData(type, index, x, y):
    return '{}{:02d}{:05d}{:05d}'.format(type, index, int(x*10), int(y*10))

def keyPress(x, y):
    s.send(("101" + formatSocketData(TOUCH_DOWN, 7, x, y)).encode())
    time.sleep(0.05)
    print(formatSocketData(TOUCH_DOWN, 7, x, y))
    s.send(("101" + formatSocketData(TOUCH_UP, 7, x, y)).encode())  # release finger
    time.sleep(0.05)

def hold(x, y):
    s.send(("101" + formatSocketData(TOUCH_DOWN, 7, x, y)).encode())
    time.sleep(0.01)
    print(formatSocketData(TOUCH_DOWN, 7, x, y))

def release(x, y):
    s.send(("101" + formatSocketData(TOUCH_UP, 7, x, y)).encode())  # release finger
    time.sleep(0.05)
    print(formatSocketData(TOUCH_DOWN, 7, x, y))

def main():
    pygame.init()
    pygame.display.set_caption("minimal program")
    screen = pygame.display.set_mode((240,180))
    running = True
    softdrop = False
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # only do something if the event is of type QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    keyPress(200,2400)
                    print("key left")
                if event.key == pygame.K_RIGHT:
                    keyPress(400, 2400)
                    print("key right")
                if event.key == pygame.K_SPACE:
                    keyPress(300, 2300)
                    print("key space bar")
                if event.key == pygame.K_DOWN:
                    # keyPress(300, 2500)
                    # print("key down")
                    softdrop = True
                if event.key == pygame.K_c:
                    keyPress(1050, 2000)
                    print("key c")
                if event.key == pygame.K_UP:
                    # keyPress(1050, 2300)
                    print("key up")
                    hold(1050, 2300)
                    softdrop = True
                if event.key == pygame.K_z:
                    keyPress(900, 2400)
                    print("key z")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    release(900, 2300)
                    softdrop = False
        # if softdrop:
        #     hold(1050, 2300)
        #     print("soft drop")





if __name__ == '__main__':
    s = socket.socket()
    s.connect(("192.168.1.40", 6000))  # connect to the tweak
    # s.connect(("172.20.10.1", 6000))
    time.sleep(0.2)  # please sleep after connection.

    # # the format should be "{task_id(2 digits)}{task_data}"
    # #############   switch application to foreground part   ##############
    # s.send("11com.apple.Preferences".encode())  # 11 at head means the task is id 11 (launch app). Move application "com.apple.Preferences" to the foreground" (launch settings app)
    # time.sleep(1)

    #############   show system wide alert box part   ##############
    # s.send("12Python Tetris Script;;The script has started.".encode())  # 12 at head means the task id is 12 (show alert). Title and content should be splitted by two semicolons.
    s.send("12Python Tetris script;;Close this message to use keyboard on tetris.".encode())
    time.sleep(1)
    main()

    s.close()