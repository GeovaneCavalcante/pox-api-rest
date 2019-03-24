# coding=utf-8

from flask import jsonify
from flask_restplus import Resource

from .. import app, api
from ..controllers.controller import Controller
from ..controllers.switch import Switch
from ..controllers.host import Host

ns_switch = api.namespace('api_switch')
ns_controller = api.namespace('api_controller')
ns_hosts = api.namespace('api_hosts')


@ns_controller.route('/info')
class ControllerInformation(Resource):

    def get(self):
        """ Controller information """
        controller = Controller()
        return jsonify(controller.getInfo())


@ns_switch.route('/switches/links')
class SwitchesLinks(Resource):

    def get(self):
        """ All link between network switches """
        switch = Switch()
        return jsonify(switch.getLinks())


@ns_switch.route('/switches/links/<dpid>')
@ns_switch.doc(params={'dpid': 'DPID of the switch is required on this route'})
class SwitchLinks(Resource):

    def get(self, dpid):
        """ Links of a single switch specified in the route """
        switch = Switch()
        return jsonify(switch.getSwitchLinks(dpid))


@ns_switch.route('/switches')
class Switches(Resource):

    def get(self):
        """ Information from all switches connected to the controllers """
        switch = Switch()
        return jsonify(switch.getSwitches())


@ns_switch.route('/switches/<dpid>')
@ns_switch.doc(params={'dpid': 'DPID of the switch is required on this route'})
class SwitchInfo(Resource):

    def get(self, dpid):
        """ Information about a specific switch connected to the controller """
        switch = Switch()
        return jsonify(switch.getSwitch(dpid))


@ns_switch.route('/switches/<dpid>/aggregate')
@ns_switch.doc(params={'dpid': 'DPID of the switch is required on this route'})
class SwitchAggregate(Resource):

    def get(self, dpid):
        """ Shows statistics aggregated to a switch """
        switch = Switch()
        return jsonify(switch.getSwitchAggregate(dpid))


@ns_switch.route('/switches/<dpid>/description')
@ns_switch.doc(params={'dpid': 'DPID of the switch is required on this route'})
class SwitchDescription(Resource):

    def get(self, dpid):
        """ Switch Description """
        switch = Switch()
        return jsonify(switch.getSwitchDescription(dpid))


@ns_switch.route('/switches/<dpid>/flows')
@ns_switch.doc(params={'dpid': 'DPID of the switch is required on this route'})
class SwitchFlows(Resource):

    def get(self, dpid):
        """ All flows of the switch connected to the controller """
        switch = Switch()
        return jsonify(switch.getSwitchFlows(dpid))


@ns_hosts.route('/hosts')
class Hosts(Resource):

    def get(self):
        """ Information from all hosts of the switches connected to the controller """
        host = Host()
        return jsonify(host.getHosts())


@ns_hosts.route('/hosts/<dpid>')
@ns_hosts.doc(params={'dpid': 'DPID of the switch is required on this route'})
class HostsSwitch(Resource):

    def get(self, dpid):
        """ Information about specified switch hosts """
        host = Host()
        return jsonify(host.getHost(dpid))
