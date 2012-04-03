import sys
from optparse import OptionParser
import ConfigParser

# Returns OptionParser
def setupCmdOptions():
    parser = OptionParser()

    parser.add_option("-s", "--swizzles", dest="in_swizzle", default="",
                help="REQUIRED. Space separated list of swizzles e.g. -s \"RGBA BGRA ABRG\"")
    parser.add_option("-v", "--vector", dest="in_vector", default="",
                help="OPTIONAL. A vec4 to apply the swizzle to e.g. -s \"1.2 4.6 2.0 11.3\"")

    return parser

def XYZWToRGBA(character):
    if character == 'R':
        return 'X'
    elif character == 'G':
        return 'Y'
    elif character == 'B':
        return 'Z'
    elif character == 'A':
        return 'W'
    else:
        print "Unhandled channel"
        return 'F'

def IsXYZW(character):
    if character == 'X':
        return 1
    elif character == 'Y':
        return 1
    elif character == 'Z':
        return 1
    elif character == 'W':
        return 1

    return 0

# Returns an integer
def getIndex(swizzle, channel):
    index = -1
    if swizzle[channel] == 'R' or swizzle[channel] == 'X':
        index = 0
    elif swizzle[channel] == 'G' or swizzle[channel] == 'Y':
        index = 1
    elif swizzle[channel] == 'B' or swizzle[channel] == 'Z':
        index = 2
    elif swizzle[channel] == 'A' or swizzle[channel] == 'W':
        index = 3
    else:
        print "Unhandled channel"
    return index

# Returns a list
def combineSwizzle(swizzleX, swizzleY):

    srcIndex = [0,0,0,0]

    srcIndex[0] = getIndex(swizzleX, 0)
    srcIndex[1] = getIndex(swizzleX, 1)
    srcIndex[2] = getIndex(swizzleX, 2)
    srcIndex[3] = getIndex(swizzleX, 3)
    
    destIndex = [0,0,0,0]

    destIndex[0] = getIndex(swizzleY, 0)
    destIndex[1] = getIndex(swizzleY, 1)
    destIndex[2] = getIndex(swizzleY, 2)
    destIndex[3] = getIndex(swizzleY, 3)
    
    characters = 'RGBA'

    x = characters[srcIndex[destIndex[0]]]
    y = characters[srcIndex[destIndex[1]]]
    z = characters[srcIndex[destIndex[2]]]
    w = characters[srcIndex[destIndex[3]]]
    
    result = x, y, z, w

    return result

# Returns a list
def applySwizzle(swizzle, vector):
    vecsplit = vector.split()
    return vecsplit[getIndex(swizzle, 0)], " ", vecsplit[getIndex(swizzle, 1)], " ",
            vecsplit[getIndex(swizzle, 2)], " ", vecsplit[getIndex(swizzle, 3)]


# Returns void
def testCombineSwizzle():
    result = combineSwizzle('BGRA', 'ARGB')
    expected = 'A', 'B', 'G', 'R'
    if result != expected:
        print "Internal correctness test failed", "Expected ", expected, " got ", result
        sys.exit(1)

# Parse parameters
parser = setupCmdOptions()
(options, args) = parser.parse_args()

if not options.in_swizzle:
    print "Swizzle list not provided"
    sys.exit(1)

# Script accepts upper and lower case input.#
# Convert to uppercase here so we only have to deal with uppercase from here on out.
options.in_swizzle = options.in_swizzle.upper()

# Put self tests for correctness here
testCombineSwizzle()

swizzleList = options.in_swizzle.split()

accumulatedSwizzle = ['R', 'G', 'B', 'A']
for s in swizzleList:
    accumulatedSwizzle = combineSwizzle(accumulatedSwizzle, s)
    # Uncomment for debugging => print "Current swizzle is ", ''.join(accumulatedSwizzle)

finalSwizzle = ['R', 'G', 'B', 'A']

# Convert to XYZW character set if the input swizzle was in that domain.
# Only check the first character. If the input includes both XYZW and RGBA
# notation then RGBA will be used for the result.
if(IsXYZW(options.in_swizzle[0])):
    finalSwizzle[0] = XYZWToRGBA(accumulatedSwizzle[0])
    finalSwizzle[1] = XYZWToRGBA(accumulatedSwizzle[1])
    finalSwizzle[2] = XYZWToRGBA(accumulatedSwizzle[2])
    finalSwizzle[3] = XYZWToRGBA(accumulatedSwizzle[3])
else:
    finalSwizzle = accumulatedSwizzle

print "   --- RESULTS ---"

print "Swizzle =", ''.join(finalSwizzle)

if options.in_vector:
    resultVector = applySwizzle(finalSwizzle, options.in_vector)
    print "Vector =", ''.join(resultVector)

