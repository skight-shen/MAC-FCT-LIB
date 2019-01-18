package.cpath = package.cpath .. ";./?.dylib"
local mid = 3;
local ip = "169.254.1.35"
local port = 7603
if(CONFIG) then
	mid = CONFIG.ID
	ip = CONFIG.FIXTURE_ADDRESS[CONFIG.ID + 1]
	port = CONFIG.DATALOGGER_PORT
	print("< "..tostring(mid).." > Load ArmDL lua...")
end

require "libArmDL"
print("< "..tostring(mid).." > Load ArmDL lua Success...")

--TBD, havn't finished
-- 1. startDataLogger when testing start
-- 2. stopDataLogger when testing finish
local dl = CArmDL:new()
--void updateConfig(float resdiv, float gain, float refVolt, float res, int flag=0, int unitConvert=1);

dl:updateConfig(1,3.91176,5.0,0.5,0);
dl:CreateTCPClient("ARMDL", ip, port)
io.read()
dl:startDataLogger("/vault")
io.read()
dl:stopDataLogger()

