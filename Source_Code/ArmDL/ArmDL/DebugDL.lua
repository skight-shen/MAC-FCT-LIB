package.cpath = package.cpath .. ";./?.dylib"
print("Load ArmDL lua...")

require "libArmDL"
print("Load ArmDL lua Success...")

-- while(true) do  end
local dl = CArmDL:new()
dl:CreateTCPClient("ARMDL", "169.254.1.35",7603)
io.read()
dl:startDataLogger("/vault")
io.read()
dl:stopDataLogger()

