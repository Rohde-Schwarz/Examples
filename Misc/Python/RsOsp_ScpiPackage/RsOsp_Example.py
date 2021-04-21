import time

from RsOsp import *


def ask(prompt, typ, default):
    print('%s [%s] ' % (prompt, default)),
    value = typ(input())
    if not value:
        return default
    else:
        return value


RsOsp.assert_minimum_version('2.10')
ip = ask('Enter IP address of OSP: ', str, '10.212.0.85')

print('-------------------------------------------------------------------------')
print('---    O S P   D E V I C E   I N F O R M A T I O N      -----------------')
print('-------------------------------------------------------------------------')
osp_base = RsOsp(f'TCPIP::{ip}::INSTR', True, False)

osp_base.utilities.visa_timeout = 5000
# Sends OPC after each commands
osp_base.utilities.opc_query_after_write = True
# Checks for syst:err? after each command / query
osp_base.utilities.instrument_status_checking = True

# You can still use the direct SCPI write / query:
osp_base.utilities.write_str('*RST')
instr_err = osp_base.utilities.query_str('SYST:ERR?')
# System Reset
osp_base.utilities.reset()

# Self-test
self_test = osp_base.utilities.self_test()

print(f'Identification ...............=: {osp_base.utilities.idn_string}\n')
print(f'Instrument Manufacturer.......=: {osp_base.utilities.manufacturer}')
print(f'Instrument Name        .......=: {osp_base.utilities.full_instrument_model_name}')
print(f'Instrument Serial Number......=: {osp_base.utilities.instrument_serial_number}')
print(f'Instrument Firmware Version ..=: {osp_base.utilities.instrument_firmware_version}')
print(f'Instrument Options............=: {",".join(osp_base.utilities.instrument_options)}\n')
print(f'Supported Devices..    .......=: {",".join(osp_base.utilities.supported_models)}')
print(f'VISA Manufacturer.............=: {osp_base.utilities.visa_manufacturer}')
print(f'VISA Timeout..................=: {osp_base.utilities.visa_timeout}')
print(f'Driver Version ...............=: {osp_base.utilities.driver_version}\n')

#    print(f'Osp instrument status:{osp_base.utilities.instrument_status_checking}')

print(f'Osp HwInfo:\n{",".join(osp_base.diagnostic.service.get_hw_info())}')
print(f'Osp virtual mode enable ?:{osp_base.configure.virtual.get_mode()}')
if osp_base.configure.virtual.get_mode() is False:
    osp_base.configure.virtual.set_mode(True)
print(f'Osp virtual mode enable ?:{osp_base.configure.virtual.get_mode()}')

osp_base.route.path.delete_all()
paths = osp_base.route.path.get_catalog()

osp_base.route.path.define.set("Test1", "(@F01M01(0201, 0302))")
paths2 = osp_base.route.path.get_catalog()

print(f'Osp HwInfo:\n{",".join(osp_base.diagnostic.service.get_hw_info())}')
hwinfolist = osp_base.diagnostic.service.get_hw_info()
print(hwinfolist)

for hw in hwinfolist:
    print(hw)
    module_info = hw.rsplit("|")
    print(module_info)
    print(module_info[1])
    time.sleep(1)

# get path list and switch all after each other
print(f'Osp defined paths:\n {",".join(osp_base.route.path.get_catalog())}')
path_last = osp_base.route.path.get_last()
path_list = osp_base.route.path.get_catalog()
path_name = path_list[0]
print(f'Defined Path Definitions: {len(path_list)}')
for path_name in path_list:
    print(f' Path Name:  {path_name} ({osp_base.route.path.define.get(path_name)} )')
    osp_base.route.close.set_path(path_name)
    print(f'Osp error?:{osp_base.utilities.query_str("SYST:ERR?")}')
    time.sleep(1)

print(f'Osp error?:{osp_base.utilities.query_str("SYST:ERR?")}')
osp_base.utilities.reset()

osp_base.configure.virtual.set_mode(False)

osp_base.close()
