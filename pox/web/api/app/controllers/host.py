from pox.core import core
import pox.lib.util


class Host():

    def __init__(self):
        self.log = core.getLogger()
        self.port = long(38663)

    def getHosts(self):
        try:
            dataArray = []
            host_tracker = core.components.get("host_tracker")
            if host_tracker == None:
                self.log.error("Error getting module pox.host_tracker")
                return dataArray
            devices = host_tracker.entryByMAC
            for deviceKey in devices.keys():
                device = devices.get(deviceKey)
                networkAddresses = ""
                for ip in device.ipAddrs:
                    if len(networkAddresses) > 0:
                        networkAddresses += " "
                    networkAddresses += str(ip)
                data = {
                    "dataLayerAddress": str(device.macaddr),
                    "networkAddresses": networkAddresses,
                    "lastSeen": device.lastTimeSeen * 1000,
                    "switch_dpid": self.dpidToStr(device.dpid),
                    "port": device.port
                }
                dataArray.append(data)
            return dataArray
        except BaseException, e:
            self.log.error(e.message)
            dataArray = []
            return dataArray

    def getHost(self, dpid):
        try:
            dataArray = []
            host_tracker = core.components.get("host_tracker")
            if host_tracker == None:
                self.log.error("Error getting module pox.host_tracker")
                return dataArray
            devices = host_tracker.entryByMAC
            for deviceKey in devices.keys():
                device = devices.get(deviceKey)

                if(dpid == self.dpidToStr(device.dpid)):
                    networkAddresses = ""
                    for ip in device.ipAddrs:
                        if len(networkAddresses) > 0:
                            networkAddresses += " "
                        networkAddresses += str(ip)
                    data = {
                        "dataLayerAddress": str(device.macaddr),
                        "networkAddresses": networkAddresses,
                        "lastSeen": device.lastTimeSeen * 1000,
                        "switch_dpid": self.dpidToStr(device.dpid),
                        "port": device.port
                    }
                    dataArray.append(data)
            return dataArray
        except BaseException, e:
            self.log.error(e.message)
            dataArray = []
            return dataArray

    def dpidToStr(self, dpid):
        dpidStr = pox.lib.util.dpidToStr(dpid)
        dpidStr = dpidStr.replace("-", ":")
        dpidStr = "00:00:" + dpidStr
        return dpidStr
