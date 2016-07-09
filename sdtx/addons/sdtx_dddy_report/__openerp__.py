# -*- coding: utf-8 -*-
{
    'name': "sdtx_dddy_report",

    'summary': """
        dddy_report""",

    'description': """
        该模块由明匠报表代码快速生成器生成
    """,

    'author': "MJ",
    'website': "http://www.shmingjiang.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'report',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'report_gt_bz.xml',
        'report_gt_pt.xml',
        'report_yd_pt.xml',
        'report_yt_pt.xml',
        'report_kj_pt.xml',
        # 'report_sf.xml',
        # 'report_sf_print.xml',
        # 'report_st.xml',
        # 'report_st_print.xml',
        # 'report_yd_print.xml',
        # 'report_yt.xml',
        # 'report_yt_print.xml',
        # 'report_zt.xml',
        # 'report_zt_print.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
    'application': True,
}