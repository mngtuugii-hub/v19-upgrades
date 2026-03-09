# tug_original_sales_order/models/purchase_order.py

from odoo import fields, models, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # The Many2one field that links to the original Sales Order
    original_sale_order_id = fields.Many2one(
        'sale.order',
        string='Original Sales Order',
        compute='_compute_original_sale_order',
        store=True, # Stores the result in the database for searching and performance
        help="The original Sales Order that initiated this Purchase Order, traced through the 'Origin' chain."
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
    internal_production_note = fields.Html(
        string='Special Notes',
        help='Internal notes for the production team regarding the manufacturing process.',
    )
    @api.depends('origin')
    def _compute_original_sale_order(self):
        """
        Computes the original Sales Order by tracing the 'origin' field 
        of the current Purchase Order and its intermediate documents.
        """
        SaleOrder = self.env['sale.order']
        MrpProduction = self.env['mrp.production']

        for po in self:
            po.original_sale_order_id = False  # Reset before calculation

            # 1. Direct Trace (e.g., SO -> PO)
            if po.origin:
                so = SaleOrder.search([('name', '=', po.origin)], limit=1)
                if so:
                    po.original_sale_order_id = so.id
                    continue

            # 2. Indirect Trace through Manufacturing (e.g., SO -> MO -> PO)
            if po.origin:
                # Check if the origin matches a Manufacturing Order name
                mo = MrpProduction.search([('name', '=', po.origin)], limit=1)
                
                if mo and mo.origin:
                    # Check the MO's origin for a Sales Order name
                    so_from_mo_origin = SaleOrder.search([('name', '=', mo.origin)], limit=1)
                    
                    if so_from_mo_origin:
                        po.original_sale_order_id = so_from_mo_origin.id
                        continue