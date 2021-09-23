"""This RsFsw Python SCPI package example shows creating new FSW applications and arranging windows"""

from RsFsw import *

# Open the session
fsw = RsFsw('TCPIP::192.168.1.101::HISLIP', reset=True)
# Greetings, stranger...
print(f'Hello, I am: {fsw.utilities.idn_string}')

# Print commands to the console with the logger
fsw.utilities.logger.mode = LoggingMode.On
fsw.utilities.logger.log_to_console = True
# Do not log status checking messages if the status was OK
fsw.utilities.logger.log_status_check_ok = False

# Update display in remote
fsw.system.display.update.set(True)

# Create new instrument VSA
fsw.instrument.create.new.set(channel_type=enums.ChannelType.K70_VectorSignalAnalyzer, channel_name='MyVsa')
# Create new instrument Pulse
fsw.instrument.create.new.set(channel_type=enums.ChannelType.K6_PulseAnalysis, channel_name='MyPulse')

# Select the specan instrument by instrument name
fsw.instrument.select.set(enums.ChannelType.SpectrumAnalyzer)

# Select the MyVsa by name
fsw.instrument.selectName.set('MyVsa')

channels = fsw.instrument.listPy.get()
print(f'All active channels (type, name): {channels}')

# Get catalog of all the active windows in the VSA
windows = fsw.layout.catalog.window.get()
print(f'All active windows in the VSA (number, name): {windows}')

# Add new window with EVM results to the right of the ResultSummary window
new_name = fsw.applications.k70_Vsa.layout.add.window.get('2', enums.WindowDirection.RIGHt, enums.WindowTypeK70.ErrorVectorMagnitude)
print(f"Newly created window name: '{new_name}'")
# Now move the window 1 to the right from the newly created window:
fsw.applications.k70_Vsa.layout.move.window.set('1', new_name, enums.WindowDirReplace.RIGHt)

# Close the session
fsw.close()
