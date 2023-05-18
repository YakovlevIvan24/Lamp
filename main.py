from neopixel import Neopixel
from rotary_irq_rp2 import RotaryIRQ

import utime


numpix = 60
strip = Neopixel(numpix, 0, 28, "RGB")
light = [255,255,255]

I = machine.ADC(27)
ratio = machine.ADC(26)

R = RotaryIRQ(14, 15, pull_up=True)
G = RotaryIRQ(10, 11, pull_up=True)
B = RotaryIRQ(12, 13, pull_up=True)
current_R = 0
current_G = 0
current_B = 0 
I_avg = []
while True:
    
    I_ratio = int(ratio.read_u16()/1000)/65
    
    R_val = 255 - R.value()*10
    G_val = 255 - G.value()*10
    B_val = 255 - B.value()*10
    if R_val >= 255:
        R_val = 255
    if G_val >= 255:
        G_val = 255
    if B_val >= 255:
        B_val = 255
    if R_val <= 0:
        R_val = 0
    if G_val <= 0:
        G_val = 0
    if B_val <= 0:
        B_val = 0
    if current_R != R_val: 
        print('R value:', R_val) 
    if current_G != G_val:
        print('G value:', G_val)
    if current_B != B_val:
        print('B value:', B_val)  
        
    current_R = R_val
    current_G = G_val
    current_B = B_val
    #RGB = [current_R, current_G, current_B]
    I_val = I.read_u16()
    
    if len(I_avg) <=10:
        I_avg.append(I_val)
    else:
        I_avg.append(I_avg.pop(0))
        I_avg[len(I_avg)-1] = I_val
        I_val = sum(I_avg)/len(I_avg)
        
    brighness = list(I_ratio*(255 - 255*I_val/10000) for i in light)
    brighness[0] *= current_R/255
    brighness[1] *= current_G/255
    brighness[2] *= current_B/255
    
    #print(I_avg)
    #print("Освещенность: ",I_val)
    strip.show()
    #print(brighness)
    for x in range(numpix):
        strip.set_pixel(x, brighness)
        strip.show()

    utime.sleep(0.1)

         