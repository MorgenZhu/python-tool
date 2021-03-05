#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: morgen

#import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
import tkinter.filedialog
import pywinio
import sys
import os
import string
import time
import atexit

#===============================================================================
'''
def init_winio():
    g_winio = pywinio.WinIO()
    return g_winio
'''
g_winio = None

def init_winio():
    global g_winio

    if g_winio is None:
            g_winio = pywinio.WinIO()
            def __clear_winio():
                    global g_winio
                    g_winio = None
            atexit.register(__clear_winio)

    return g_winio
#===========================EC Direct Access interface==========================
'''
//Port Config:
//  BADRSEL(0x200A) bit1-0  Addr    Data
//                  00      2Eh     2Fh
//                  01      4Eh     4Fh
//
//              01      4Eh     4Fh
//  ITE-EC Ram Read/Write Algorithm:
//  Addr    w   0x2E
//  Data    w   0x11
//  Addr    w   0x2F
//  Data    w   high byte
//  Addr    w   0x2E
//  Data    w   0x10
//  Addr    w   0x2F
//  Data    w   low byte
//  Addr    w   0x2E
//  Data    w   0x12
//  Addr    w   0x2F
//  Data    rw  value
'''
# Write EC RAM via EC port(2E/2F or 4E/4F)
EC_ADDR_PORT = 0x2E     #0x2E or 0x4E
EC_DATA_PORT = 0x2F     #0x2F or 0x4F

def ec_ram_read(d_index):
    winio = init_winio()
    r_data = 0
    
    #print('{0:2x} {1:2x} {2:2x}'.format(d_index, d_index>>8, d_index&0xFF))
    winio.set_port_byte(EC_ADDR_PORT, 0x2E);
    winio.set_port_byte(EC_DATA_PORT, 0x11);
    winio.set_port_byte(EC_ADDR_PORT, 0x2F);
    winio.set_port_byte(EC_DATA_PORT, d_index>>8);  # high byte addr 
    
    winio.set_port_byte(EC_ADDR_PORT, 0x2E);
    winio.set_port_byte(EC_DATA_PORT, 0x10);
    winio.set_port_byte(EC_ADDR_PORT, 0x2F);
    winio.set_port_byte(EC_DATA_PORT, d_index&0XFF);  # low byte addr 
    
    winio.set_port_byte(EC_ADDR_PORT, 0x2E);
    winio.set_port_byte(EC_DATA_PORT, 0x12);
    winio.set_port_byte(EC_ADDR_PORT, 0x2F);
    r_data = winio.get_port_byte(EC_DATA_PORT);
    
    return r_data

def ec_ram_write(d_index, data):
    winio = init_winio()
    
    winio.set_port_byte(EC_ADDR_PORT, 0x2E);
    winio.set_port_byte(EC_DATA_PORT, 0x11);
    winio.set_port_byte(EC_ADDR_PORT, 0x2F);
    winio.set_port_byte(EC_DATA_PORT, d_index>>8);  # high byte addr 
    
    winio.set_port_byte(EC_ADDR_PORT, 0x2E);
    winio.set_port_byte(EC_DATA_PORT, 0x10);
    winio.set_port_byte(EC_ADDR_PORT, 0x2F);
    winio.set_port_byte(EC_DATA_PORT, d_index&0xFF);  # low byte addr 
    
    winio.set_port_byte(EC_ADDR_PORT, 0x2E);
    winio.set_port_byte(EC_DATA_PORT, 0x12);
    winio.set_port_byte(EC_ADDR_PORT, 0x2F);
    winio.set_port_byte(EC_DATA_PORT, data);
#===============================================================================

labe_name_list = []
labe_value_list = []

#===============================================================================
#create window
root_window = Tk()
root_window.title('Battery view(zxqchongchi@gmail.com)')
root_window.geometry('1200x780')
root_window.resizable(False, False)
refresh_time_ms = 0
#===============================================================================

def ToolInit():
    '''
    // ITE IT-557x chip is DLM architecture for EC  RAM and It's support 6K/8K RAM.
    // If used RAM less  than 4K, you can access EC RAM form 0x000--0xFFF by 4E/4F IO port
    // If used RAM more than 4K, RAM address change to 0xC000
    // If you want to access EC RAM by 4E/4F IO port, you must set as follow register first
    // REG_1060[BIT7]
    '''
    EC_CHIP_ID1 = ec_ram_read(0x2000)
    EC_CHIP_ID2 = ec_ram_read(0x2001)
    if(0x55 == EC_CHIP_ID1):
    	EC_CHIP_Ver = ec_ram_read(0x1060)
    	EC_CHIP_Ver = EC_CHIP_Ver | 0x80
    	ec_ram_write(0x1060, EC_CHIP_Ver)

    ft_1 = tkFont.Font(family='Courier', size=14, weight=tkFont.BOLD)
    Label(root_window, text=("CHIP:IT-%02X%02X" % (EC_CHIP_ID1, EC_CHIP_ID2)), font=ft_1).place(x=1050, y=750)

INFO_LABLE_X = 30
INFO_LABLE_Y = 10
def dispaly_lable_name():
	labe_x = INFO_LABLE_X
	labe_y = INFO_LABLE_Y
	ft_1 = tkFont.Font(family='Courier', size=13, weight=tkFont.BOLD)
	Label_num = 0

	for labe_index in range(0, len(labe_name_list)):
		#print("%d %s" % (labe_index, labe_name_list[labe_index][4]))
		text = StringVar()
		text.set("INIT")
		labe_value_list.append(text)

		if(0 != (int(labe_name_list[labe_index][3], 16)&0x03)):
			Label(root_window, text=("%-18s :" % labe_name_list[labe_index][4]), font=ft_1).place(x=labe_x, y=labe_y)
		else:
			continue

		Label_num = Label_num+1
		if(Label_num<30):
			labe_x = INFO_LABLE_X
			labe_y = INFO_LABLE_Y + Label_num*25
		elif(Label_num<60):
			labe_x = INFO_LABLE_X+350
			labe_y = INFO_LABLE_Y+(Label_num-30)*25
		elif(Label_num<90):
			labe_x = INFO_LABLE_X+700
			labe_y = INFO_LABLE_Y+(Label_num-60)*25
		elif():
			break;

DATA_LABLE_X = INFO_LABLE_X+210
DATA_LABLE_Y = INFO_LABLE_Y
def display_info_data():
	labe_x = DATA_LABLE_X
	labe_y = DATA_LABLE_Y
	ft_1 = tkFont.Font(family='Courier', size=13)
	Label_num = 0

	for labe_index in range(0, len(labe_name_list)):
		#print("%s" % labe_value_list[labe_index].get())
		if(0 != (int(labe_name_list[labe_index][3], 16)&0x03)):
			Label(root_window, textvariable=labe_value_list[labe_index], font=ft_1).place(x=labe_x, y=labe_y)
		else:
			continue

		Label_num = Label_num+1
		if(Label_num<30):
			labe_x = DATA_LABLE_X
			labe_y = DATA_LABLE_Y + Label_num*25
		elif(Label_num<60):
			labe_x = DATA_LABLE_X+350
			labe_y = DATA_LABLE_Y+(Label_num-30)*25
		elif(Label_num<90):
			labe_x = DATA_LABLE_X+700
			labe_y = DATA_LABLE_Y+(Label_num-60)*25
		elif():
			break;


def read_special_data(labe_index):
	if('EC_Version' == labe_name_list[labe_index][0]):
		index = int(labe_name_list[labe_index][1], 16)
		ver1 = ec_ram_read(index)
		ver2 = ec_ram_read(index+1)
		ver3 = ec_ram_read(index+2)
		ver4 = ec_ram_read(index+3)

		labe_value_list[labe_index].set("%02X-%02X-%02X-%02X" % (ver1, ver2, ver3, ver4))
	elif('BAT_Current' == labe_name_list[labe_index][0]):
		bat_current = ec_ram_read(int(labe_name_list[labe_index][1], 16)) + \
						ec_ram_read(int(labe_name_list[labe_index][2], 16))*0x100

		if(bat_current>=0x8000):
			bat_current = ~bat_current
			labe_value_list[labe_index].set("-%-5d" % bat_current)
		else:
			labe_value_list[labe_index].set("%5d" % bat_current)
	elif('BAT_Temp' == labe_name_list[labe_index][0]):
		bat_temp = ec_ram_read(int(labe_name_list[labe_index][1], 16)) + \
						ec_ram_read(int(labe_name_list[labe_index][2], 16))*0x100

		bat_temp = (bat_temp*0.1)-273.15
		labe_value_list[labe_index].set("%5.1f" % bat_temp)
	elif('BAT_ManuDate' == labe_name_list[labe_index][0]):
		bat_date = ec_ram_read(int(labe_name_list[labe_index][1], 16)) + \
						ec_ram_read(int(labe_name_list[labe_index][2], 16))*0x100

		labe_value_list[labe_index].set("%d-%d-%d" % (((bat_date>>9)&0x7F)+1980, (bat_date>>5)&0x0F, bat_date&0x1F))
	else:
		labe_value_list[labe_index].set("NA")


def read_info_data():
	info_value = 0

	for labe_index in range(0, len(labe_name_list)):
		#print("%d = %s" % (labe_index, labe_value_list[labe_index].get()))
		#print("%d %s" % (labe_index, labe_name_list[labe_index][4]))

		if(0x0F == int(labe_name_list[labe_index][3], 16)): # Special data
			read_special_data(labe_index)
			continue

		if(0x04 == int(labe_name_list[labe_index][3], 16)&0x0C): # Byte data
			#print("0x%04X" % int(labe_name_list[labe_index][1], 16))
			info_value = ec_ram_read(int(labe_name_list[labe_index][1], 16))

		elif(0x08 == int(labe_name_list[labe_index][3], 16)&0x0C): # Word data
			#print("0x%04X-0x%04X" % (int(labe_name_list[labe_index][1], 16), int(labe_name_list[labe_index][2], 16)))
			info_value = ec_ram_read(int(labe_name_list[labe_index][1], 16)) + \
							ec_ram_read(int(labe_name_list[labe_index][2], 16))*0x100
			#print("%d" % info_value)
		elif(0x0C == int(labe_name_list[labe_index][3], 16)&0x0C): #Special
			continue
		else:
			info_value = 0

		if(0x01 == int(labe_name_list[labe_index][3], 16)&0x03): # Decimal data
			labe_value_list[labe_index].set(("%d" % info_value))
			#print(labe_value_list[labe_index].get())
		elif(0x02 == int(labe_name_list[labe_index][3], 16)&0x03): # Hexadecimal data
			labe_value_list[labe_index].set(("0x%04X" % info_value))
			#print(labe_value_list[labe_index].get())
		elif(0x03 == int(labe_name_list[labe_index][3], 16)&0x03): # Special data
			continue
		else:
			labe_value_list[labe_index].set("NA")

cfg_file_name = ''

def parsing_cfg_file(data_line):
	global EC_ADDR_PORT
	global EC_DATA_PORT

	if('$1' == data_line[0:2]):
		#print (data_line, end="")
		#print(data_line.split("#")[1].split("#")[0])
		str1 = data_line.split("#")[1].split("#")[0]
		#print(str1.split(","), end='')
		labe_name_list.append(str1.split(","))
	elif('$0_0' == data_line[0:4]):
		print("%X" % int(data_line.split(",")[1], 16))
	elif('$0_1' == data_line[0:4]):
		EC_ADDR_PORT = int(data_line.split(",")[1], 16)
		EC_DATA_PORT = int(data_line.split(",")[1], 16) + 1
		print("%X-%X" % (EC_ADDR_PORT, EC_DATA_PORT))
	elif('$0_2' == data_line[0:4]):
		refresh_time_ms = int(data_line.split(",")[1])
		print("%d" % refresh_time_ms)

def open_cfg_file():
	global cfg_file_name

	cfg_file_name = tkinter.filedialog.askopenfilename()
	if cfg_file_name != '':
		print("file name:" + cfg_file_name)
		try:
			with open(cfg_file_name, 'r+', encoding='utf-8') as cfg_file:
				labe_name_list.clear()
				labe_value_list.clear()

				line = cfg_file.readline()
				while line:
					parsing_cfg_file(line)
					line = cfg_file.readline()

			ToolInit()
			dispaly_lable_name()
			display_info_data()

		except IOError:
			print("无法打开文件")
			cfg_file_name = ''
	else:
		print("file name:" + "NA")
		cfg_file_name = ''


def refresh_data():
	if cfg_file_name != '':
		read_info_data()
	root_window.after(500, refresh_data)	# ms


btn = Button(root_window, text="选择配置文件", font=('Courier', 13), bd=5, command=open_cfg_file).place(x=1050, y=50)
root_window.after(500, refresh_data)
root_window.mainloop()