# -*- coding: utf-8 -*-
from odoo import models, fields

class FinanceExpense(models.Model):
    _name = "finance.expense"
    _description = "Expense"

    date = fields.Date(default=fields.Date.context_today, required=True)
    amount = fields.Monetary(required=True)
    currency_id = fields.Many2one("res.currency", default=lambda s: s.env.company.currency_id.id)
    wallet_id = fields.Many2one("finance.wallet", required=True)
    category_id = fields.Many2one("finance.category", domain=[("type","=","expense")], required=True)
    merchant = fields.Char()
    description = fields.Char()
    method = fields.Selection([("cash","Cash"),("bank","Bank"),("card","Card")], default="cash")
    attachment = fields.Binary("Receipt")
    attachment_filename = fields.Char()
