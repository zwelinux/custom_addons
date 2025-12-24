from odoo import models, fields, api
import re


from odoo import models, fields, api
import re


class StockAssignSerialInherit(models.TransientModel):
    _inherit = "stock.assign.serial"

    last_serial = fields.Char(
        string="Last Serial Used",
        readonly=True
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        move_id = self.env.context.get("active_id")
        if not move_id:
            return res

        move = self.env["stock.move"].browse(move_id)
        if not move or move.product_id.tracking != "serial":
            return res

        last_lot = self.env["stock.lot"].sudo().search(
            [
                ("product_id", "=", move.product_id.id),
                ("company_id", "=", self.env.company.id),
            ],
            order="id desc",
            limit=1,
        )

        if last_lot and "last_serial" in fields_list:
            res["last_serial"] = last_lot.name

        return res


    # --------------------------------------------------
    # ACTION BUTTON (ASSIGN SERIAL NUMBERS)
    # --------------------------------------------------
    def action_assign_serial(self):
        move_id = self.env.context.get("active_id")
        if not move_id:
            return super().action_assign_serial()

        # Respect manual input
        if self.first_serial:
            return super().action_assign_serial()

        move = self.env["stock.move"].browse(move_id)
        if not move or move.product_id.tracking != "serial":
            return super().action_assign_serial()

        last_lot = self.env["stock.lot"].sudo().search(
            [
                ("product_id", "=", move.product_id.id),
                ("company_id", "=", self.env.company.id),
            ],
            order="id desc",
            limit=1,
        )

        if last_lot:
            next_sn = self._next_serial(last_lot.name)
            if next_sn:
                self.first_serial = next_sn
                self.serial_count = int(move.product_uom_qty or 0)

        return super().action_assign_serial()

    # --------------------------------------------------
    # SERIAL INCREMENT LOGIC
    # --------------------------------------------------
    def _next_serial(self, serial):
        """
        Extract trailing number and increment it.
        Example:
            WH00042 -> WH00043
        """
        match = re.search(r"(\d+)$", serial)
        if not match:
            return False

        number = match.group(1)
        prefix = serial[:-len(number)]
        return f"{prefix}{str(int(number) + 1).zfill(len(number))}"
