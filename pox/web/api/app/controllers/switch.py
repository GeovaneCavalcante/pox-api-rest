from pox.core import core
import pox.lib.util


class Switch():

    def __init__(self):
        self.log = core.getLogger()

    def getLinks(self):

        try:
            dataArray = []
            discovery = core.components.get("openflow_discovery")

            if discovery == None:
                self.log.error("Error getting module pox.openflow.discovery")
                return dataArray

            links = discovery.adjacency
            for link in links.keys():
                data = {
                    "dataLayerSource": self.dpidToStr(link.dpid1),
                    "portSource": link.port1,
                    "dataLayerDestination": self.dpidToStr(link.dpid2),
                    "portDestination": link.port2
                }
                dataArray.append(data)
            return dataArray
        except BaseException, e:
            self.log.error(e.message)
            dataArray = []
            return dataArray

    def dpidToStr(self, dpid):
        """
        Converts DPID from numeric format to format XX:XX:XX:XX:XX:XX:XX:XX.

        :param dpid: DPID in numeric format to convert
        :type dpid: int
        :return: DPID in format XX:XX:XX:XX:XX:XX:XX:XX
        :rtype: str
        """
        dpidStr = pox.lib.util.dpidToStr(dpid)
        dpidStr = dpidStr.replace("-", ":")
        dpidStr = "00:00:" + dpidStr
        return dpidStr
