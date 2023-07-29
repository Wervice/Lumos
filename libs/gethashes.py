import gzip
import tarfile
import os
import platform
import time

def init_processbar(name):
#    print(name+" 0%                ")
#    return name
    pass

def set_proccessbar(name, value):
#    time.sleep(0.1)
#    if platform.system == "Windows":
#        os.system("cls")
#    elif platform.system == "Linux":
#        os.system("clear")
#    strc = ""
#    for i in range(value):
#        strc += "▮"
#   print(name+" "+str(value * 10)+"% "+strc)
    pass

def get_hashes_names(file):
    bar = init_processbar("Virus Scanner")
    if file == "main":
        bin_data = open("main.cvd", "rb").read()
    elif file == "daily":
        bin_data = open("daily.cvd", "rb").read()
    else:
        print("This file can't be parsed")
        exit()
    i = 0
    bin_data_clean = bytes()
    end_data = bytearray()  # Changed from bytes() to bytearray()
    val = bin_data[i]
    set_proccessbar(bar, 1)
    while val != 139 and bin_data[i + 1] != 8 and bin_data[i + 2] != 0:
        i += 1
        val = bin_data[i]
    i -= 1
    while i != len(bin_data):  # Changed the condition from val != None to i >= 0
        end_data.append(bin_data[i])  # Changed += to append()
        i += 1
    set_proccessbar(bar, 2)
    open("clamav.tar.tmp", "wb").write(gzip.decompress(end_data))
    set_proccessbar(bar, 3)
    tarfile_dat = tarfile.open("clamav.tar.tmp", "r")
    tarfile_dat.extractall(".\\clamavdb\\")
    tarfile_dat.close()
    set_proccessbar(bar, 4)
    if file == "main":
        lines = open("clamavdb/main.hdb", "r").read().split("\n")
    else:
        lines = open("clamavdb/daily.hdb", "r").read().split("\n")
    set_proccessbar(bar, 5)
    hashes_hdb = []
    hashes_hdb_name = []
    i = 0
    for line in lines:
        split_line = line.split(":")
        if len(split_line) > 1:
            hashes_hdb.append(split_line[0])
            hashes_hdb_name.append(split_line[2])
    set_proccessbar(bar, 6)
    if file == "main":
        lines = open("clamavdb/main.hsb", "r").read().split("\n")
    else:
        lines = open("clamavdb/daily.hdb", "r").read().split("\n")
    hashes_hsb = []
    hashes_hsb_name = []
    set_proccessbar(bar, 7)
    i = 0
    for line in lines:
        split_line = line.split(":")
        if len(split_line) > 1:
            hashes_hsb.append(split_line[0])
            hashes_hsb_name.append(split_line[2])
    set_proccessbar(bar, 8)
    hashes_final = []
    hashes_final.extend(hashes_hdb)
    hashes_final.extend(hashes_hsb)
    names_final = []
    names_final.extend(hashes_hdb_name)
    names_final.extend(hashes_hsb_name)
    set_proccessbar(bar, 9)
    hashes_main_writer = open("hashes_main.txt", "a")
    for hash in hashes_final:
        hashes_main_writer.write(hash+"\n")
    hashes_main_writer.close()
    names_main_writer = open("names_main.txt", "a")
    for name in names_final:
        names_main_writer.write(name+"\n")
    names_main_writer.close()
    os.remove(os.getcwd()+"/clamav.tar.tmp")
    if platform.system == "Windows":
        os.system("rmdir /s "+os.getcwd()+"\clamavdb /q")
    elif platform.system == "Linux":
        os.system("rm -r -f -d "+os.getcwd()+"\clamavdb")
    open("last_virus_update.txt", "w").write(time.strftime("%Y-%m-%d @ %H:%M"))
    set_proccessbar(bar, 10)