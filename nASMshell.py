#!/usr/bin/env python

import subprocess
import argparse
import signal
import os.path

def signal_handler(signal, frame):
    print "\r"
    exit()
signal.signal(signal.SIGINT, signal_handler)

#parse
raw = False
bin_mode = False
bits = "64"
path = "nasm"

parser = argparse.ArgumentParser(description = "Simple program that converts nasm syntax to machine code. Nasm is required", epilog ="Made by srakai (swientymateusz at gmail d0t com)")
parser.add_argument("-r", "--raw", type = str, help = "raw mode. Must be followed with asm instruction, (execute, print and exit)", required = False)
parser.add_argument("-b", "--binary", help = "print in binary (default print in hex)", action="store_true", required = False)
parser.add_argument("--bits", type = str, help = "x86 bits (32 or 64)", required = False)
parser.add_argument('--npath', type = str, help = "path to nasm", required = False)

args = parser.parse_args()

if args.raw:
    code = args.raw
    raw = True

if args.binary:
    bin_mode = True

if args.bits:
    if (args.bits == "64" or args.bits == "32"):
        bits = args.bits
    else:
        print "wrong bits value!"
        parser.print_help()
        exit()

if args.npath:
    path = args.npath


#temp files
infile = "/tmp/asm_gen.asm"
outfile = "/tmp/asm_gen"    

while 1:
        if (not raw):
	    code = raw_input("asm-opcode->")
            if code == "exit":
		exit()
	cmd ="echo 'BITS " + bits + "\\n"+ code +"' > " + infile +" && " + path + " -f bin -o " + outfile + " " + infile
	err_output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE).stderr.read()
       
        if os.path.exists(outfile):
            out = open(outfile, "rb").read()
        else:
            out = ""
            
        if (len(out) ==0 and (not raw) and (len(code) >0)):
            print "Wrong syntax " ,  err_output[:-1].split("error")[1][2:]     # some string magic
            continue

        if (bin_mode):
            # raw binary mode
            print out
        else:
            # hex mode
            out =  out.encode("hex")
            new = ""
            for i in range(0, len(out),2):
                new += '\\x' + out[i:i+2]
            print new 
        if (raw):
            exit()
