from optparse import OptionParser
import os.path
import types

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="input file", metavar="FILE")
(options, args) = parser.parse_args()

if type(options.filename) is types.NoneType : print("file not specified"); exit()

basename, extension = os.path.splitext(options.filename)

print("File: " + basename)
print("Ext: " + extension)

(head, tail) = os.path.split(options.filename);

print("Head: " + head)
print("Tail: " + tail)

basetail = os.path.splitext(tail)[0]
print("Tail without ext: " + basetail)

outputfilename = basename + ".h"
inputfile = open(options.filename, "r")
arrayname = "psz" + basetail + "_" + extension

# numlines = len(inputfile.readlines());

headerfile = "#include <memfilesys.h>\n\n"

headerfile = headerfile + "const char* " + arrayname + "[] = {\n"

line = inputfile.readline()
linelen = len(line);
line = line[:linelen-1];
while line:
    headerfile = headerfile + "\"" + line + "\"\n";
    line = inputfile.readline();

headerfile = headerfile + "\n}\n"

# register with file system

inputfile.close()
outputfile = open(outputfilename, "w")
outputfile.write(headerfile)
outputfile.close()

