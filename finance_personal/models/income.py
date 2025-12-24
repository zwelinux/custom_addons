# -*- coding: utf-8 -*-
from odoo import models, fields

class FinanceIncome(models.Model):
    _name = "finance.income"
    _description = "Income"

    date = fields.Date(default=fields.Date.context_today, required=True)
    amount = fields.Monetary(required=True)
    currency_id = fields.Many2one("res.currency", default=lambda s: s.env.company.currency_id.id)
    wallet_id = fields.Many2one("finance.wallet", required=True)
    source = fields.Char("Source")
    type = fields.Selection([
        ("salary","Salary"), ("freelance","Freelance"), ("side","Side Income"),
        ("rental","Rental"), ("dividend","Dividend"), ("other","Other")
    ], default="salary", required=True)
    note = fields.Text()
