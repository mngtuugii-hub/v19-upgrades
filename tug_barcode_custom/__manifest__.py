{
    'name': 'Tug Barcode Custom',
    'version': '1.0',
    'summary': 'Scan packages, view contents, and move them efficiently.',
    'category': 'Inventory/Inventory',
    'author': 'Custom',
    'depends': ['stock', 'stock_barcode', 'web'],
    'data': [
        'views/stock_quant_package_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # Ensure the Service is loaded first
            'tug_barcode_custom/static/src/js/package_mover_service.js',
            'tug_barcode_custom/static/src/js/package_mover_action.js',
            'tug_barcode_custom/static/src/xml/package_mover.xml',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}