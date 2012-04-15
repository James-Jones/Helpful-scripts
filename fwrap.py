import argparse
import os.path
import types

parser = argparse.ArgumentParser(description='File wrapper.')

parser.add_argument("-f", "--file", dest="filename", required=True, help="REQUIRED. input file")
parser.add_argument("-n", "--name", dest="arrayname", help="name of array")

options = parser.parse_args()

inputfile = open(options.filename, "r")

basename, extension = os.path.splitext(options.filename)
outputfilename = basename + ".h"

if options.arrayname:
	arrayname = options.arrayname
else:
	(head, tail) = os.path.split(options.filename);
	basetail = os.path.splitext(tail)[0]
	postfix = extension.strip('.')
	arrayname = "psz" + "_" + basetail + "_" + postfix

headerfile = "const char* " + arrayname + "[] = {\n"

lines = inputfile.readlines()

for line in lines:
	line = line[:len(line)-1];
	headerfile = headerfile + "\t\"" + line + "\"" + "\n";

headerfile = headerfile + "};\n"

# register with file system

inputfile.close()
outputfile = open(outputfilename, "w")
outputfile.write(headerfile)
outputfile.close()

