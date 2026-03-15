{
    'name': 'Tug: Manufacturing Order: Mods, Reports',
    'version': '3.4',
    'category': 'Manufacturing',
    'summary': """
        Comprehensive Manufacturing Suite for Odoo 19: 
        1. Advanced PDF Reporting: Professional Internal & External MO reports with automated barcode/GS1 integration.
        2. Production Logistics: Dynamic 'Update from BoM' tool for rapid component re-alignment and separate packaging logic for stock transfers.
        3. Quality Control (QFM): Full suite of digitalized compliance checklists (QFM-067, 084, 091, 092) for blending and filling operations.
        4. ZPL Labeling & Direct Print: Automated ZPL label generation for packages/pallets with built-in Direct Print (PrintNode) scenario configuration.
        5. Email Wizard: Tablet-friendly UI for instant customer notifications with auto-attached PDF production specs.
    """,
    'author': 'Tug',
    'license': 'LGPL-3',
    'depends': ['mrp', 'mail', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'reports/paperformat.xml',
        'reports/report_action.xml',
        'data/mail_template_data.xml',
        'data/printnode_setup_action.xml',
        'wizard/mrp_report_wizard_view.xml',
        'views/mrp_view.xml',
        'views/stock_picking_view.xml',
        'reports/report_internal_template.xml',
        'reports/report_external_template.xml',
        'reports/report_package_zpl_template.xml',
        'reports/report_package_sscc_zpl.xml',
        'reports/report_pallet_label.xml',
        'reports/report_sample_label_zpl.xml',
        'reports/report_qfm_067.xml',
        'reports/report_qfm_084.xml',
        'reports/report_qfm_091.xml',
        'reports/report_qfm_092.xml',
    ],
    'installable': True,
    'application': False,
}