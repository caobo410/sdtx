# -*- coding: utf-8 -*-
import logging
from openerp import fields,models,api
from datetime import datetime
import httplib2
date_ref = datetime.now().strftime('%Y-%m-%d')
_logger = logging.getLogger(__name__)


class sdtx_dddy(models.Model):
    _name = "sdtx.dddy"
    _description = "sdtx.dddy"

    name = fields.Char(string='code', size=64, required=True, help="code")
    defaut_id = fields.Float(string='defaut_id', size=64, help="defaut_id")
    status = fields.Char(string='status', size=64, help="status")
    sender = fields.Many2one('res.users', string='Sender', select=True, track_visibility='onchange')
    # sender = fields.Char(string='Sender', size=64, required=True, help="Sender")
    sender_tel = fields.Char(string='Sender Tel', size=64, help="Sender Tel")
    sender_phone = fields.Char(string='Sender Phone', size=64, help="Sender Phone")
    sender_city = fields.Char(string='Sender City', size=64, help="Sender City")
    sender_street = fields.Char(string='Sender Street', size=64, help="Sender Street")
    warehouse_id = fields.Many2one('sdtx.warehouse', string='WareHouse', select=True, track_visibility='onchange')
    recipient = fields.Char(string='Recipient', size=64, required=True, help="Recipient")
    recipient_tel = fields.Char(string='Recipient Tel', size=64, required=True, help="Recipient Tel")
    recipient_city = fields.Char(string='Recipient City', size=64, required=True, help="Recipient City")
    recipient_street = fields.Char(string='Recipient_Street', size=64, help="Recipient_Street")
    total_price = fields.Char(string='Total Price', size=64, help="Total Price")
    commodity = fields.Char(string='Commodity', required=True, size=64, help="Commodity")
    logistics = fields.Char(string='Logistics', size=64, help="Logistics")
    payment_time = fields.Datetime(string='Payment Time', size=64, help="Payment Time")
    order_time = fields.Datetime(string='Order Time', size=64, help="Order Time")
    express = fields.Char(string='Express code', size=64, help="Express code")
    express_id = fields.Many2one('sdtx.express', string='Express', select=True, track_visibility='onchange')
    commodity_status = fields.Char(string='Commodity status', size=64, help="Commodity status")
    is_print = fields.Selection([('yes', 'YES'),('no','No')], 'Is print', required=True, help="Is print")
    number = fields.Float(string='Num', size=64, help="Num")
    price = fields.Float(string='Price', size=64, help="Price")
    wight = fields.Float(string='Wight', size=64, help="Wight")
    type = fields.Char(string='Type', size=64, help="Type")
    rec_id = fields.Char(string='Rec Id', size=64, help="Rec Id")
    messages = fields.Char(string='Messages', size=64, help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, help="Date")


    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
        'number': 0,
        'price': 0,
        'wight': 0,
        'is_print': 'no',
    }

class sdtx_address(models.Model):
    _name = "sdtx.warehouse"
    _description = "sdtx.warehouse"

    name = fields.Char(string='Code', size=64, required=True, help="Code")
    warehouse = fields.Char(string='Warehouse', size=64, required=True, help="Warehouse")
    sender = fields.Many2one('res.users', string='Sender', select=True, track_visibility='onchange')
    sender_tel = fields.Char(string='Sender Tel', size=64, help="Sender Tel")
    sender_phone = fields.Char(string='Sender Phone', size=64, help="Sender Phone")
    sender_city = fields.Char(string='Sender City', size=64, help="Sender City")
    sender_street = fields.Char(string='Sender Street', size=64, help="Sender Street")
    messages = fields.Char(string='Messages', size=64, help="Messages")
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, help="Date")

    @api.multi
    def name_get(self):
        result = []
        for inv in self:
            name = inv.warehouse + ' (' + inv.name + ')'
            result.append((inv.id, name))
        return result

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

class sdtx_import(models.Model):
    _name = "sdtx.import"
    _description = "sdtx.import"

    name = fields.Char(string='code', size=64, required=True, help="code")
    operate_time = fields.Datetime(string='Operate Time', select=True, copy=False)
    user_id = fields.Many2one('res.users', string='Operator')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    @api.one
    def but_import_warehouse(self):
        #接受仓库数据
        try:
            urlstr = 'http://api.76sd.com/repertory/repertorylist'
            http = httplib2.Http('.cache')
        except:
            print "连接不上"
        else:
            response,content = http.request(urlstr)
            content_obj = eval(content)
            data_objs = content_obj['data']
            for data_obj in data_objs:
                warehouse_obj = self.env['sdtx.warehouse'].search([('name','=', str(data_obj['id']))])
                if not warehouse_obj:
                    values = {
                        'name': str(data_obj['id']),
                        'warehouse': data_obj['name'].decode('raw_unicode_escape'),
                        'sender': data_obj['principal'].decode('raw_unicode_escape'),
                        'sender_street': data_obj['address'].decode('raw_unicode_escape'),
                        'sender_tel': data_obj['mobile'].decode('raw_unicode_escape'),
                        'sender_city': data_obj['province'].decode('raw_unicode_escape')+data_obj['city'].decode('raw_unicode_escape')+data_obj['area'].decode('raw_unicode_escape'),
                        'messages': data_obj['title'].decode('raw_unicode_escape'),
                    }
                    self.env['sdtx.warehouse'].create(values)
    @api.one
    def but_import_ddlb(self):
        # 接受订单信息
        try:
            urlstr = 'http://wl.76sd.com/index.php?s=/sd/Common/dyorder'
            http = httplib2.Http('.cache')
        except:
            print "连接不上"
        else:
            response,content = http.request(urlstr)
            content_obj = eval(content.replace(':null',':"nothing"'))
            order_objs = content_obj['data']
            for order_obj in order_objs:
                dddy_obj = self.env['sdtx.dddy'].search([('rec_id', '=', str(order_obj['rec_id']))])
                warehouse_obj = self.env['sdtx.warehouse'].search([('name', '=', str(order_obj['ent_id']))])
                if not dddy_obj and warehouse_obj:
                    values = {
                        'sender': warehouse_obj['sender'],
                        'sender_tel': warehouse_obj['sender_tel'],
                        'sender_phone': warehouse_obj['sender_tel'],
                        'sender_city': warehouse_obj['sender_city'],
                        'sender_street': warehouse_obj['sender_street'],
                        'warehouse_id': warehouse_obj['id'],
                        'rec_id': str(order_obj['rec_id']),
                        'commodity': order_obj['goods_name'].decode('raw_unicode_escape'),
                        'name': order_obj['order_sn'].decode('raw_unicode_escape'),
                        'status': order_obj['order_status'].decode('raw_unicode_escape'),
                        'commodity_status': order_obj['status'].decode('raw_unicode_escape'),
                        'sender_province': order_obj['ent_name'].decode('raw_unicode_escape'),
                        'logistics': order_obj['shipcode'].decode('raw_unicode_escape'),
                        'sender_area': order_obj['ent_id'].decode('raw_unicode_escape'),
                        'payment_time': order_obj['time'].decode('raw_unicode_escape'),
                        'order_time': order_obj['add_time'].decode('raw_unicode_escape'),
                        'is_print': 'no',
                        'recipient': order_obj['consignee'].decode('raw_unicode_escape'),
                        'recipient_street': order_obj['address'].decode('raw_unicode_escape'),
                        'recipient_city': order_obj['sheng'].decode('raw_unicode_escape')+' '+order_obj['shi'].decode('raw_unicode_escape')+' '+order_obj['xian'].decode('raw_unicode_escape'),
                        'recipient_tel': order_obj['phone_tel'].decode('raw_unicode_escape'),
                    }
                    print values
                    self.env['sdtx.dddy'].create(values)
    @api.one
    def but_import_wlxx(self):
        try:
            urlstr = 'http://wl.76sd.com/index.php?s=/sd/Common/wuliu'
            http = httplib2.Http('.cache')
        except:
            print "连接不上"
        else:
            response,content = http.request(urlstr)
            content_obj = eval(content.replace(':null',':"nothing"'))
            data_objs = content_obj['data']
            max_code = '0'
            max_code = self.env['sdtx.express'].search([], order="code DESC")
            max_code = max_code and max_code[0]['code'] or 0
            for k in data_objs:
                express_obj = self.env['sdtx.express'].search([('name', '=', data_objs[k].decode('raw_unicode_escape'))])
                if not express_obj:
                    max_code = '0000' + str(int(max_code)+1)
                    max_code = max_code[-4:]
                    values = {
                        'code': max_code,
                        'name': data_objs[k].decode('raw_unicode_escape'),
                        'field': k,
                    }
                    self.env['sdtx.express'].create(values)
    _defaults = {
        'operate_time': datetime.now(),
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }