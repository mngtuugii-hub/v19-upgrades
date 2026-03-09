# tug_original_sales_order/models/mrp_production.py

from odoo import fields, models, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    original_sale_order_id = fields.Many2one(
        'sale.order',
        string='Original Sales Order',
        compute='_compute_original_sale_order_mo',
        store=True,
        help="The original Sales Order that initiated this Manufacturing Order, traced up the component chain."
    )
    # NEW FIELD: Sales Order Customer Reference
    sale_order_ref = fields.Char(
        string='SO Customer Ref',
        related='original_sale_order_id.client_order_ref',
        store=True,
        readonly=True,
        help="The Customer Reference (client_order_ref) from the linked original Sales Order."
    )

    # NEW FIELD: Sales Order Customer (Partner)
    sale_order_partner_id = fields.Many2one(
        'res.partner',
        string='SO Customer',
        related='original_sale_order_id.partner_id',
        store=True,
        readonly=True,
        help="The Customer (Partner) from the linked original Sales Order."
    )

    # The 'html' widget will automatically be used in the form view
    # Odoo typically maps 'text' fields with 'html' widget for this purpose.
    internal_production_note = fields.Html(
        string='Special Notes',
        help='Internal notes for the production team regarding the manufacturing process.',
    )

    @api.depends('origin')
    def _compute_original_sale_order_mo(self):
        SaleOrder = self.env['sale.order']
        MrpProduction = self.env['mrp.production']

        for mo in self:
            mo.original_sale_order_id = False
            
            # Start the recursive search with the current MO's origin string
            current_origin_name = mo.origin
            
            max_depth = 10  
            depth = 0

            while current_origin_name and depth < max_depth:
                depth += 1
                
                # Search term for finding the SO (must start with origin name)
                so_search_term = f"{current_origin_name}%%"
                
                # Search term for finding the intermediate MO (can contain origin name anywhere)
                # This is the key change to handle suffixes like '-MTS'.
                mo_search_term = f"%%{current_origin_name}%%" 

                # 1. CHECK FOR SALES ORDER (Goal Reached)
                # Searches for names STARTING WITH the origin string (e.g., 'S00042%')
                so = SaleOrder.search([('name', 'ilike', so_search_term)], limit=1)
                if so:
                    mo.original_sale_order_id = so.id
                    break  # Found the SO, exit the loop

                # 2. CHECK FOR MANUFACTURING ORDER (Must Trace Further)
                # Searches for names CONTAINING the origin string (e.g., '%MO/00042%')
                parent_mo = MrpProduction.search([('name', 'ilike', mo_search_term)], limit=1)
                
                if parent_mo:
                    # If found, move up the chain
                    current_origin_name = parent_mo.origin
                else:
                    # Chain is broken or leads to an unknown document, stop searching.
                    break