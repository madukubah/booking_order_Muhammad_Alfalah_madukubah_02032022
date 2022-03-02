{
    'name': 'Booking Order',
    'version': '1.0',
    'author': 'Muhammad Alfalah Madukubah',
    'category': 'Sales',
    'depends':[
        'sale'
    ],
    'data':[
        'views/service_team.xml',
        'views/sale_order.xml',
        'views/work_order.xml',
        'views/menu.xml',

        'wizard/message_alert.xml',
        'wizard/work_order_cancel.xml',

        'data/work_order.xml',

        'report/report_work_order.xml',
        'report/report_work_order_temp.xml',
    ],
    'installable': True,
    'application': False,
}