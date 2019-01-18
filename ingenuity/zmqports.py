import json
import os

config_dir = os.path.expanduser('~/testerconfig')
config_file = os.path.join(config_dir, 'zmqports.json')
f = open(config_file, 'rU')
config = json.load(f)
f.close()

PUB_CHANNEL = str(config['PUB_CHANNEL'])
TEST_ENGINE_PORT = config['TEST_ENGINE_PORT']
TEST_ENGINE_PUB = config['TEST_ENGINE_PUB']
SEQUENCER_PORT = config['SEQUENCER_PORT']
SEQUENCER_PUB = config['SEQUENCER_PUB']
TE_PROXY_PUB = config['TE_PROXY_PUB']
SEQUENCER_PROXY_PUB = config['SEQUENCER_PROXY_PUB']
DATALOGGER_PORT = config['DATALOGGER_PORT']
DATALOGGER_PUB = config['DATALOGGER_PUB']
DEBUG_LOGGER_PORT = config['DEBUG_LOGGER_PORT']
SM_PUB = config['SM_PUB']
SM_RPC_PUB = config['SM_RPC_PUB']
SM_PROXY_PUB = config["SM_PROXY_PUB"]
SM_PORT = config['SM_PORT']
STATEMACHINE_PORT = config['SM_PORT']
LOGGER_PUB = config['LOGGER_PUB']
UART_PUB = config["UART_PUB"]
UART_PORT = config["UART_PORT"]
UART2_PUB = config["UART2_PUB"]
UART2_PORT = config["UART2_PORT"]
ARM_PUB = config["ARM_PUB"]
FIXTURE_PUB = config["FIXTURE_CTRL_PUB"]
FIXTURE_PORT = config["FIXTURE_CTRL_PORT"]
FIXTURE_PROXY_PUB = config["FIXTURE_PROXY_PUB"]
PWR_SEQUENCER_PUB = config["PWR_SEQUENCER_PUB"]
AUDIO_PUB = config["AUDIO_PUB"]
SPDIF_PUB = config["SPDIF_PUB"]
HDMI_PUB = config["HDMI_PUB"]
BACKLIGHT_PUB = config["BKLT_PUB"]

PUB_PORT = config['PUB_PORT']  # this is our magic number between a server port and a publisher port
