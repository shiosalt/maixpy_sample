# this script use ESP8266 as wifi network card for MAix bit.
# connect ESP8286 TX to pin-6,RX to pin-7
# and ESP8286 must be runing on AT command mode.

import usocket as socket
import ustruct as struct
import network
import machine
from board import board_info
from fpioa_manager import fm

SSID = "SSID"
SSID_PWD = "PASSWORD"
timezonehour = 9 #Japan

def esp_connect():
    fm.register(board_info.WIFI_RX, fm.fpioa.UART2_TX)
    fm.register(board_info.WIFI_TX, fm.fpioa.UART2_RX)
    uart = machine.UART(machine.UART.UART2, 115200,timeout=1000, read_buf_len=4096)
    try:
        nic=network.ESP8285(uart)
        nic.connect(SSID,SSID_PWD)
        if (nic.isconnected):
            print("ip:{}/{}".format(nic.ifconfig()[0],nic.ifconfig()[1]))
            return True
        else:
            sleep(1)  # retry
            if (nic.isconnected):
                print("ip:{}/{}".format(nic.ifconfig()[0],nic.ifconfig()[1]))
                return True
            else:
                print("network connection failed.\n")
                return False

    except:
        print(" try to connect ESP8286 TX to pin-{},RX to pin-{}".format(board_info.WIFI_TX,board_info.WIFI_RX))
        print(" ,and ESP8286 must be runing on AT command mode.\n")
        return False

def ntptime():
    NTP_DELTA = 1009843200
    #NTP_DELTA = 3155673600
    # maixpy : (date(2032, 1, 1) - date(2000, 1, 1)).days * 24*60*60
    # usual  : (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    so.settimeout(1)
    """ maixpy seems not yet support sendto.
    res = so.sendto(NTP_QUERY, addr)
    """
    so.connect(addr)
    so.send(NTP_QUERY)
    msg = so.recv(48)
    so.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA

def settime():
    t = ntptime() + timezonehour *60*60
    import utime
    tm = utime.localtime(t)
    utime.set_time(tm)

if(esp_connect()):
    host = "pool.ntp.org"
    settime()
    import utime
    t = utime.localtime()
    print("{0}/{1:0=2}/{2:0=2} {3:0=2}:{4:0=2}".format(t[0],t[1],t[2],t[3],t[4]) )
    #this may show strange year, but date of file creation is collect when writing to SD card.
    #(maybe maixpy's problem)
else:
    print("esp connection error.\n")

SSID = ""
SSID_PWD = ""
