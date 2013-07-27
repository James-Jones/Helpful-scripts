=begin
Given positive non-zero numbers find the Lowest Common Multiple.
=end

def gcm(a, b)
	while(b!=0)
		temp = b
		b = a % b
		a = temp
	end
	return a
end

def lcm2(a, b)
	return a * b / gcm(a, b)
end

def lcm3(a, b, c)
	return lcm2(a, lcm2(b, c))
end

if ARGV.length == 0
	return
elsif ARGV.length == 1
	puts ARGV[0]
else
	lcmTotal = ARGV[0].to_i
	loopCount = ARGV.length-1
	loopCount.times do |i|
		lcmTotal = lcm2(lcmTotal, ARGV[i+1].to_i)
	end
	puts lcmTotal
end
