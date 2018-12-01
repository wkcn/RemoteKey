#coding=utf-8
import sys
import serial
import threading

if sys.version_info[0] >= 3:
    raw_input = input

PORT = '/dev/ttyUSB0'
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
            buffer += s.decode('utf-8')
        else:
            if buffer:
                colorstr = '\033[1;32;46m%s\033[0m'
                print(colorstr % buffer)
            buffer = ''

# 如果收到信息，则打印
thread_recv = threading.Thread(target=receiver, args=(SERIAL,))
thread_recv.setDaemon(True)
thread_recv.start()

# 输入信息
while 1:
    msg = raw_input()
    SERIAL.write(msg.encode('utf-8'))
