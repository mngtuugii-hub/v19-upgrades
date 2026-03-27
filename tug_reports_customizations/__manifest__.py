# -*- coding: utf-8 -*-
{
    'name': 'Tug Reports Customizations',
    'version': '1.0',
    'category': 'Inventory/Inventory',
    'summary': 'Customizes the Stock Picking Operation Report',
    'description': """
        This module replaces the inner content of the default 
        stock picking report template (stock.report_picking).
    """,
    'depends': ['stock', 'mrp'],
    'data': [
        'views/report_picking.xml',
        'views/report_delivery_slip.xml',
        'views/report_bom_overview.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'author': 'Tug',
}