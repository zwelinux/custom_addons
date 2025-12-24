# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date

class FinanceDebtAccount(models.Model):
    _name = "finance.debt.account"
    _description = "Debt Account"

    name = fields.Char(required=True)
    type = fields.Selection([
        ("credit_card","Credit Card"), ("loan","Loan"),
        ("family","Family"), ("other","Other")
    ], default="loan", required=True)

    principal = fields.Monetary("Current Balance", required=True)
    apr = fields.Float("APR (%)", digits=(16, 4))
    min_payment = fields.Monetary(default=0.0)
    due_day = fields.Integer("Due Day (1-28)")
    start_date = fields.Date()
    currency_id = fields.Many2one("res.currency", default=lambda s: s.env.company.currency_id.id)
    active = fields.Boolean(default=True)

    payment_ids = fields.One2many("finance.debt.payment", "account_id")
    total_paid = fields.Monetary(compute="_compute_totals", store=True, readonly=True)
    is_settled = fields.Boolean(compute="_compute_totals", store=True, readonly=True)

    @api.depends("payment_ids.amount", "principal")
    def _compute_totals(self):
        for acc in self:
            acc.total_paid = sum(acc.payment_ids.mapped("amount"))
            acc.is_settled = (acc.principal or 0.0) <= 0.00001


class FinanceDebtPayment(models.Model):
    _name = "finance.debt.payment"
    _description = "Debt Payment"

    date = fields.Date(default=fields.Date.context_today, required=True)
    account_id = fields.Many2one("finance.debt.account", required=True, ondelete="cascade")
    amount = fields.Monetary(required=True)
    currency_id = fields.Many2one("res.currency", related="account_id.currency_id", store=True)
    principal_applied = fields.Monetary(readonly=True)
    interest_applied = fields.Monetary(readonly=True)
    extra_payment = fields.Monetary(readonly=True)

    def _split_payment(self):
        """Very simple interest split: monthly APR/12 * current balance."""
        for rec in self:
            bal = rec.account_id.principal or 0.0
            monthly_rate = (rec.account_id.apr or 0.0) / 100.0 / 12.0
            interest = round(bal * monthly_rate, 2)
            principal = max(0.0, (rec.amount or 0.0) - interest)
            rec.write({
                "interest_applied": interest,
                "principal_applied": principal,
                "extra_payment": max(0.0, principal - (rec.account_id.min_payment or 0.0))
            })

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        rec._split_payment()
        # reduce balance
        new_bal = max(0.0, (rec.account_id.principal or 0.0) - (rec.principal_applied or rec.amount or 0.0))
        rec.account_id.write({"principal": new_bal})
        return rec
