# tug_original_sales_order/models/stock_picking.py

from odoo import fields, models, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Compute + Store + Readonly=False allows auto-calculation AND manual editing
    original_sale_order_id = fields.Many2one(
        'sale.order',
        string='Original Sales Order',
        compute='_compute_original_sale_order_picking',
        store=True,
        readonly=False,
        help="The original Sales Order that initiated this transfer. Can be manually changed."
    )
    
    sale_order_ref = fields.Char(
        string='SO Customer Ref',
        related='original_sale_order_id.client_order_ref',
        store=True,
    )
    
    sale_order_partner_id = fields.Many2one(
        'res.partner',
        string='SO Customer',
        related='original_sale_order_id.partner_id',
        store=True,
    )
    internal_production_note = fields.Html(
        string='Special Notes',
        help='Internal notes for the production team regarding the manufacturing process.',
    )
    @api.depends('origin')
    def _compute_original_sale_order_picking(self):
        SaleOrder = self.env['sale.order']
        MrpProduction = self.env['mrp.production']
        PurchaseOrder = self.env['purchase.order']

        for picking in self:
            # If manually set by a user, do not overwrite it
            if picking.original_sale_order_id:
                continue

            current_origin_name = picking.origin
            so_id = False
            max_depth = 10
            depth = 0

            while current_origin_name and depth < max_depth:
                depth += 1
                
                # 1. CHECK FOR SALES ORDER
                so = SaleOrder.search([('name', 'ilike', f"{current_origin_name}%%")], limit=1)
                if so:
                    so_id = so.id
                    break

                # 2. CHECK FOR MANUFACTURING ORDER
                parent_mo = MrpProduction.search([('name', 'ilike', f"%%{current_origin_name}%%")], limit=1)
                if parent_mo:
                    current_origin_name = parent_mo.origin
                    continue

                # 3. CHECK FOR PURCHASE ORDER (If picking is a receipt from a PO)
                parent_po = PurchaseOrder.search([('name', 'ilike', f"%%{current_origin_name}%%")], limit=1)
                if parent_po:
                    current_origin_name = parent_po.origin
                    continue
                    
                # Chain broken
                break
            
            # Set the calculated value
            picking.original_sale_order_id = so_id