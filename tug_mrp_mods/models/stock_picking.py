from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_put_in_separate_packs(self):
        """ 
        Iterates over all move lines in the picking that have a quantity done 
        but are not yet in a package. Creates a new package for EACH line individually.
        """
        for picking in self:
            # Filter: Quantity > 0 AND No Package assigned yet
            lines_to_pack = picking.move_line_ids.filtered(
                lambda l: l.quantity > 0 and not l.result_package_id
            )
            
            for line in lines_to_pack:
                # Create a new package for this specific line
                new_package = self.env['stock.quant.package'].create({})
                # Assign the package to the line
                line.result_package_id = new_package
        
        return True