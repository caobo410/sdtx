# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# Odoo Connector
# QQ:61365857
# 邮件:caobo@shmingjiang.org.cn
# 手机：15562666538
# 作者：'caobo'
# 公司网址： www.goderp.com
# 山东开源ERP有限公司
# 日期：2015-12-18
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
import logging
from openerp import fields,models,api
from datetime import datetime
date_ref = datetime.now().strftime('%Y-%m-%d')
_logger = logging.getLogger(__name__)

class ckgl_dddy(models.Model):
    _name = 'ckgl.dddy'
    _description = 'ckgl.dddy'

    name = fields.Char(string='订单编号', size=64,  help='订单编号')
    warehouse = fields.Char(string='仓库', size=64,  help='仓库')
    warehouse_in = fields.Char(string='调入仓库', size=64,  help='调入仓库')
    state = fields.Char(string='审批状态', size=64,  help='审批状态')
    check_user = fields.Char(string='审批人', size=64,  help='审批人')
    type = fields.Char(string='订单类型', size=64,  help='订单类型')
    send_user = fields.Char(string='收货人/发货人', size=64,  help='收货人/发货人/供应商')
    supplier = fields.Char(string='供应商', size=64,  help='供应商')
    order_code = fields.Char(string='订单编号', help='订单编号')
    tel = fields.Char(string='电话', size=64,  help='电话')
    address = fields.Char(string='发货地址', size=64,  help='发货地址')
    send_date = fields.Char(string='发货日期', size=64,  help='发货日期')
    express = fields.Char(string='快递公司', size=64,  help='快递公司')
    express_code = fields.Char(string='快递单号', size=64, help='快递单号')
    send_money = fields.Char(string='运费', size=64,  help='运费')
    number = fields.Char(string='打包件数', size=64,  help='打包件数')
    sum_money = fields.Char(string='总金额', size=64,  help='总金额')
    default_id = fields.Char(string='关联', help='关联')
    operation_date = fields.Char(string='录入日期', help='录入日期')
    operator = fields.Char(string='录入人', help='录入人')
    line_id = fields.One2many('dddy.line', 'line_id', string='明细', copy=True)
    messages = fields.Char(string='Messages', help='Messages')
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, help='Date')

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class dddy_line(models.Model):
    _name = 'dddy.line'
    _description = 'dddy.line'

    code = fields.Char(string='商品编号', size=64, help='商品编号')
    name = fields.Char(string='商品名称', size=64,  help='商品名称')
    line_id = fields.Many2one('ckgl.dddy', string='链接', select=True, track_visibility='onchange')
    spec = fields.Char(string='规格型号', size=64,  help='规格型号')
    unit = fields.Char(string='单位', size=64,  help='单位')
    number = fields.Char(string='数量', size=64,  help='数量')
    money = fields.Char(string='入库单价', size=64,  help='入库单价')
    sum_money = fields.Char(string='金额', help='金额')
    default_id = fields.Char(string='关联', help='关联')
    order_code = fields.Char(string='订单编号', help='订单编号')
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, help='Date')
    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class sdtx_pos(models.Model):
    _name = "sdtx.pos"
    _description = "sdtx.pos"

    name = fields.Char(string='订单编号', size=64, required=True, help="订单名称")
    state = fields.Char(string='订单状态', help="订单状态")
    buyers = fields.Char(string='买家', help="买家")
    shop = fields.Char(string='店铺', help="店铺")
    desk_no = fields.Char(string='桌号', help="桌号")
    people_num = fields.Char(string='就餐人数', help="就餐人数")
    sum_price = fields.Char(string='总金额', help="总金额")
    print_time = fields.Char(string='打印时间', help="打印时间")
    order_time = fields.Char(string='订单日期', help="订单日期")
    line_id = fields.One2many('pos.line', 'line_id', string='明细', copy=True)
    sum_zkb = fields.Char(string='支付折扣币', help="支付折扣币")
    sum_jf = fields.Char(string='积分', help="积分")
    sum_gwq = fields.Char(string='购物券', help="购物券")
    messages = fields.Char(string='商家留言', help="商家留言")
    QR = fields.Char(string='二维码', help="二维码")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
        'QR': 'www.76sd.com',
    }
class pos_line(models.Model):
    _name = "pos.line"
    _description = "pos.line"

    name = fields.Char(string='名称', size=64, required=True, help="名称")
    num = fields.Char(string='数量', size=64, required=True, help="数量")
    price = fields.Char(string='单价', size=64, required=True, help="单价")
    sum_price = fields.Char(string='小计', size=64, required=True, help="小计")
    line_id = fields.Many2one('sdtx.pos', string='链接', select=True, track_visibility='onchange')
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: