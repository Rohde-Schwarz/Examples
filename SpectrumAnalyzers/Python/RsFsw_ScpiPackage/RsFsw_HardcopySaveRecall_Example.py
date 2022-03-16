"""RsFsw Python package example. Performs the following:
- Creates new FSW application.
- Takes a screenshot and transfers the file to the control PC.
- Saves the instrument status to a file 'RsFswState.dfl'.
- Copies the 'RsFswState.dfl' file under a different name to the Control PC: 'RsFswState_PC.dfl'
- Copies the file 'RsFswState_PC.dfl' back to the instrument under a new name 'RsFswState_back.dfl'.
    This simulates acquiring and distribution of a setup file from the Control PC
- Resets the instrument
- Recalls the status from the 'RsFswState_back.dfl'
"""

from RsFsw import *

# A good practice is to check for the installed version
RsFsw.assert_minimum_version('5.0.0')

# Open the session
fsw = RsFsw('TCPIP::192.168.1.102::HISLIP', reset=True)
# Greetings, stranger...
print(f'Hello, I am: {fsw.utilities.idn_string}')

# Update display in remote
fsw.system.display.update.set(True)

# Create new instrument PhaseNoise
fsw.instrument.create.new.set(channel_type=enums.ChannelType.K40_PhaseNoise, channel_name='NoiseOnly')

# Add new window with SpotNoiseTable results at the bottom
new_name = fsw.applications.k40_PhaseNoise.layout.add.window.get('2', enums.WindowDirection.BELow, enums.WindowTypeK40.SpotNoiseTable)

# Let's make a screenshot
fsw.hardCopy.mode.set(enums.HardcopyMode.SCReen)
fsw.hardCopy.device.color.set(True)
# Set the color map. Colors.Ix4 means: Screen colors without changes
fsw.hardCopy.cmap.default.set(colors=repcap.Colors.Ix4)
fsw.massMemory.name.set(r'c:\Temp\Device_Screenshot2.png')
fsw.hardCopy.immediate.set_with_opc()
# Copy the screenshot to the PC
fsw.utilities.read_file_from_instrument_to_pc(r'c:\Temp\Device_Screenshot2.png', r'c:\Temp\PC_Screenshot2.png')
print(r'Screenshot saved here: c:\Temp\PC_Screenshot2.png')

# Save the current instrument status to a recall file
fsw.massMemory.store.state.set(r'RsFswState.dfl')
# Copy the setup file to the PC under a different name
fsw.utilities.read_file_from_instrument_to_pc(r'RsFswState.dfl', r'c:\Temp\RsFswState_PC.dfl')
print(r'Setup file saved here: c:\Temp\RsFswState_PC.dfl')
# Copy the setup file back to the instrument as 'RsFswState_back.dfl'
fsw.utilities.send_file_from_pc_to_instrument(r'c:\Temp\RsFswState_PC.dfl', r'RsFswState_back.dfl')

# Make a reset and restore the saved state.
fsw.utilities.reset()

# Restore the instrument status with the file copied back from the PC
fsw.massMemory.load.state.set(r'RsFswState_back.dfl')

# Close the session
fsw.close()
