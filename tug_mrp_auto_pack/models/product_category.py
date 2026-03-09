from odoo import fields, models

class ProductCategory(models.Model):
    _inherit = 'product.category'

    auto_pack_mrp = fields.Boolean(
        string="Auto Pack on Manufacture",
        help="If checked, products in this category will be automatically put into a new package when the Manufacturing Order is marked as Done."
    )