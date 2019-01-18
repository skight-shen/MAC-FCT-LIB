package.cpath = package.cpath .. ";./?.dylib"
local mid = 3;
local ip = "169.254.1.32"
local port = 7630
if(CONFIG) then
	mid = CONFIG.ID
	ip = CONFIG.FIXTURE_ADDRESS[CONFIG.ID + 1]
	port = CONFIG.HDMI_DATA_PORT
	print("< "..tostring(mid).." > Load HDMI DL lua...")
end

require "libHDMI_DL"
print("< "..tostring(mid).." > Load HDMI_DL lua Success...")

--TBD, havn't finished

local dl = CHDMI:new()
dl:CreateTCPClient("HDMI_DL", ip, port)
io.read()
dl:startDataLogger("/vault")
io.read()
dl:stopDataLogger()

