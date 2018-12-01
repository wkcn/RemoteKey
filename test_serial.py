# coding=utf-8
import platform
import sys
import serial
import threading


OS_NAME = platform.system()
OS_IS_WINDOWS = OS_NAME == 'Windows'
OS_IS_LINUX = OS_NAME in ['Linux', 'Darwin']
assert OS_IS_WINDOWS or OS_IS_LINUX,\
    Exception('Unsupported Operator System: {}'.format(OS_NAME))

if sys.version_info[0] >= 3:
    raw_input = input

PORT = '/dev/ttyUSB0' if OS_IS_LINUX else 'COM3'
BAUDRATE = 115200
TIMEOUT = 0.5

# 读取串口
SERIAL = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)

print('Please input some strings, then press enter key :-)')


def receiver(ser):
    buffer = ''
    while 1:
        s = ser.read(1)
        if s:
            c = s.decode('utf-8')
            # Notice: when restarting SCM, the first char is char(0).
            # In Windows, if the first char of string is char(0),
            #   the string won't be printed.
            if ord(c) != 0:
                buffer += c
        else:
            if buffer:
                print(buffer)
            buffer = ''


# 如果收到信息，则打印
thread_recv = threading.Thread(target=receiver, args=(SERIAL,))
thread_recv.setDaemon(True)
thread_recv.start()

# 输入信息
while 1:
    msg = raw_input()
    SERIAL.write(msg.encode('utf-8'))
