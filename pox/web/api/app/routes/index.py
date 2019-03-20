# coding=utf-8

from flask import jsonify
from flask_restplus import Resource

from .. import app, api
from ..controllers.controller import Controller
from ..controllers.switch import Switch

ns_switch = api.namespace('api_switch')
ns_controller = api.namespace('api_controller')


@ns_controller.route('/info')
class ControllerInformation(Resource):

    def get(self):
        """ Driver Information """
        controller = Controller()
        return jsonify(controller.getInfo())
