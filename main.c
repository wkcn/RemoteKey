#include "key.h"
#include "serial.h"

void main(void) {
    u8 send_buffer[2];
    u8 remoteKeyCode = 0;

    serial_init();
    key_init();

    while(1)
    {
        // 检测是否收到数据
        if((TX1_Cnt != RX1_Cnt) && (!B_TX1_Busy))   //收到数据, 发送空闲
        {
            remoteKeyCode = RX1_Buffer[TX1_Cnt];
            if(++TX1_Cnt >= UART1_BUF_LENGTH)   TX1_Cnt = 0;
        }

        if(B_1ms)   //1ms到
        {
            B_1ms = 0;
            if(++msecond >= 1000)   //1秒到
            {
                msecond = 0;
                ReadRTC();
                DisplayRTC();
            }

            if(++cnt50ms >= 50)     //50ms扫描一次行列键盘
            {
                cnt50ms = 0;
                IO_KeyScan();
            }

            if(KeyCode != 0) // 有键按下，发送信息
            {
                send_buffer[0] = KeyCode; 
                send_buffer[1] = 0;
                // 发送按键信息
                PrintString1(send_buffer);
                // KeyCode 清零
                KeyCode = 0;
            }

            if(remoteKeyCode != 0)        //有键按下
            {
                if(remoteKeyCode == 17)   //hour +1
                {
                    if(++hour >= 24)    hour = 0;
                    WriteRTC();
                    DisplayRTC();
                }
                if(remoteKeyCode == 18)   //hour -1
                {
                    if(--hour >= 24)    hour = 23;
                    WriteRTC();
                    DisplayRTC();
                }
                if(remoteKeyCode == 19)   //minute +1
                {
                    second = 0;
                    if(++minute >= 60)  minute = 0;
                    WriteRTC();
                    DisplayRTC();
                }
                if(remoteKeyCode == 20)   //minute -1
                {
                    second = 0;
                    if(--minute >= 60)  minute = 59;
                    WriteRTC();
                    DisplayRTC();
                }

                remoteKeyCode = 0;
            }

        }
    }
}
