{
    'name': 'Estado de  Compras - Recepcion',
    'version': '1.0',
    'summary': '',
    'author': 'FPC Technology',
    'website': 'https://fpc-technology.com/',
    'license': 'LGPL-3',
    'depends': [
        'base', "stock", "purchase"
    ],
    "data" : [
        "security/ir.model.access.csv",
        "wizard/wizard_compras_descuento.xml",
        "view/inherit_form_compras.xml",
    ],
    'auto_install': False,
    'application': True,
}