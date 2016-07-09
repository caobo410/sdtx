# -*- coding: utf-8 -*-
from openerp import http, fields
import rest
import authorizer
from datetime import datetime

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


date_ref = datetime.now().strftime('%Y-%m-%d')
# _logger = logging.getLogger(__name__)

class OrderController(http.Controller):
    @authorizer.authorize
    @http.route('/api/sdtx_dddy/<database>', type='http', auth='none', methods=['post'])
    def sdtx_dddy(self, database, login, password, rec_id, goods_name, order_sn, status, order_status, ent_id, consignee, address, city, phone_tel):
        if rec_id is None or goods_name is None or order_sn is None or order_status is None:
            return rest.render_json({'No': 'fields is null'})
        if ent_id is None or consignee is None or address is None or city is None or phone_tel is None:
            return rest.render_json({'No': 'fields is null'})
        warehouse_obj = self.current_env['sdtx.warehouse'].search([('name', '=', str(ent_id))])
        dddy_obj = self.current_env['sdtx.dddy'].search([('rec_id', '=', str(rec_id))])
        if not warehouse_obj or not dddy_obj:
            values = {
                'sender': warehouse_obj['sender'],
                'sender_tel': warehouse_obj['sender_tel'],
                'sender_phone': warehouse_obj['sender_tel'],
                'sender_city': warehouse_obj['sender_city'],
                'sender_street': warehouse_obj['sender_street'],
                'address_id': warehouse_obj['name'],
                'rec_id': str(rec_id),
                'commodity': goods_name,
                'name': str(order_sn),
                'status': order_status,
                'commodity_status': status,
                'is_print': 'no',
                'recipient': consignee,
                'recipient_street': address,
                'recipient_city': city,
                'recipient_tel': phone_tel,
            }
            self.current_env['sdtx.dddy'].create(values)
        return rest.render_json({'Yes': 'ok'})

    @authorizer.authorize
    @http.route('/api/sdtx_warehouse/<database>', type='http', auth='none', methods=['post'])
    def sdtx_warehouse(self, database, login, password, id, name, principal, mobile, title, city, address):
        if id is None or name is None or principal is None or mobile is None:
            return rest.render_json({'No': 'fields is null'})
        if title is None or city is None or address is None:
            return rest.render_json({'No': 'fields is null'})
        warehouse_obj = self.current_env['sdtx.warehouse'].search([('name', '=', str(id))])
        user_obj = self.current_env['res.users'].search([('name', '=', str(principal))])
        if user_obj:
            sender = user_obj.id
        else:
            sender = '1'
        if not warehouse_obj:
            values = {
                'name': str(id),
                'warehouse': name,
                'sender': sender,
                'sender_street': address,
                'sender_tel': mobile,
                'sender_city': city,
                'messages': title,
            }
            self.current_env['sdtx.warehouse'].create(values)
        return rest.render_json({'Yes': 'ok'})

    @authorizer.authorize
    @http.route('/api/sdtx_express/<database>', type='http', auth='none', methods=['post'])
    def sdtx_express(self, database, login, password, field, name):
        if fields is None or name is None:
            return rest.render_json({'No': 'fields is null'})
        express_obj = self.current_env['sdtx.express'].search([('field', '=', str(field))])
        max_code = self.current_env['sdtx.express'].search([], order="code DESC")
        max_code = max_code and max_code[0]['code'] or 0
        if not express_obj:
            max_code = '0000' + str(int(max_code)+1)
            max_code = max_code[-4:]
            values = {
                'code': max_code,
                'name': name,
                'field': fields,
            }
            self.current_env['sdtx.express'].create(values)
        return rest.render_json({'Yes': 'ok'})