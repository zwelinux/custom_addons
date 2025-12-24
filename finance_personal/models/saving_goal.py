# -*- coding: utf-8 -*-
from odoo import models, fields, api

class FinanceSavingGoal(models.Model):
    _name = "finance.saving.goal"
    _description = "Saving Goal"

    name = fields.Char(required=True)
    target_amount = fields.Monetary(required=True)
    # Auto-computed from related transfers
    current_amount = fields.Monetary(
        compute="_compute_current_amount", store=True, readonly=True
    )
    deadline = fields.Date()
    priority = fields.Selection(
        [("low","Low"),("med","Medium"),("high","High")], default="med"
    )
    currency_id = fields.Many2one(
        "res.currency", default=lambda s: s.env.company.currency_id.id
    )
    active = fields.Boolean(default=True)

    # Link to transfers so compute depends on them
    transfer_ids = fields.One2many(
        "finance.transfer", "goal_id", string="Transfers"
    )

    @api.depends("transfer_ids.amount")
    def _compute_current_amount(self):
        for g in self:
            g.current_amount = sum(g.transfer_ids.mapped("amount"))


class FinanceTransfer(models.Model):
    _name = "finance.transfer"
    _description = "Wallet -> Goal Transfer"

    date = fields.Date(default=fields.Date.context_today, required=True)
    wallet_id = fields.Many2one("finance.wallet", required=True)
    goal_id = fields.Many2one("finance.saving.goal", required=True, ondelete="cascade")
    amount = fields.Monetary(required=True)
    currency_id = fields.Many2one(
        "res.currency", default=lambda s: s.env.company.currency_id.id
    )
    note = fields.Char()
