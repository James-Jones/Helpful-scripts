
ARGV.each do|arg|
	if File.file?(arg)
		withTabs = File.read(arg)
		withSpaces = withTabs.gsub("\t", "    ");
		File.open(arg, "w") { |file| file.puts withSpaces }
	end
end
