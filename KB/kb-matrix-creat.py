#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: morgen

#import tkinter as tk
from tkinter import *

#create window
root_window = Tk()
root_window.title('Matrix Create(zxqchongchi@gmail.com)')
root_window.geometry('1100x900')
matrix_entry_list = []
ksi_entry_list = []
kso_entry_list = []
matrix_data_list = []
KSI_SIZE = 8
KSO_SIZE = 16

Location_Code_Table = [
    [ 0,  '0x00', '       '], \
    [ 1,  '0x0E', '~`     '], \
    [ 2,  '0x16', '!1     '], \
    [ 3,  '0x1E', '@2     '], \
    [ 4,  '0x26', '#3     '], \
    [ 5,  '0x25', '$4     '], \
    [ 6,  '0x2E', '%5     '], \
    [ 7,  '0x36', '^6     '], \
    [ 8,  '0x3D', '&7     '], \
    [ 9,  '0x3E', '*8     '], \
    [10,  '0x46', '(9     '], \
    [11,  '0x45', ')0     '], \
    [12,  '0x4E', '_-     '], \
    [13,  '0x55', '+=     '], \
    [14,  '0x6A', '|(JP)  '], \
    [15,  '0x66', 'Back   '], \
    
    [16,  '0x0D', 'Tab    '], \
    [17,  '0x15', 'Q      '], \
    [18,  '0x1D', 'W      '], \
    [19,  '0x24', 'E      '], \
    [20,  '0x2D', 'R      '], \
    [21,  '0x2C', 'T      '], \
    [22,  '0x35', 'Y      '], \
    [23,  '0x3C', 'U      '], \
    [24,  '0x43', 'I      '], \
    [25,  '0x44', 'O      '], \
    [26,  '0x4D', 'P      '], \
    [27,  '0x54', '{[     '], \
    [28,  '0x5B', ']}     '], \
    #Key 29 is available on the US and not on the International Keyboard
    [29,  '0x5D', '|(US)  '], \
    [30,  '0x58', 'CapsLk '], \
    [31,  '0x1C', 'A      '], \
    
    [32,  '0x1B', 'S      '], \
    [33,  '0x23', 'D      '], \
    [34,  '0x2B', 'F      '], \
    [35,  '0x34', 'G      '], \
    [36,  '0x33', 'H      '], \
    [37,  '0x3B', 'J      '], \
    [38,  '0x42', 'K      '], \
    [39,  '0x4B', 'L      '], \
    [40,  '0x4C', ':;     '], \
    [41,  '0x52', ',      '], \
    [42,  '0x5D', '42(UK) '], \
    [43,  '0x5A', 'Enter  '], \
    [44,  '0x88', 'L-Sft  '], \
    [45,  '0x61', '45(UK) '], \
    [46,  '0x1A', 'Z      '], \
    [47,  '0x22', 'X      '], \
    
    [48,  '0x21', 'C      '], \
    [49,  '0x2A', 'V      '], \
    [50,  '0x32', 'B      '], \
    [51,  '0x31', 'N      '], \
    [52,  '0x3A', 'M      '], \
    [53,  '0x41', '<,     '], \
    [54,  '0x49', '>.     '], \
    [55,  '0x4A', '?/     '], \
    [56,  '0x51', '56(JP) '], \
    [57,  '0x89', 'R-Sft  '], \
    [58,  '0x8C', 'L-Ctl  '], \
    [59,  '0x8E', 'Fn     '], \
    [60,  '0x8A', 'L-Alt  '], \
    [61,  '0x29', 'Space  '], \
    [62,  '0x8B', 'R-Alt  '], \
    [63,  '0x00', '       '], \
    
    [64,  '0x8D', 'R-Ctl  '], \
    [65,  '0x00', '       '], \
    [66,  '0x00', '       '], \
    [67,  '0x00', '       '], \
    [68,  '0x00', '       '], \
    [69,  '0x00', '       '], \
    [70,  '0x00', '       '], \
    [71,  '0x00', '       '], \
    [72,  '0x00', '       '], \
    [73,  '0x00', '       '], \
    [74,  '0x00', '       '], \
    [75,  '0xC2', 'Ins    '], \
    [76,  '0xC0', 'Del    '], \
    [77,  '0x00', '       '], \
    [78,  '0x00', '       '], \
    [79,  '0x9A', 'Left   '], \
    
    [80,  '0x94', 'Home   '], \
    [81,  '0x95', 'End    '], \
    [82,  '0x00', '       '], \
    [83,  '0x98', 'Up     '], \
    [84,  '0x99', 'Down   '], \
    [85,  '0x96', 'PgUp   '], \
    [86,  '0x97', 'PgDn   '], \
    [87,  '0x00', '       '], \
    [88,  '0x00', '       '], \
    [89,  '0x9B', 'Right  '], \
    [90,  '0x77', 'NumLk  '], \
    [91,  '0x9C', 'Num7   '], \
    [92,  '0xA0', 'Num4   '], \
    [93,  '0xA4', 'Num1   '], \
    [94,  '0x00', '       '], \
    [95,  '0xAA', 'Num/   '], \
    
    [96,  '0x9D', 'Num8   '], \
    [97,  '0xA1', 'Num5   '], \
    [98,  '0xA5', 'Num2   '], \
    [99,  '0xA8', 'Num0   '], \
    [100, '0x9F', 'Num*   '], \
    [101, '0x9E', 'Num9   '], \
    [102, '0xA2', 'Num6   '], \
    [103, '0xA6', 'Num3   '], \
    [104, '0xA9', 'Num.   '], \
    [105, '0xA3', 'Num-   '], \
    [106, '0xA7', 'Num+   '], \
    [107, '0x00', '       '], \
    [108, '0x81', 'NumEn  '], \
    [109, '0x00', '       '], \
    [110, '0x76', 'ESC    '], \
    [111, '0x00', '       '], \
    
    [112, '0xE0', 'F1     '], \
    [113, '0xE1', 'F2     '], \
    [114, '0xE2', 'F3     '], \
    [115, '0xE3', 'F4     '], \
    [116, '0xE4', 'F5     '], \
    [117, '0xE5', 'F6     '], \
    [118, '0xE6', 'F7     '], \
    [119, '0xE7', 'F8     '], \
    [120, '0xE8', 'F9     '], \
    [121, '0xE9', 'F10    '], \
    [122, '0xEA', 'F11    '], \
    [123, '0xEB', 'F12    '], \
    [124, '0xC3', 'PrtSc  '], \
    [125, '0x7E', 'ScrLk  '], \
    [126, '0x91', 'Pause  '], \
    
    [127, '0x82', 'L-Win  '], \
    [128, '0x83', 'R-Win  '], \
    [129, '0x84', 'App    '], \
    [130, '0x00', '       '], \
    [131, '0x67', '131(JP)'], \
    [132, '0x64', '132(JP)'], \
    [133, '0x13', '133(JP)'], \
    [134, '0x00', '       '], \
    [135, '0x00', '       '], \
    [136, '0x00', '       '], \
    [137, '0x00', '       '], \
    [138, '0x00', '       '], \
    [139, '0x00', '       '], \
    [140, '0x00', '       '], \
    [141, '0x00', '       '], \
    [142, '0x00', '       ']]
                       
                       

# Each of the values of the matrix is in the range is 0-FF
def check_matrix_input(content):
    if(len(content)<=3 and len(content)>0):
        #print('{0:s}'.format(content[-1]))
        if(content[-1]>='0' and content[-1]<='9'):
            if(int(content) >= len(Location_Code_Table)):
                return False
            else:
                return True
        else:
            return False
    elif(len(content)==0):
        return True
    else:
        return False

# KSI range is 0--7
def check_ksi_input(content):
    if(len(content)==1):
        #print('{0:s}'.format(content[-1]))
        if(content[-1]>='0' and content[-1]<='7'):
            if(int(content) > 7):
                return False
            else:
                return True
        else:
            return False
    elif(len(content)==0):
        return True
    else:
        return False

# KSO range is 0--17
def check_kso_input(content):
    if(len(content)<=2 and len(content)>0):
        #print('{0:s}'.format(content[-1]))
        if((content[-1]>='0' and content[-1]<='9')):
            if(int(content) > 17):
                return False
            else:
                return True
        else:
            return False
    elif(len(content)==0):
        return True
    else:
        return False

matrix_entry_validate = root_window.register(check_matrix_input)
ksi_entry_validate = root_window.register(check_ksi_input)
kso_entry_validate = root_window.register(check_kso_input)


# creat matrix table
for column in range(0, KSI_SIZE):
    for row in range(0, KSO_SIZE):
        e1 = Entry(root_window, show=None, relief=SUNKEN, font=('Arial', 20), \
                validate='key', vcmd=(matrix_entry_validate,'%P'))
        e1.place(x = 80+row*50, y = 40+column*50, width=50, height=50)
        matrix_entry_list.append(e1)

# creat KSO table
for row in range(0, KSO_SIZE):
    Label(root_window, text='KSO-', font=('Arial', 10)).place(x=80+row*50, y=440)
    kso_default = StringVar()
    kso_default.set(str(row))
    e1 = Entry(root_window, show=None, relief=SUNKEN, font=('Arial', 12), \
            validate='key', vcmd=(kso_entry_validate,'%P'), textvariable=kso_default)
    e1.place(x = 88+row*50, y = 460, width=25, height=25)
    kso_entry_list.append(e1)

# creat KSI table
for column in range(0, KSI_SIZE):
    Label(root_window, text='KSI-', font=('Arial', 10)).place(x=47, y=40+column*50)
    ksi_default = StringVar()
    ksi_default.set(str(column))
    e1 = Entry(root_window, show=None, relief=SUNKEN, font=('Arial', 12), \
            validate='key', vcmd=(ksi_entry_validate,'%P'), textvariable=ksi_default)
    e1.place(x = 50, y = 60+column*50, width=25, height=25)
    ksi_entry_list.append(e1)

# creat text box
text_1 = Text(root_window, width=120, height=18, font=('Courier', 10))
text_1.place(x=50, y=570)


def out_put_to_text():
    text_1.delete('1.0', END)   # clean text content

    # Output to the text box
    for i in range(0, KSI_SIZE):
        text_1.insert(INSERT, '//')
        for j in range(0, KSO_SIZE):
            if(matrix_data_list[j+i*KSO_SIZE] <= len(Location_Code_Table)):
                text_1.insert(INSERT, Location_Code_Table[matrix_data_list[j+i*KSO_SIZE]][2])
            else:
                text_1.insert(INSERT, '       ')
        text_1.insert(INSERT, '\n')
        
        text_1.insert(INSERT, '  ')
        for j in range(0, KSO_SIZE):
            if(matrix_data_list[j+i*KSO_SIZE] <= len(Location_Code_Table)):
                text_1.insert(INSERT, Location_Code_Table[matrix_data_list[j+i*KSO_SIZE]][1])
                text_1.insert(INSERT, ',  ')
            else:
                text_1.insert(INSERT, '0x00,  ')
        text_1.insert(INSERT, '\n')

def out_put_to_console():
    # Output to console
    print("location code")
    for i in range(0, KSI_SIZE):
        for j in range(0, KSO_SIZE):
             print("%3d, " % matrix_data_list[j+i*KSO_SIZE], end='')
        print("")

    print("")
    print("scan code")
    print("const unsigned char code Rc_ROM_Tables[] =")
    print("{")
    for i in range(0, KSI_SIZE):
        print("//", end='')
        for j in range(0, KSO_SIZE):
            if(matrix_data_list[j+i*KSO_SIZE] <= len(Location_Code_Table)):
                print("%6s" % Location_Code_Table[matrix_data_list[j+i*KSO_SIZE]][2], end='')
            else:
                print("      ", end='')
        print("")
        
        print("  ", end='')
        for j in range(0, KSO_SIZE):
            if(matrix_data_list[j+i*KSO_SIZE] <= len(Location_Code_Table)):
                print("%s,  " % Location_Code_Table[matrix_data_list[j+i*KSO_SIZE]][1], end='')
            else:
                print("0x00,  ", end='')
        print("")
    print("};")
    
def get_matrix_data():
    matrix_data_list.clear()    # clean list

    for index in range(0, KSI_SIZE*KSO_SIZE):
        for i in range(0, KSI_SIZE):
            column = int(ksi_entry_list[i].get())
            for j in range(0, KSO_SIZE):
                row = int(kso_entry_list[j].get())
                if(index == (row+column*KSO_SIZE)):
                    break;
            if(index == (row+column*KSO_SIZE)):
                    break;
        
        if(len(matrix_entry_list[j+i*KSO_SIZE].get())>0):
            #print('%s' % matrix_entry_list[j+i*KSO_SIZE].get())
            table_data = int(matrix_entry_list[j+i*KSO_SIZE].get(), 10)
        else:
            table_data = 0
        
        #print('index={0:02X} matrix_data={1:02X}'.format(index, table_data))
        matrix_data_list.append(table_data)

    #out_put_to_console()
    out_put_to_text()

Button(root_window, text ="Convert", font=('Arial', 14), \
        command = get_matrix_data).place(x=950, y=210)

Label(root_window, text='KSI range is [0,7]', font=('Arial', 10)).place(x=20, y= 15)
Label(root_window, text='KSO range is [0,15]', font=('Arial', 10)).place(x=880, y= 460)
Label(root_window, text='1. Fill in KSI and KSO according to the actual SCH', font=('Arial', 10)).place(x=50, y= 500)
Label(root_window, text='2. Fill in matrix code according to the KB matrix diagram', font=('Arial', 10)).place(x=50, y= 520)
Label(root_window, text='3. The matrix array is generated in the text box below', font=('Arial', 10)).place(x=50, y= 540)

root_window.mainloop()









