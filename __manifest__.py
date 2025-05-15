{
    'name': 'Base Odoo module',
    'version': '17.0',
    'category': 'Administration',
    'author': "Self Ltd",
    'website': "https://example.com",
    'license': 'LGPL-3',
    'images': ['static/logo-sq100.png'],
    'summary': 'Base Odoo module',
    # docxtpl
    'depends': ['base', 'mail', 
                'web',
                # oca
                'fs_storage', 'fs_attachment',
                'fs_image', 'fs_file', 
    ],
    # wip depends on oca fs_attachment & fs_storage
    # 'fs_storage', 'fs_attachment'
    'description': """Base module""",
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/menu.xml',
    ],
    "external_dependencies": {"python": ["docxtpl", "openpyxl"]},
    'images': ['static/img/icons/logo-sq100.jpg'],
    'installable': True,
    'application': True,
    'auto_install': False,
	"assets": {
        "web.assets_backend": [
            "base_om/static/src/control-panel/cp.js",
            "base_om/static/src/control-panel/cp.xml",
            "base_om/static/src/control-panel/cmodal.xml",
        ],
    }
}
