{
    'name': "Tug: Original Sales Order Tracer",
    'summary': """
        Traces and links the original Sales Order (SO) that triggered a Purchase Order (PO).
    """,
    'description': """
        Adds a computed Many2one field to the Purchase Order model to trace the original 
        Sales Order, even if the chain goes through an intermediate document (like a 
        Manufacturing Order or another Picking).
    """,
    'author': "Tug",
    'website': "http://www.yourcompany.com",
    'category': 'Sales/Purchase',
    'version': '19.0.1.0.0',
    'depends': [
        'purchase',     
        'sale_management', 
        'mrp',          
        'stock',
    ],
    'data': [
        'views/purchase_order_views.xml',
        'views/mrp_production_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
}