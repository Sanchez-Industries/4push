#!/usr/bin/python3
#coding: utf-8 
#==================================================
import hashlib, json, os
import argparse, base64
#==================================================
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--push-version-level", type=str,
                    help="X.Y.Z in the order is that: (MAJOR/MINOR/CORRECTIVE), so choose the level, it's corrective by defaults.")
parser.add_argument("-Ni", "--not-increments", action="store_true",
                    help="X.Y.Z increments can disable because is enable by defaults.")
parser.add_argument("-bf", "--beta-flag", action="store_true",
                    help="set True the beta flag in informations about the node.")
parser.add_argument("-nbf", "--no-beta-flag", action="store_true",
                    help="set False the beta flag in informations about the node.")
parser.add_argument("-namenode", "--set-node-name", type=str,
                    help="set the name of the node.")
parser.add_argument("-namehuman", "--set-maintainer-name", type=str,
                    help="set the name of humans maintain the service in front of their screen.")
parser.add_argument("-resetv", "--reset-version", action="store_true",
                    help="set the version code to zero (for X.Y.Z).")
parser.add_argument("-geth", "--get-print-hash", action="store_true",
                    help="Print the hash of files.")
parser.add_argument("-initial", "--init-all", action="store_true",
                    help="Initialisation of all 4push-files in current.")
parser.add_argument("-initS", "--init-scan-file", action="store_true",
                    help="Initialisation of scan 4push-files in current.")
parser.add_argument("-initJ", "--init-json-conf", action="store_true",
                    help="Initialisation of json 4push-files in current.")
#parser.add_argument("-U", "--update-for-last", action="store_true",
#                    help="Update & reinstall or the result are an upgrade.(igniore and not execute other params)")
#==================================================
args = parser.parse_args()
#==============================
default_json, default_txt = "/var/4push/defaults/4push.json.b64",  "/var/4push/defaults/4push.txt.b64"
with open(default_json,'rb') as f:
    default_json = json.loads(base64.b64decode(f.read()))
    f.close()
with open(default_txt,'rb') as f:
    default_txt = base64.b64decode(f.read()).decode()
    f.close()
#==============================
#init_json_conf,args.init_scan_file
if args.init_all or args.init_json_conf:
    with open("4push.json",'wb') as f:
        f.write(json.dumps(default_json,indent=4).encode())
        f.close()
if args.init_all or args.init_scan_file:
    with open("4push.txt",'wb') as f:
        f.write(default_txt.encode())
        f.close()
#==============================
#update_code=None
#if args.update_for_last:
#    os.system(base64.b64decode(update_code.encode()).decode())
#    exit(0)
#==============================
if args.set_node_name:
    node_name = args.set_node_name
else:
    node_name = None
    #==============================
if args.set_maintainer_name:
    maintainer_name = args.set_maintainer_name
else:
    maintainer_name = None
#==============================
if args.beta_flag and args.no_beta_flag:
    print("ERROR: NEED TO CHOOSE( --beta-flag or --no-beta-flag ) AND NOT ENABLE BOTH.\nEXITING...")
    exit(0)
beta_flag = None
if args.beta_flag:
    beta_flag = True
elif args.no_beta_flag:
    beta_flag = False
#==============================
if args.not_increments:
    not_increments = True
else:
    not_increments = False
#==============================
if args.push_version_level:
    level_version = args.push_version_level.upper()
else:
    level_version = None
#================================================== 
#FUNCTIONS
def filter_no_smoke(strarg):
    out = ""
    if type(strarg) == str:
        for i in strarg:
            if i in ".0123456789":
                out = out + i 
    return out
#==================================================
def versionXYZ_decode(str_version_code):
    str_version_code = filter_no_smoke(str_version_code).split(".")
    return {
        "MAJOR": int(str_version_code[0]),
        "MINOR": int(str_version_code[1]),
        "CORRECTIVE": int(str_version_code[2])
    }
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
def read_list2scan_target(pathfile="4push.txt"):
    with open(pathfile,'r') as f:
        data = f.read().strip().split("\n")
        l1 = data[0].split(",")
        l2 = data[1:]
        f.close()
    return {
        "list_types": l1,
        "list_direct": l2
    }
#====================================================
#==================================================
#CLASS
class Far4Push(object):
    #==============================
    def __init__(self,VERSION_INC_LEVEL="CORRECTIVE",not_increments=False,reset_version=None):
        self._4push_json_data = self.readjsonfile("4push.json")
        self.signatures = self.extract_originals_build_signatures()
        if reset_version: 
            self.version_code = {
                "MAJOR": 0,
                "MINOR": 0,
                "CORRECTIVE": 0
                }
        else:
            self.version_code = versionXYZ_decode(self.extract_version_code())
        if not not_increments: self.increment_version(VERSION_INC_LEVEL)
        self.make_originals_build_signatures()
    #==============================
    #==============================
    def make_originals_build_signatures(self):
        self.save()
        ltsfiles = self.scan_all_need()
        self.signatures={}
        for i in ltsfiles:
            with open(i,'rb') as f:
                self.signatures[i] = hashlib.sha512(f.read()).hexdigest()
                f.close()
        self.setter_originals_build_signatures(self.signatures)
    #==============================
    #==============================
    def scan_all_need(self):
        lst = read_list2scan_target()
        flst = []
        for i in lst["list_types"]:
            flst = flst + scan_specific_type_of_file(i)
        flst = flst + lst["list_direct"]
        return flst
    #==============================
    #==============================
    def readjsonfile(self,filepath):
        with open(filepath, 'rb') as f:
            data = json.loads(f.read())
            f.close()
        return data
    #==============================
    #==============================
    def extract_version_code(self):
        return self._4push_json_data["about"]["node"]["version"]
    #==============================
    def extract_node_name(self):
        return self._4push_json_data["about"]["node"]["name"]
    #==============================
    def extract_node_beta_flag(self):
        return self._4push_json_data["about"]["node"]["beta"]
    #==============================
    def extract_maintainer_name(self):
        return self._4push_json_data["about"]["maintainer"]["name"]
    #==============================
    def extract_maintainer_email(self):
        return self._4push_json_data["about"]["maintainer"]["email"]
    #==============================
    def extract_originals_build_signatures(self):
        return self._4push_json_data["about"]["originals-build-signatures"]
    #==============================
    #==============================
    #==============================
    def setter_node_name(self,data):
        self._4push_json_data["about"]["node"]["name"] = data
    #==============================
    def setter_node_beta_flag(self,data):
        self._4push_json_data["about"]["node"]["beta"] = data
    #==============================
    def setter_maintainer_name(self,data):
        self._4push_json_data["about"]["maintainer"]["name"] = data
    #==============================
    def setter_maintainer_email(self,data):
        self._4push_json_data["about"]["maintainer"]["email"] = data
    #==============================
    def setter_originals_build_signatures(self,data):
        self._4push_json_data["about"]["originals-build-signatures"] = data
    #==============================
    #==============================
    def increment_version(self,level):
        if level in self.version_code.keys():
            self.version_code[level] += 1
        else:
            print("ERROR ON VERSION LEVEL CODE NAME!")
            exit(-1)
        self.save()
    #==============================
    def save(self,filepath="4push.json"):
        #save version code
        self._4push_json_data["about"]["node"]["version"] = ".".join([str(self.version_code["MAJOR"]),str(self.version_code["MINOR"]),str(self.version_code["CORRECTIVE"])])
        with open(filepath,'wb') as f:
            f.write(json.dumps(self._4push_json_data,indent=4).encode())
            f.close()
#==================================================
#MAIN
if level_version != None:
    F4P = Far4Push(level_version,not_increments,args.reset_version)
else:
    F4P = Far4Push(not_increments=not_increments,reset_version=args.reset_version)
if not_increments == True:
    print("Version code unchanged. is actually : {}".format(F4P.extract_version_code()))
else:
    print("The version code updated! it's now : {}".format(F4P.extract_version_code()))
    
#==============================
print("Beta flag: {}".format(F4P.extract_node_beta_flag()))
if beta_flag == None:
    print("betaflag unchanged.")
else:
    F4P.setter_node_beta_flag(beta_flag)
    print("The beta flag is now: ( {} )".format(F4P.extract_node_beta_flag()))
#==============================
#==============================
print("Node name: {}".format(F4P.extract_node_name()))
if node_name == None:
    print("Node name unchanged.")
else:
    F4P.setter_node_name(node_name)
    print("The node name is now: ( {} )".format(F4P.extract_node_name()))
#==============================
#==============================
print("Maintainer name: {}".format(F4P.extract_maintainer_name()))
if maintainer_name == None:
    print("Maintainer name unchanged.")
else:
    F4P.setter_maintainer_name(maintainer_name)
    print("The maintainer name is now: ( {} )".format(F4P.extract_maintainer_name()))
#==============================
#==============================
F4P.save()
#==================================================
if args.get_print_hash:
    signatures = F4P.extract_originals_build_signatures()
    print("{}\t|\t{}".format((128-19)*" "+"Signature (SHA-512)","File"))
    for k,v in signatures.items():
        print ("{}\t|\t{}".format(v,k))
#==================================================