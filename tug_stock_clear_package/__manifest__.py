{
    'name': 'Tug Clear Destination Packages',
    'version': '17.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Adds a button to clear all destination packages on a transfer.',
    'description': """
        Adds a 'Clear Dest. Packages' button to the Stock Picking (Transfer) header.
        - Clears 'result_package_id' on all move lines.
        - Deletes 'package_level_ids' to prevent 'You cannot move the same package content' errors.
    """,
    'author': 'Tug Ser',
    'depends': ['stock'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}