import pyautogui
import time


def move_mouse():
    while True:

        pyautogui.moveTo(509, 200, 2)
        pyautogui.moveTo(509, 600, 2)
        time.sleep(60)

def refresh_browser1():

    while True:

        pyautogui.click((509, 66))
        pyautogui.hotkey('f5')    
        time.sleep(15)

        pyautogui.click((699, 66))
        pyautogui.hotkey('f5')    
        time.sleep(15)

        pyautogui.click((893, 66))
        pyautogui.hotkey('f5')    
        time.sleep(15)

        pyautogui.click((1060, 66))
        pyautogui.hotkey('f5')    
        time.sleep(15)

        pyautogui.click((1267, 66))
        pyautogui.hotkey('f5')    
        time.sleep(15)

        pyautogui.click((1441, 66))
        pyautogui.hotkey('f5')    
        time.sleep(15)

        pyautogui.click((1600, 66))
        pyautogui.hotkey('f5')    
        time.sleep(15)


def refresh_browser2():

    pyautogui.moveTo(1100, 500, duration=2)
    pyautogui.moveTo(1000, 500, duration=2)

    img_dir = 'D:\\OneDrive - ITG Technologies\Documents\\_SORBA\Development\\_Scripts\\'
    imgs = ['refresh_btn.PNG', 'refresh_btn2.PNG']

    try:
        for img in imgs:
            print('Looking for image '+img)
            pos = pyautogui.locateCenterOnScreen(img_dir+img)
            if pos == None:
                print('Could not find image '+img)
                continue
            else:
                print('Image '+img+' found!')
                time.sleep(15)
                pyautogui.click(pos)
                break
        
    except Exception as e:
        print(e,':( ')


def game_name():
    img_dir = 'D:\\OneDrive - ITG Technologies\Documents\\_SORBA\Development\\_Scripts\\'
    name = pyautogui.prompt(text='', title='name' , default='')
    
    pyautogui.hotkey('win', 'r')    # open
    pyautogui.write('mspaint')      # type mspaint (MS Paint)
    pyautogui.press('enter')        # press the Enter key
    
    #pos = pyautogui.locateCenterOnScreen(img_dir+'paint_text_icon.PNG')
    #time.sleep(1)
    pyautogui.click(538,201, 1)    # click text icon
    pyautogui.click(538,201, 1)    # click text icon
    pyautogui.click(538,201, 1)    # click text icon
    
    pyautogui.moveTo(240,500, 1)
    pyautogui.dragTo(1000, 800, button='left')
    
    pyautogui.write('...', 0.25)      # type mspaint (MS Paint)
  
    #pos = pyautogui.locateCenterOnScreen(img_dir+'paint_font_icon.PNG')
    #time.sleep(1)
    pyautogui.click(369,235, 1)    # click font size icon
    pyautogui.write('72', 0.25)          # click font size 72 
    pyautogui.press('enter')
    
    pyautogui.click(812,190, 1)    # click red font color
    pyautogui.click(812,190, 1)    # click red font color
    pyautogui.click(812,190, 1)    # click red font color
    
    pyautogui.click(500,600, 1)

    pyautogui.write(name.upper()+' \n es un animal!'.lower(), 0.25)      # type mspaint (MS Paint)
    
    

if __name__ == '__main__':
    
    # game_name()
    move_mouse()
