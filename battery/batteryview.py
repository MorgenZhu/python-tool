#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: morgen

#import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
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

labe_name_list = [
['EC_Version', '        0xC410', '    0x0000', '    0x0F', '    EC_Version'],
['BAT_mAormW', '        0xC900', '    0xC901', '    0x0F', '    BAT_Data_Unit'],
['BAT_AC_State', '      0xC460', '    0xC460', '    0x0F', '    BAT_AC_State'],
['BAT_FCCFlag', '       0xC914', '    0xC915', '    0x0F', '    BAT_FC_Status'],
['BAT_RealRSOC', '      0xC000', '    0xC000', '    0x0F', '    BAT_RealRSOC'],
['BAT_ManuName', '      0xC930', '    0xC000', '    0x0F', '    BAT_ManuName'],
['BAT_DeviceName', '    0xC940', '    0xC000', '    0x0F', '    BAT_DevName'],
['BAT_DevChemistry', '  0xC920', '    0xC000', '    0x0F', '    BAT_DevChem'],
['BAT_ManuDate', '      0xC91C', '    0xC91D', '    0x0F', '    BAT_ManuDate'],
['BAT_SerialNum', '     0xC91E', '    0xC91F', '    0x0F', '    BAT_S-Num'],
['Data_01', '    0xC906', '    0xC907', '    0x0D', '    BAT_Current'],
['Data_02', '    0xC904', '    0xC905', '    0x0D', '    BAT_Voltage'],
['Data_03', '    0xC90C', '    0xC90D', '    0x0D', '    BAT_RMC'],
['Data_04', '    0xC90E', '    0xC90F', '    0x0D', '    BAT_FCC'],
['Data_05', '    0xC908', '    0xC909', '    0x0D', '    BAT_RSOC'],
['Data_06', '    0xC90A', '    0xC90B', '    0x0D', '    BAT_ASOC'],
['Data_07', '    0xC91A', '    0xC91B', '    0x0D', '    BAT_DV'],
['Data_08', '    0xC918', '    0xC919', '    0x0D', '    BAT_DC'],
['Data_09', '    0xC902', '    0xC903', '    0x0D', '    BAT_Temp'],
['Data_10', '    0xC916', '    0xC917', '    0x0D', '    BAT_CycleCount'],
['Data_11', '    0xC910', '    0xC911', '    0x0D', '    BAT_CC'],
['Data_12', '    0xC912', '    0xC913', '    0x0D', '    BAT_CV'],
['Data_13', '    0xC915', '    0xC000', '    0x0D', '    BAT_Status_H'],
['Data_14', '    0xC914', '    0xC000', '    0x0D', '    BAT_Status_L'],
['Data_15', '    0xC982', '    0xC983', '    0x0D', '    CHARGE_Voltage'],
['Data_16', '    0xC984', '    0xC985', '    0x0D', '    CHARGE_Current'],
['Data_17', '    0xC980', '    0xC981', '    0x0D', '    INPUT_Current'],
['Data_20', '    0xC8B6', '    0xC8B7', '    0x0F', '    CHARGE_OP0'],
['Data_21', '    0xC8B8', '    0xC8B9', '    0x0F', '    CHARGE_OP1'],
['Data_22', '    0xC8BA', '    0xC8BB', '    0x0F', '    CHARGE_OP2'],
['Data_23', '    0xC8BC', '    0xC8BD', '    0x0F', '    CHARGE_OP3'],
['Data_24', '    0xC8B8', '    0xC8B9', '    0x0F', '    CHARGE_OP4'],
['Data_25', '    0xC8BA', '    0xC8BB', '    0x0F', '    CHARGE_OP5'],
['Data_26', '    0xC8BC', '    0xC8BD', '    0x0F', '    CHARGE_OP6'],
['Data_27', '    0xC8BE', '    0xC8BF', '    0x0F', '    PROHOT_OP0'],
['Data_28', '    0xC8C0', '    0xC8C1', '    0x0F', '    PROHOT_OP1'],
['Data_29', '    0xC8C2', '    0xC8C3', '    0x0F', '    PROHOT_Status'],
['Data_30', '    0xC8CA', '    0xC8CB', '    0x0F', '    ChargerStatus'],
['Data_31', '    0xC8B6', '    0xC8B7', '    0x0F', '    Hex_Dat_01'],
['Data_32', '    0xC8B8', '    0xC8B9', '    0x0F', '    Hex_Dat_02'],
['Data_33', '    0xC8BA', '    0xC8BB', '    0x0F', '    Hex_Dat_03'],
['Data_34', '    0xC8BC', '    0xC8BD', '    0x0F', '    Hex_Dat_04'],
['Data_35', '    0xC8B8', '    0xC8B9', '    0x0F', '    Hex_Dat_05'],
['Data_36', '    0xC8BA', '    0xC8BB', '    0x0F', '    Hex_Dat_06'],
['Data_37', '    0xC8BC', '    0xC8BD', '    0x0F', '    Hex_Dat_07'],
['Data_38', '    0xC8BE', '    0xC8BF', '    0x0F', '    Hex_Dat_08'],
['Data_39', '    0xC8C0', '    0xC8C1', '    0x0F', '    Hex_Dat_09'],
['Data_40', '    0xC417', '    0x0000', '    0x0F', '    CHG_Temp_NTC'],
['Data_41', '    0xC418', '    0x0000', '    0x0F', '    CPU_NTC'],
['Data_42', '    0xC419', '    0x0000', '    0x0F', '    SEN1'],
['Data_43', '    0xC41A', '    0x0000', '    0x0F', '    Memory_NTC'],
['Data_44', '    0xC41B', '    0x0000', '    0x0F', '    CPU_DTS'],
['Data_45', '    0xC41C', '    0x0000', '    0x0F', '    NTC_DDR'],
['Data_46', '    0xC41D', '    0x0000', '    0x0F', '    NTC_GPU'],
['Data_47', '    0xC41E', '    0x0000', '    0x0F', '    V5P0A_NTC'],
['Data_48', '    0xC41F', '    0x0000', '    0x0F', '    NTC_CPU'],
['Data_49', '    0xC41F', '    0x0000', '    0x0F', '    NTC_CPU_Back'],
['Data_50', '    0xC41F', '    0x0000', '    0x0F', '    Dec_Dat_01'],
['Data_51', '    0xC41F', '    0x0000', '    0x0F', '    Dec_Dat_02'],
['Data_52', '    0xC41F', '    0x0000', '    0x0F', '    Dec_Dat_03'],
['Data_53', '    0xC41F', '    0x0000', '    0x0F', '    Dec_Dat_04'],
['Data_54', '    0xC41F', '    0x0000', '    0x0F', '    Dec_Dat_05'],
['Data_55', '    0xC41F', '    0x0000', '    0x0F', '    Dec_Dat_06'],
['Data_56', '    0xC41F', '    0x0000', '    0x0F', '    Dec_Dat_07'],
['Data_57', '    0xC41F', '    0x0000', '    0x0F', '    Dec_Dat_08'],
['Data_58', '    0xC41F', '    0x0000', '    0x0F', '    Dec_Dat_09'],
['Data_59', '    0xC41F', '    0x0000', '    0x0F', '    Dec_Dat_10'],
['OS_AC             ', '    0x0000', '    0x0000', '    0x00', '    OS_AC_Status'],
['OS_BAT            ', '    0x0000', '    0x0000', '    0x00', '    OS_BAT_Status'],
['OS_BAT_Charge     ', '    0x0000', '    0x0000', '    0x00', '    OS_BAT_Charge'],
['OS_BAT_Discharge  ', '    0x0000', '    0x0000', '    0x00', '    OS_BAT_Discha'],
['OS_BAT_Remtime    ', '    0x0000', '    0x0000', '    0x00', '    OS_BAT_Remtime'],
['OS_BAT_FCC        ', '    0x0000', '    0x0000', '    0x00', '    OS_BAT_FCC'],
['OS_BAT_RMC        ', '    0x0000', '    0x0000', '    0x00', '    OS_BAT_RMC'],
['OS_BAT_Current    ', '    0x0000', '    0x0000', '    0x00', '    OS_BAT_Current'],
['OS_BAT_RSOC       ', '    0x0000', '    0x0000', '    0x00', '    OS_BAT_RSOC'],
['OS_BAT_Alert1_Low ', '    0x0000', '    0x0000', '    0x00', '    OS_BAT_Low'],
['OS_BAT_Alert1_War ', '    0x0000', '    0x0000', '    0x00', '    OS_BAT_War'],
]

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
		if(0 != (int(labe_name_list[labe_index][3], 16)&0x03)):
			Label(root_window, text=labe_value_list[labe_index], font=ft_1).place(x=labe_x, y=labe_y)
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

def read_cfg_file():
	try:
		with open('./batteryview.cfg', 'r+', encoding='utf-8') as cfg_file:
			line = cfg_file.readline()
			labe_name_list.clear()
			while line:
				parsing_cfg_file(line)
				line = cfg_file.readline()
	except IOError:
		print("配置文件不存在,载入默认配置...")

def read_special_data(labe_index):
	if('EC_Version' == labe_name_list[labe_index][0]):
		index = int(labe_name_list[labe_index][1], 16)
		ver1 = ec_ram_read(index)
		ver2 = ec_ram_read(index+1)
		ver3 = ec_ram_read(index+2)
		ver4 = ec_ram_read(index+3)

		labe_value_list.append("%02X-%02X-%02X-%02X" % (ver1, ver2, ver3, ver4))
	else:
		labe_value_list.append('NA')

def read_info_data():
	labe_value_list.clear()
	info_value = 0

	for labe_index in range(0, len(labe_name_list)):
		if(0x0F == int(labe_name_list[labe_index][3], 16)):
			read_special_data(labe_index)
			continue

		if(0x04 == int(labe_name_list[labe_index][3], 16)&0x0C): # Byte data
			#print("0x%04X" % int(labe_name_list[labe_index][1], 16))
			info_value = ec_ram_read(int(labe_name_list[labe_index][1], 16))

		elif(0x08 == int(labe_name_list[labe_index][3], 16)&0x0C): # Word data
			print("0x%04X-0x%04X" % (int(labe_name_list[labe_index][1], 16), int(labe_name_list[labe_index][2], 16)))
			info_value = ec_ram_read(int(labe_name_list[labe_index][1], 16)) + \
							ec_ram_read(int(labe_name_list[labe_index][2], 16))*0x100
			print("%d" % info_value)
		else:
			info_value = 0


		if(0x01 == int(labe_name_list[labe_index][3], 16)&0x03): # Decimal data
			#print(hex(info_value))
			labe_value_list.append(("%d" % info_value))
		elif(0x02 == int(labe_name_list[labe_index][3], 16)&0x03): # Hexadecimal data
			#print(hex(info_value))
			labe_value_list.append(("0x%04X" % info_value))
		else:
			labe_value_list.append("NA")

def refresh_data():
	read_info_data()
	display_info_data()
	root_window.after(500, refresh_data)	# ms


read_cfg_file()
dispaly_lable_name()
ToolInit()
read_info_data()
display_info_data()

root_window.after(500, refresh_data)
root_window.mainloop()