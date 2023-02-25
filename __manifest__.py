{
    'name': 'customreport',
    'version': '1.0',
    'depends': ['sale', 'product'],
    'data': [
        'views/product_template_views.xml',
        'report/product_reports.xml',
        'report/product_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'new_sales_report/static/src/js/**/*',
        ],
    },
    'installable': True,
    'application': False,
}