# -*- coding: utf-8 -*-
from odoo import models, fields, api

class FinanceAsset(models.Model):
    _name = "finance.asset"
    _description = "Asset (Stock/REIT/Fund/Crypto)"

    name = fields.Char(required=True)
    symbol = fields.Char()
    asset_type = fields.Selection([
        ("stock","Stock"),("reit","REIT"),("fund","Fund"),
        ("crypto","Crypto"),("bond","Bond"),("cash","Cash")
    ], default="stock")
    currency_id = fields.Many2one("res.currency", default=lambda s: s.env.company.currency_id.id)


class FinanceHolding(models.Model):
    _name = "finance.holding"
    _description = "Holding Position"
    _sql_constraints = [
        ("asset_wallet_unique", "unique(asset_id, wallet_id)", "One holding per asset & wallet.")
    ]

    asset_id = fields.Many2one("finance.asset", required=True)
    wallet_id = fields.Many2one("finance.wallet")
    quantity = fields.Float(default=0.0)
    avg_cost = fields.Monetary(default=0.0)
    currency_id = fields.Many2one("res.currency", default=lambda s: s.env.company.currency_id.id)


class FinanceTrade(models.Model):
    _name = "finance.trade"
    _description = "Trade (Buy/Sell)"

    date = fields.Date(default=fields.Date.context_today, required=True)
    asset_id = fields.Many2one("finance.asset", required=True)
    wallet_id = fields.Many2one("finance.wallet", required=True)
    action = fields.Selection([("buy","Buy"),("sell","Sell")], required=True, default="buy")
    qty = fields.Float(required=True)
    price = fields.Monetary(required=True)
    fees = fields.Monetary(default=0.0)
    currency_id = fields.Many2one("res.currency", default=lambda s: s.env.company.currency_id.id)
    note = fields.Char()

    # computed for sells
    realized_pnl = fields.Monetary(readonly=True)

    def _apply_to_holding(self):
        for t in self:
            Holding = self.env["finance.holding"]
            h = Holding.search([("asset_id","=",t.asset_id.id), ("wallet_id","=",t.wallet_id.id)], limit=1)
            if not h:
                h = Holding.create({
                    "asset_id": t.asset_id.id,
                    "wallet_id": t.wallet_id.id,
                    "quantity": 0.0,
                    "avg_cost": 0.0,
                    "currency_id": t.currency_id.id,
                })
            if t.action == "buy":
                total_cost = h.avg_cost * h.quantity
                add_cost   = (t.price + (t.fees or 0.0)/max(t.qty,1.0)) * t.qty
                new_qty    = h.quantity + t.qty
                new_avg    = (total_cost + add_cost) / new_qty if new_qty else 0.0
                h.write({"quantity": new_qty, "avg_cost": new_avg})
            else:  # sell
                # realized P/L using average-cost method
                cost_basis = h.avg_cost * t.qty
                proceeds   = t.price * t.qty - (t.fees or 0.0)
                pnl        = proceeds - cost_basis
                t.write({"realized_pnl": pnl})
                new_qty = h.quantity - t.qty
                h.write({"quantity": max(0.0, new_qty)})
                # keep avg_cost unchanged (average-cost method)

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        rec._apply_to_holding()
        return rec


class FinanceDividend(models.Model):
    _name = "finance.dividend"
    _description = "Dividend"

    asset_id = fields.Many2one("finance.asset", required=True)
    ex_date = fields.Date()
    pay_date = fields.Date(default=fields.Date.context_today)
    amount_gross = fields.Monetary(required=True)
    tax_withheld = fields.Monetary(default=0.0)
    amount_net = fields.Monetary(compute="_compute_net", store=True)
    currency_id = fields.Many2one("res.currency", default=lambda s: s.env.company.currency_id.id)

    @api.depends("amount_gross", "tax_withheld")
    def _compute_net(self):
        for rec in self:
            rec.amount_net = (rec.amount_gross or 0.0) - (rec.tax_withheld or 0.0)
