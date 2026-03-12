from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_clear_destination_packages(self):
        """
        Clears destination packages from all move lines and removes package levels
        to prevent 'cannot move same package content' errors.
        """
        for picking in self:
            # 1. Remove the 'Entire Package' reservation (Package Levels).
            # This is CRITICAL to fix the "cannot move same package" error.
            # It forces Odoo to treat the move as 'Product' moves, not 'Box' moves.
            if picking.package_level_ids:
                picking.package_level_ids.unlink()

            # 2. Clear the Destination Package on all detailed operations (move lines)
            lines_with_packages = picking.move_line_ids.filtered(lambda l: l.result_package_id)
            if lines_with_packages:
                lines_with_packages.write({'result_package_id': False})

        return True