from odoo import models, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_update_from_bom(self):
        """ Re-computes the raw moves based on the selected BOM. """
        for production in self:
            if production.state in ['done', 'cancel']:
                raise UserError(_('Cannot update a MO that is Done or Cancelled.'))
            
            # 1. Unreserve any allocated stock so we can modify lines
            production.do_unreserve()
            
            # 2. Delete existing component moves (raw moves)
            # Only delete lines that are not done
            moves_to_unlink = production.move_raw_ids.filtered(lambda m: m.state != 'done')
            moves_to_unlink.unlink()
            
            # 3. Re-generate moves from BOM
            if production.bom_id:
                moves_values = production._get_moves_raw_values()
                production.env['stock.move'].create(moves_values)
                
        return True
