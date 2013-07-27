=begin
Rotate integer-encoded controller data by 90 degrees anti-clockwise/clockwise.
=end

DirUP = (0x0001)
DirDOWN	= (0x0004)
DirLEFT	= (0x0002)
DirRIGHT = (0x0008)

def rotateControllerACW(control)
	
	leftSh = (control << 1) & 0xF
	wrap = (control >> 3) & 0xF #3 being numbits-1
	
	return leftSh | wrap
end

def rotateControllerCW(control)
	
	leftSh = (control >> 1) & 0xF
	wrap = (control << 3) & 0xF #3 being numbits-1
	
	return leftSh | wrap
end

if ARGV[0] == "ACW"
	puts rotateControllerACW(ARGV[1].to_i)
elsif ARGV[0] == "CW"
	puts rotateControllerCW(ARGV[1].to_i)
end
