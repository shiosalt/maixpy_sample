'''
maixpy script
display camera's image to lcd ,
and save to /sd/image/xxxxxxxx.jpg (upto 500 files)

'''
import sensor
import image
import lcd

#camera config
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(0) #default mirrored
sensor.run(1)

#lcd config
lcd.init()
lcd.direction(lcd.YX_LRUD) #default rotated

chsd=False

if (len(os.listdir("/"))>1): #easy-check /flash and /sd exist
    chsd=True
else:
    print("SD card not found.")
    lcd.draw_string(10,20,"SD card error.",lcd.RED)
    chsd=False
try:
    if (chsd):
        os.mkdir("/sd/image")
except:
    print("forlder exists.coninue.")

n=0
try:
    while(True):
        img = sensor.snapshot()
        a = lcd.display(img)
        if(chsd):
            img.save("/sd/image/{0:0=8}.jpg".format(n)) #00000000.jpg 
        n=n+1
        if (n>500):
            break
    print("capture end")
    lcd.draw_string(10,30,"capture end",lcd.WHITE)

except:
    print("except error.exit")
    lcd.draw_string(10,30,"except error.exit",lcd.RED)

