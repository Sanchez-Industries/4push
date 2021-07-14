#!/usr/bin/python3
#coding: utf-8
#====================================================
import os, time, json
from datetime import datetime
from base64 import b64encode as b64enc 
from base64 import b64decode as b64dec 
import argparse, base64
#==================================================
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--local-scan-extensions", type=str,
                    help="exemple: -l 'txt,csv,py,js'")
parser.add_argument("-o", "--output-file", type=str,
                    help="Set the outputfile.\nexemple: -o 'playthat.py'")
parser.add_argument("-oax", "--output-file-all-can-execute", type=str,
                    help="Set an outputfile can be execute.\nexemple: -oax '/usr/bin/playthat'")
parser.add_argument("-syco", "--symlink-dump-to-clone", type=str,
                    help="Set an outputfile script can write an clone of the symlink pre-dumped.\nexemple: -syco '/dev/sr0'")
parser.add_argument("-vcat", "--verbose-generated", action="store_true",
                    help="Enable Verbose of generated file.")
#==================================================
args = parser.parse_args()
#====================================================
def scan_specific_type_of_file(type_file,path_=""):
    os.system("ls {}*.{} > .scan".format(path_,type_file))
    with open(".scan", 'r') as f:
        data = f.read()
        f.close()
    os.remove(".scan")
    data = data.strip().split()
    return data
#====================================================
list_files = []
if args.local_scan_extensions:
    for i in args.local_scan_extensions.split(','):
        list_files = list_files + scan_specific_type_of_file(i)
#==================================================
to_install_b64 = []
for it in list_files:
    with open(it,"rb") as f:
        to_install_b64.append(b64enc(f.read()).decode())
        f.close()
#==============================
if args.symlink_dump_to_clone:
    with open(args.symlink_dump_to_clone,'rb') as f:
        data_syco = b64enc(f.read()).decode()
        f.close()
    template_script="""
#!/usr/bin/python3
#coding: utf-8
#====================================================
import os
from base64 import b64decode as b64dec 
#==============================
to_install = {}
#==============================
data_syco = "{}"
with open("syco.img",'wb') as f:
    f.write(b64dec(data_syco.encode()))
    f.close()
#==============================
#==============================
def install_all(list_bash_b64):
    for it in list_bash_b64:
        os.system(b64dec(it.encode()).decode())
    exit(0)
#==============================
install_all(to_install)
    """.format(to_install_b64,data_syco)
else:
    template_script="""
#!/usr/bin/python3
#coding: utf-8
#====================================================
import os
from base64 import b64decode as b64dec 
#==============================
to_install = {}
#==============================
def install_all(list_bash_b64):
    for it in list_bash_b64:
        os.system(b64dec(it.encode()).decode())
    exit(0)
#==============================
install_all(to_install)
    """.format(to_install_b64)
#==================================================
if args.verbose_generated:
    print(template_script)
#==============================
if args.output_file:
    with open(args.output_file,'wb') as f:
        f.write(template_script.encode())
        f.close()
#==============================
if args.output_file_all_can_execute:
    with open(args.output_file_all_can_execute,'wb') as f:
        f.write(template_script.encode())
        f.close()
    os.system("sudo chmod a+x {}".format(args.output_file_all_can_execute))
#==================================================
exit(0)