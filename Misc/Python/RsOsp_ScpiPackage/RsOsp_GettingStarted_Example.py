import time

from RsOsp import *

RsOsp.assert_minimum_version('2.10')
osp = RsOsp(f'TCPIP::10.212.0.85::INSTR')

osp.utilities.visa_timeout = 5000
# Sends OPC after each commands
osp.utilities.opc_query_after_write = True

osp.utilities.reset()

# Self-test
self_test = osp.utilities.self_test()
print(f'Hello, I am {osp.utilities.idn_string}\n')

osp.route.path.delete_all()
osp.route.path.define.set("Test1", "(@F01M01(0201, 0302))")
paths2 = osp.route.path.get_catalog()

print(f'Osp defined paths:\n {",".join(osp.route.path.get_catalog())}')
path_last = osp.route.path.get_last()
path_list = osp.route.path.get_catalog()
pathname = path_list[0]
print(f'Defined Path Definitions: {len(path_list)}')
for pathname in path_list:
    print(f' Path Name:  {pathname} ({osp.route.path.define.get(pathname)} )')
    osp.route.close.set_path(pathname)
    time.sleep(1)

print(f'Osp errors\n:{osp.utilities.query_all_errors()}')

osp.close()
