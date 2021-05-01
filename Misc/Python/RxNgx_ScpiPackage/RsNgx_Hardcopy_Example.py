""""RsNgx example showing how to make a screenshot of the instrument display."""

import time
from RsNgx import *

file_path = r'c:\temp\ngx_screenshot.png'
RsNgx.assert_minimum_version('1.0.0.37')
ngx = RsNgx('TCPIP::10.102.52.45::INSTR')
print(f'Hello, I am: {ngx.utilities.idn_string}')

ngx.display.window.text.set_data("My Greetings to you ...")
ngx.hardCopy.formatPy.set(enums.HcpyFormat.PNG)
picture = ngx.hardCopy.get_data()

file = open(file_path, 'wb')
file.write(picture)
file.close()
print(f'Screenshot saved to: {file_path}')

ngx.close()
