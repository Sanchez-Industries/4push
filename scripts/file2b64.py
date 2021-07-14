#!/usr/bin/python3
#coding: utf-8
#==============================
import argparse
from base64 import b64encode as b64enc
#==================================================
parser = argparse.ArgumentParser()
parser.add_argument("input_file", type=str,
                    help="Input file need to be converted.")
parser.add_argument("-o", "--output-file", type=str,
                    help="Output file need to get result(By default overwrite!).")
#==================================================
args = parser.parse_args()
#==============================
def main(input_file, output_file=None):
    data = ""
    with open(input_file,'rb') as f:
        if output_file:
            with open(output_file,'wb') as f2:
                f2.write(b64enc(f.read()))
                f2.close()
            exit(0)
        else:
            data=b64enc(f.read())
        f.close()
    with open(input_file,'wb') as f:
        f.write(data)
#==============================
main(args.input_file, args.output_file)