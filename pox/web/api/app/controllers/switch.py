from pox.core import core


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
                    "dataLayerSource": dpidToStr(link.dpid1),
                    "portSource": link.port1,
                    "dataLayerDestination": dpidToStr(link.dpid2),
                    "portDestination": link.port2
                }
                dataArray.append(data)
            return dataArray
        except BaseException, e:
            self.log.error(e.message)
            dataArray = []
            return dataArray
