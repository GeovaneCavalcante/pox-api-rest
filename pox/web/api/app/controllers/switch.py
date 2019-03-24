from pox.core import core
import pox.lib.util
import pox.openflow.libopenflow_01 as of
import time


class Switch():

    def __init__(self):
        self.log = core.getLogger()
        self.port = long(38663)
        self.stats = None
        core.openflow.addListenerByName(
            "AggregateFlowStatsReceived", self.handle_AggregateFlowStatsReceived)
        core.openflow.addListenerByName(
            "SwitchDescReceived", self.handle_DescStatsReceived)
        core.openflow.addListenerByName(
            "FlowStatsReceived", self.handle_FlowStatsReceived)
        core.openflow.addListenerByName(
            "PortStatsReceived", self.handle_PortStatsReceived)
        core.openflow.addListenerByName(
            "QueueStatsReceived", self.handle_QueueStatsReceived)
        core.openflow.addListenerByName(
            "TableStatsReceived", self.handle_TableStatsReceived)

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
                    "dpidSrc": self.dpidToStr(link.dpid1),
                    "portSrc": link.port1,
                    "dpidDst": self.dpidToStr(link.dpid2),
                    "portDst": link.port2
                }
                dataArray.append(data)
            return dataArray
        except BaseException, e:
            self.log.error(e.message)
            dataArray = []
            return dataArray

    def getSwitchLinks(self, dpid):

        try:
            dataArray = []
            discovery = core.components.get("openflow_discovery")

            if discovery == None:
                self.log.error("Error getting module pox.openflow.discovery")
                return dataArray

            links = discovery.adjacency
            for link in links.keys():
                if(self.dpidToStr(link.dpid1) == dpid):
                    data = {
                        "dpidSrc": self.dpidToStr(link.dpid1),
                        "portSrc": link.port1,
                        "dpidDst": self.dpidToStr(link.dpid2),
                        "portDst": link.port2
                    }
                    dataArray.append(data)
            return dataArray
        except BaseException, e:
            self.log.error(e.message)
            dataArray = []
            return dataArray

    def getSwitches(self):

        try:
            dataArray = []
            openflow = core.components.get("openflow")
            if openflow == None:
                self.log.error("Error getting module pox.openflow")
                return dataArray

            connections = openflow._connections
            fakePort = self.port
            for connKey in connections.keys():
                fakePort += 1
                connection = connections.get(connKey)
                switch_dpid = self.dpidToStr(connection.dpid)
                data = {
                    "dpid": switch_dpid,
                    "remoteIp": "192.168.56.2",
                    "remotePort": fakePort,
                    "connectedSince": connection.connect_time * 1000,
                }
                dataArray.append(data)
            return dataArray
        except BaseException, e:
            self.log.error(e.message)
            dataArray = []
            return dataArray

    def getSwitch(self, dpid):

        try:
            dataArray = []
            openflow = core.components.get("openflow")
            if openflow == None:
                self.log.error("Error getting module pox.openflow")
                return dataArray

            connections = openflow._connections
            fakePort = self.port
            for connKey in connections.keys():
                connection = connections.get(connKey)
                switch_dpid = self.dpidToStr(connection.dpid)
                if(switch_dpid == dpid):
                    fakePort += 1
                    data = {
                        "dpid": switch_dpid,
                        "remoteIp": "192.168.56.2",
                        "remotePort": fakePort,
                        "connectedSince": connection.connect_time * 1000,
                    }
                    dataArray.append(data)
            return dataArray
        except BaseException, e:
            self.log.error(e.message)
            dataArray = []
            return dataArray

    def getSwitchAggregate(self, switch_dpid):

        try:
            bodyMsg = of.ofp_aggregate_stats_request()

            bodyMsg.match = of.ofp_match()
            bodyMsg.table_id = of.TABLE_ALL
            bodyMsg.out_port = of.OFPP_NONE
            msg = of.ofp_stats_request(body=bodyMsg)
            msg.type = of.OFPST_AGGREGATE

            data = {}

            aggStats = self.get_switch_stats(
                switch_dpid, msg, "aggregate flows")
            if aggStats == None:
                self.log.error("Error getting aggregate stats")
                return data

            data = {
                "bytes": aggStats.byte_count,
                "flows": aggStats.flow_count,
                "packets": aggStats.packet_count
            }
            return data
        except BaseException, e:
            self.log.error(e.message)
            data = {}
            return data

    def getSwitchDescription(self, switch_dpid):
        try:
            msg = of.ofp_stats_request()
            msg.type = of.OFPST_DESC

            data = {}
            descStats = self.get_switch_stats(switch_dpid, msg, "description")
            if descStats == None:
                self.log.error("Error getting description stats")
                return data

            data = {
                "serialNumber": descStats.serial_num,
                "manufacturer": descStats.mfr_desc,
                "hardware": descStats.hw_desc,
                "software": descStats.sw_desc,
                "datapath": descStats.dp_desc
            }
            return data
        except BaseException, e:
            self.log.error(e.message)
            data = {}
            return data

    def getSwitchFlows(self, switch_dpid):
        try:
            bodyMsg = of.ofp_flow_stats_request()
            bodyMsg.match = of.ofp_match()
            bodyMsg.table_id = of.TABLE_ALL
            bodyMsg.out_port = of.OFPP_NONE
            msg = of.ofp_stats_request(body = bodyMsg)
            msg.type = of.OFPST_FLOW
      
            dataArray = []
            stats = self.get_switch_stats(switch_dpid, msg, "flows")
            if stats == None:
                self.log.error("Error getting flow stats")
                return dataArray
           
            for flowStats in stats:
                outports = ""
                for action in flowStats.actions:
                    if isinstance(action, of.ofp_action_output):
                        if len(outports) > 0:
                            outports += " "
                        outports += str(action.port)
       
                data = {
                        "inPort": flowStats.match._in_port,
                        "dataLayerSource": str(flowStats.match._dl_src),
                        "dataLayerDestination": str(flowStats.match._dl_dst),
                        "dataLayerType": flowStats.match._dl_type,
                        "networkSource": str(flowStats.match._nw_src),
                        "networkDestination": str(flowStats.match._nw_dst),
                        "networkProtocol": flowStats.match._nw_proto,
                        "transportSource": flowStats.match._tp_src,
                        "transportDestination": flowStats.match._tp_dst,
                        "wildcards": flowStats.match.wildcards,
                        "bytes": flowStats.byte_count,
                        "packets": flowStats.packet_count,
                        "time": float(flowStats.duration_sec) + (float(flowStats.duration_nsec) / float(1000000000)),
                        "idleTimeout": flowStats.idle_timeout,
                        "hardTimeout": flowStats.hard_timeout,
                        "cookie": flowStats.cookie,
                        "outports": outports
                        }
            
                dataArray.append(data)
            return dataArray
        except BaseException, e:
            self.log.error(e.message)
            dataArray = []
            return dataArray

    def get_switch_stats(self, switch_dpid, msg, statsType):

        try:
            self.stats = None
            dpid = self.strToDPID(switch_dpid)
            core.openflow.sendToDPID(dpid, msg.pack())
            initialTime = time.time()
            while self.stats == None:
                if (time.time() - initialTime) > 15:
                    self.log.error("Timeout failure retrieving " +
                                   statsType + " stats")
                    break
            return self.stats
        except BaseException, e:
            self.log.error("Failure retrieving " + statsType + " stats")
            self.log.error(e.message)
            return None

    def strToDPID(self, dpidStr):

        dpidStr = dpidStr[6:]
        dpidStr = dpidStr.replace(":", "-")
        dpid = pox.lib.util.strToDPID(dpidStr)
        return dpid

    def dpidToStr(self, dpid):
        dpidStr = pox.lib.util.dpidToStr(dpid)
        dpidStr = dpidStr.replace("-", ":")
        dpidStr = "00:00:" + dpidStr
        return dpidStr

    # event handler functions
    def handle_AggregateFlowStatsReceived(self, event):
        """
        Handles aggregate flow stats event.

        :param event: Event received to handle.
        """
        self.stats = event.stats
        self.log.debug("AggregateFlowStatsReceived")

    def handle_DescStatsReceived(self, event):
        """
        Handles description stats event.

        :param event: Event received to handle.
        """
        self.stats = event.stats
        self.log.debug("SwitchDescReceived")

    def handle_FlowStatsReceived(self, event):
        """
        Handles flow stats event.

        :param event: Event received to handle.
        """
        self.stats = event.stats
        self.log.debug("FlowStatsReceived")

    def handle_PortStatsReceived(self, event):
        """
        Handles port stats event.

        :param event: Event received to handle.
        """
        self.stats = event.stats
        self.log.debug("PortStatsReceived")

    def handle_QueueStatsReceived(self, event):
        """
        Handles queue stats event.

        :param event: Event received to handle.
        """
        self.stats = event.stats
        self.log.debug("QueueStatsReceived")

    def handle_TableStatsReceived(self, event):
        """
        Handles table stats event.

        :param event: Event received to handle.
        """
        self.stats = event.stats
        self.log.debug("TableStatsReceived")
