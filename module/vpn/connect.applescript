tell application "Tunnelblick"
	connect "vpngate_JP"
	get state of first configuration where name = "vpngate_JP"
	repeat until result = "CONNECTED"
		delay 1
		get state of first configuration where name = "vpngate_JP"
	end repeat
end tell
