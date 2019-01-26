on run argv
	tell application "Tunnelblick"
		connect "CA_216.168.109.105"
		get state of first configuration where name = "CA_216.168.109.105"
		repeat until result = "CONNECTED"
			delay 1
			get state of first configuration where name = "CA_216.168.109.105"
		end repeat
		
		(* local vpn
		set vpn to quoted form of (item 1 of argv)
		do shell script "echo The value: " & vpn
		set vpn2 to "CA_216.168.109.105"
		connect "CA_216.168.109.105" # & vpn # error occur
		get state of first configuration where name = "CA_216.168.109.105"
		repeat until result = "CONNECTED"
			delay 1
			get state of first configuration where name = "CA_216.168.109.105"
		end repeat*)
	end tell
end run
