import argparse
import os.path
import types

parser = argparse.ArgumentParser(description='File wrapper.')

parser.add_argument("-f", "--file", dest="filename", required=True, help="REQUIRED. input file")
parser.add_argument("-n", "--name", dest="cvarname", help="name of the generated C string variable")
parser.add_argument("-b", "--binary", dest="bBinary", action='store_true', help="output char array instead of string")

options = parser.parse_args()

if(options.bBinary):
    inputfile = open(options.filename, "rb")
else:
    inputfile = open(options.filename, "r")

basename, extension = os.path.splitext(options.filename)
if extension:
	outputfilename = basename + "_" + extension.strip('.') + ".h"
else:
	outputfilename = basename + ".h"

if options.cvarname:
	cvarname = options.cvarname
else:
	(head, tail) = os.path.split(options.filename);
	basetail = os.path.splitext(tail)[0]
	postfix = extension.strip('.')
	if postfix:
		cvarname = "psz" + "_" + basetail + "_" + postfix
	else:
		cvarname = "psz" + "_" + basetail

if options.bBinary:
    headerfile = "const unsigned char " + cvarname + " [] = {\n"

    headerfile = headerfile;

    chars = inputfile.read()

    for char in chars:
	    headerfile = headerfile + str(ord(char)) + ",\n"

    headerfile = headerfile + "};\n"

else:
    headerfile = "const char* " + cvarname + " = {\n"

    lines = inputfile.readlines()

    headerfile = headerfile + "\"";
    for line in lines:
        line = line[:len(line)-1];

        processed = line.replace('\"', '\\"');

        headerfile = headerfile + "\t" + processed + "\\" + "\n";

    headerfile = headerfile + "\"};\n"

# register with file system

inputfile.close()
outputfile = open(outputfilename, "w")
outputfile.write(headerfile)
outputfile.flush()
outputfile.close()

