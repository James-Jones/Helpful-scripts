=begin
Write a function to generate a checksum for an area of memory.
This type of function can easily be used to verify such things as data load/save etc.
=end

def checksum(buffer)

	table = Array.new(256) { |index|
		crc = index
		8.times do |k|
			if (crc & 0x1) != 0
				crc = 0xEDB88320 ^ (crc >> 1)
			else
				crc = crc >> 1
			end
		end
		crc #final W
	}
	
	result = 0xFFFFFFFF
	
	buffer.each_byte { | bufferItem |
		result = table[(result ^ bufferItem) & 0xFF] ^ (result >> 8);
	}
	
	return result
end

#Checksum of file contents
if ARGV.length == 2 and ARGV[0]=="--file" && File.file?(ARGV[1])
	File.open(ARGV[1], "r") { |file| puts checksum(file.gets) }
#Checksum of command line argument
elsif ARGV.length == 1
	puts checksum(ARGV[0])
end
