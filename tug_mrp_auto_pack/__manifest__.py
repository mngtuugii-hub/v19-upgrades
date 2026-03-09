{
    'name': 'MRP Auto Pack',
    'version': '1.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Automatically put finished goods in a package upon completion',
    'description': """
        Adds a configuration to Product Categories.
        If enabled, finished goods are automatically assigned a new package 
        when the Manufacturing Order is marked as Done.
    """,
    'depends': ['mrp', 'stock'],
    'data': [
        'views/product_category_views.xml',
        'views/mrp_production_views.xml',  # Add this line
    ],
    'installable': True,
    'license': 'LGPL-3',
}