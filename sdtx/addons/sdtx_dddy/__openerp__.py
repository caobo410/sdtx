# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Odoo Connector
# QQ:61365857
# 邮件:caobo@shmingjiang.org.cn
# 手机：15562666538
# 作者：'caobo'
# 公司网址： www.shmingjiang.org.cn
# 上海明匠智能有限公司
# 日期：2015-12-18
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
{
    'name': 'sdtx dddy',
    'summary': '描述',
    'version': '1.0',
    'category': 'Tools',
    'sequence': 0,
    'author': 'caobo',
    'website': 'http://www.shmingjiang.com',
    'depends': ['base','report',],
    'data': [
        'views/dddy_view.xml',
        'views/address_view.xml',
        'views/import_view.xml',
        'views/distribute_order.xml',
        'views/express.xml',
        'views/merge_order.xml',
        #'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
模块功能
==================================
zzzzz

功能
-------------
* xxxxxxxxx
""",
}



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

