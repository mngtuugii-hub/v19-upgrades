{
    'name': 'Tug: Manufacturing Order: Mods, Reports',
    'version': '2.11', # Bumped version
    'category': 'Manufacturing',
    'summary': 'Custom Manufacturing Order Reports & Email Wizard',
    'depends': ['mrp', 'mail', 'stock'], # Added 'stock' back as we are modifying Transfers
    'data': [
        'security/ir.model.access.csv',
        'reports/report_action.xml',
        'data/mail_template_data.xml',
        'data/printnode_setup_action.xml',
        'wizard/mrp_report_wizard_view.xml',
        'views/mrp_view.xml',
        'views/stock_picking_view.xml', # Added Picking View
        'reports/report_internal_template.xml',
        'reports/report_external_template.xml',
        'reports/report_package_zpl_template.xml',
    ],
    'installable': True,
    'application': False,
}