# -*- coding: utf-8 -*-
# from odoo import http


# class FinancePersonal(http.Controller):
#     @http.route('/finance_personal/finance_personal', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/finance_personal/finance_personal/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('finance_personal.listing', {
#             'root': '/finance_personal/finance_personal',
#             'objects': http.request.env['finance_personal.finance_personal'].search([]),
#         })

#     @http.route('/finance_personal/finance_personal/objects/<model("finance_personal.finance_personal"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('finance_personal.object', {
#             'object': obj
#         })

