=begin
Rotate integer-encoded controller data by 90 degrees anti-clockwise/clockwise.
=end

DirUP = (0x0001)
DirDOWN	= (0x0004)
DirLEFT	= (0x0002)
DirRIGHT = (0x0008)
	
def rotateControllerACW(control)
	
	shift = (control << 1) & 0xF
	wrap = (control >> 3) & 0xF #3 being numbits(4)-rotate_amount(1)
	
	return shift | wrap
end

def rotateControllerCW(control)
	
	shift = (control >> 1) & 0xF
	wrap = (control << 3) & 0xF #3 being numbits(4)-rotate_amount(1)
	
	return shift | wrap
end

if ARGV[0] == "ACW"
	puts rotateControllerACW(ARGV[1].to_i)
elsif ARGV[0] == "CW"
	puts rotateControllerCW(ARGV[1].to_i)
end
