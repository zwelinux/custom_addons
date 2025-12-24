# -*- coding: utf-8 -*-
from odoo import models, fields

class FinanceWallet(models.Model):
    _name = "finance.wallet"
    _description = "Wallet / Account"

    name = fields.Char(required=True)
    type = fields.Selection([
        ("cash","Cash"), ("bank","Bank"), ("card","Card"), ("broker","Broker"), ("other","Other")
    ], default="cash")
    currency_id = fields.Many2one("res.currency", default=lambda s: s.env.company.currency_id.id)
    active = fields.Boolean(default=True)
