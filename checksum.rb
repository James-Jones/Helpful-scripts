=begin
Generate a checksum. Checksums can be used to verify data has not been modified.
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
		crc #final value of 'index' in table
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
