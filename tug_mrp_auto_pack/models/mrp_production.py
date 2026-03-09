from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # 1. The computed field to count packages
    package_count = fields.Integer(
        string='Packages', 
        compute='_compute_package_count'
    )

    # 2. The compute method for the field above
    @api.depends('move_finished_ids.move_line_ids.result_package_id')
    def _compute_package_count(self):
        for record in self:
            # Gather all move lines for finished products
            move_lines = record.move_finished_ids.mapped('move_line_ids')
            # Get unique packages from those lines
            unique_packages = move_lines.mapped('result_package_id')
            record.package_count = len(unique_packages)

    # 3. The Action method called by the XML Button
    # (This was likely missing or indented wrong causing your error)
    def action_view_mrp_packages(self):
        self.ensure_one()
        move_lines = self.move_finished_ids.mapped('move_line_ids')
        packages = move_lines.mapped('result_package_id')
        
        return {
            'name': 'Packages',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.quant.package',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', packages.ids)],
            'context': {'create': False},
        }

    # 4. The Logic to Auto-Pack when "Mark as Done" is clicked
    def button_mark_done(self):
        for production in self:
            # Check if this product category has Auto Pack enabled
            if production.product_id.categ_id.auto_pack_mrp:
                
                # Handle "Immediate Production" (if user didn't type a qty)
                if production.qty_producing == 0 and production.product_qty > 0:
                    production.qty_producing = production.product_qty
                    if hasattr(production, '_set_qty_producing'):
                        production._set_qty_producing()

                # Find valid finished moves (exclude cancelled/done ones)
                finished_moves = production.move_finished_ids.filtered(
                    lambda m: m.product_id == production.product_id and m.state not in ('done', 'cancel')
                )

                if finished_moves:
                    # Create the Package
                    package = self.env['stock.quant.package'].create({
                        'name': self.env['ir.sequence'].next_by_code('stock.quant.package') or 'PACK-AUTO-MRP'
                    })

                    # Assign Package to the lines
                    for move in finished_moves:
                        # Ensure lines exist
                        if not move.move_line_ids:
                            vals = move._prepare_move_line_vals(quantity=move.quantity or move.product_uom_qty)
                            self.env['stock.move.line'].create(vals)
                        
                        # Update lines with the package
                        move.move_line_ids.write({
                            'result_package_id': package.id
                        })

        # Call the original Odoo function
        return super(MrpProduction, self).button_mark_done()