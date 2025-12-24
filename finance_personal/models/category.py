# -*- coding: utf-8 -*-
from odoo import models, fields

class FinanceCategory(models.Model):
    _name = "finance.category"
    _description = "Finance Category"
    _parent_store = True

    name = fields.Char(required=True)
    type = fields.Selection(
        [("income","Income"), ("expense","Expense")],
        required=True, default="expense", index=True
    )
    parent_id = fields.Many2one("finance.category", string="Parent")
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many("finance.category", "parent_id")
    budget_monthly = fields.Monetary("Monthly Budget")
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id.id)
    active = fields.Boolean(default=True)
