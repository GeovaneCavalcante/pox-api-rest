from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.addresses import EthAddr, IPAddr
import pox.lib.packet as pkt

log = core.getLogger()

rules = [['b6:66:95:4c:f3:76', '26:50:be:d0:50:44'], ['00:00:00:00:00:02', '00:00:00:00:00:04'], [
    '00:00:00:00:00:08', '00:00:00:00:00:03'], ['00:00:00:00:00:07', '00:00:00:00:00:02']]

dns = ['172.217.29.4', '172.217.162.100',
       '172.217.28.238', '216.58.202.206', '216.58.202.195', '31.13.85.36', '157.240.12.35', '157.240.12.13']


class SDNFirewall (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)

    def _handle_ConnectionUp(self, event):

        for d in dns:
            log.info("Hub running.")
            msg = of.ofp_flow_mod()
            msg.priority = 42
            msg.match.dl_type = 0x800
            msg.match.nw_dst = IPAddr(d)

            msg.match.nw_src = IPAddr("10.0.0.1")
            # msg.match.tp_dst = 80
            # msg.actions.append(of.ofp_action_output(port=4))
            event.connection.send(msg)

        # for rule in rules:
        #     pass
        #     # block = of.ofp_match()

        #     # block.dl_src = EthAddr(rule[0])
        #     # block.dl_dst = EthAddr(rule[1])
        #     # block._nw_src = IPAddr('10.0.0.1')
        #     # block._nw_dst = IPAddr('10.0.0.2')
        #     # flow_mod = of.ofp_flow_mod()
        #     # flow_mod.match = block
        #     # print(block.__dict__)
        #     msg = of.ofp_flow_mod()
        #     msg.priority = 42
        #     msg.match.dl_type = 0x800
        #     msg.match.nw_dst = IPAddr("172.217.29.4")
        #     # msg.match.nw_src = IPAddr("10.0.0.2")
        #     # msg.match.tp_dst = 80
        #     msg.actions.append(of.ofp_action_output(port=4))
        #     event.connection.send(msg)


def launch():
    log.info("Hub running.")

    core.registerNew(SDNFirewall)
