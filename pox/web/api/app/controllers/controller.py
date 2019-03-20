from pox.core import core


class Controller():

    def __init__(self):
        self.log = core.getLogger()

    def getInfo(self):

        data = {}
        try:
            of_01 = core.components.get("of_01")
            if of_01 == None:
                self.log.error("module not started pox.openflow.of_01")
                return data

            data = {
                "address": of_01.address,
                "port": of_01.port,
                "started": of_01.started,
                "name": of_01.name,
                "id": of_01.id
            }
            return data
        except BaseException, error:
            self.log.error(error.message)
            return data
