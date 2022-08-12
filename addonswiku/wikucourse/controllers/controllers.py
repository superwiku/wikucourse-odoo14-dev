# -*- coding: utf-8 -*-
# from odoo import http


# class Wikucourse(http.Controller):
#     @http.route('/wikucourse/wikucourse/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wikucourse/wikucourse/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wikucourse.listing', {
#             'root': '/wikucourse/wikucourse',
#             'objects': http.request.env['wikucourse.wikucourse'].search([]),
#         })

#     @http.route('/wikucourse/wikucourse/objects/<model("wikucourse.wikucourse"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wikucourse.object', {
#             'object': obj
#         })
