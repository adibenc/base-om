# -*- coding: utf-8 -*-
# from odoo import http


# class TsaNetworkManagement(http.Controller):
#     @http.route('/tsa_network_management/tsa_network_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tsa_network_management/tsa_network_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tsa_network_management.listing', {
#             'root': '/tsa_network_management/tsa_network_management',
#             'objects': http.request.env['tsa_network_management.tsa_network_management'].search([]),
#         })

#     @http.route('/tsa_network_management/tsa_network_management/objects/<model("tsa_network_management.tsa_network_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tsa_network_management.object', {
#             'object': obj
#         })

