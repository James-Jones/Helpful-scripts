=begin
Write a function which takes 3 points in 2D space vL0, vL1, vP, and
returns +1 or -1 depending on whether the point vP is on the right (+1)
or left (-1) of the line from L0 to L1.
=end

Struct.new("Point", :x, :y)

def isLeftRight(lineP0, lineP1, p)
	#2D cross product
	if (((lineP1.x - lineP0.x)*(p.y - lineP0.y) - (lineP1.y - lineP0.y)*(p.x - lineP0.x)) > 0)
		return -1
	else
		return +1
	end
end

vL0 = Struct::Point.new(ARGV[0].to_f, ARGV[1].to_f);
vL1 = Struct::Point.new(ARGV[2].to_f, ARGV[3].to_f);
vP = Struct::Point.new(ARGV[4].to_f, ARGV[5].to_f);

puts isLeftRight(vL0, vL1, vP)
