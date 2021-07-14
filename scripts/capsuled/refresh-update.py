#!/usr/bin/python3
#coding: utf-8
#====================================================
import os
from base64 import b64decode as b64dec 
#==============================
to_install = [
    None
    ]
#==============================
def install_all(list_bash_b64):
    for it in list_bash_b64:
        os.system(b64dec(it.encode()).decode())
    exit(0)
#==============================
install_all(to_install)