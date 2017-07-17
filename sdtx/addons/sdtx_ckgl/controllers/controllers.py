# -*- coding: utf-8 -*-
from openerp import http, fields,api
import rest
import authorizer
from datetime import datetime
import random

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

date_ref = datetime.now().strftime('%Y-%m-%d')
# _logger = logging.getLogger(__name__)
class OrderController(http.Controller):
    @authorizer.authorize
    @http.route('/api/sdtx_ckgl/<database>', type='http', auth='none', methods=['GET'])
    def sdtx_ckgl(self, database, login, password, type, warehouse_list, line_list):
        if type:
            if type == u'8':
                name = u'销售出库单'
                print_name = u'sdtx_ckgl_report.report_sdtx_xsck_main'
            elif type == u'9':
                name = u'销售退货单'
                print_name = u'sdtx_ckgl_report.report_sdtx_xsth_main'
            elif type == u'1':
                name = u'采购入库单'
                print_name = u'sdtx_ckgl_report.report_sdtx_cgrk_main'
            elif type == u'2':
                name = u'采购退货单'
                print_name = u'sdtx_ckgl_report.report_sdtx_cgth_main'
            elif type == u'5':
                name = u'调拨单'
                print_name = u'sdtx_ckgl_report.report_sdtx_dbd_main'
            elif type == u'3':
                name = u'其他出库单'
                print_name = u'sdtx_ckgl_report.report_sdtx_qtck_main'
            elif type == u'4':
                name = u'其他入库单'
                print_name = u'sdtx_ckgl_report.report_sdtx_qtrk_main'
            else:
                return rest.render_json({'status': 'no', 'message': u'type类型不正确！'})
        else:
            return rest.render_json({'status': 'no', 'message': u'type不能为空！'})
        if not warehouse_list:
            return rest.render_json({'status': 'no', 'message': name + u'不能为空！'})
        if not line_list:
            return rest.render_json({'status': 'no', 'message': name + u'商品明细不能为空！'})
        try:
            warehouse_list = warehouse_list.replace('\"', '\'')
            line_list = line_list.replace('\"', '\'')
            warehouse_list = warehouse_list.replace('fail', ' ')
            line_list = line_list.replace('fail', ' ')
            warehouse_list = warehouse_list.decode('unicode-escape')
            line_list = line_list.decode('unicode-escape')
            warehouse_values = eval(warehouse_list)
            line_values = eval(line_list)
        except:
            return rest.render_json({'status': 'no', 'message': u'warehouse_values/line_values参数有问题！'})
        sjs = str(random.randint(100, 999))
        str_time = str(datetime.now())
        filename = str_time[:4] + str_time[5:7] + str_time[8:10] + str_time[11:13] + str_time[14:16] + str_time[17:18] + type + sjs
        self.current_env.cr.execute('delete from ckgl_dddy;delete from dddy_line')
        sdtx_ckgl_obj = self.current_env['ckgl.dddy']
        sdtx_ckgl_line_obj = self.current_env['dddy.line']
        for warehouse_value in warehouse_values:
            sdtx_ckgl_obj.create(warehouse_value)
        for line_value in line_values:
            ckgl_obj = sdtx_ckgl_obj.search([('default_id', '=', line_value['default_id'])])
            line_value['line_id'] = ckgl_obj.id
            sdtx_ckgl_line_obj.create(line_value)
        report_objs = self.current_env['report']
        ckgl_objs = sdtx_ckgl_obj.search([])
        values = report_objs.get_pdf(ckgl_objs, print_name)
        return rest.render_pdf(values, filename)
    @authorizer.authorize
    @http.route('/api/sdtx_pos/<database>', type='http', auth='none', methods=['GET'])
    def sdtx_pos(self, database, login, password, pos_list, line_list, qr_list):
        try:
            pos_list = pos_list.replace('\"', '\'')
            line_list = line_list.replace('\"', '\'')
            pos_list = pos_list.replace('fail', ' ')
            line_list = line_list.replace('fail', ' ')
            if pos_list == '' or pos_list == 'null':
                return rest.render_json({'status': u'no', 'message': u'pos_list/line_list彐版楫棰锛'})
            pos_list = pos_list.decode('unicode-escape')
            pos_values = eval(pos_list)
            if line_list != '' and line_list != 'null':
                line_list = line_list.decode('unicode-escape')
                line_values = eval(line_list)
            qr_list = qr_list.decode('unicode-escape')
            qr_values = eval(qr_list)
        except:
            return rest.render_json({'status': u'no', 'message': u'pos_list/line_list参数有问题！'})
        sjs = str(random.randint(100, 999))
        str_time = str(datetime.now())
        filename = str_time[:4] + str_time[5:7] + str_time[8:10] + str_time[11:13] + str_time[14:16] + str_time[17:18] + sjs
        self.current_env.cr.execute('delete from sdtx_pos;delete from pos_line')
        pos_obj = self.current_env['sdtx.pos']
        pos_line_obj = self.current_env['pos.line']
        # print qr_values['shangjia_id']
        pos_values['QR'] = u'http://m.76sd.com/storeOrder/inputPrice?shangjia_id=' + qr_values['shangjia_id'] + u'%26order_id=' + '' + qr_values['order_id']
        # print pos_values['QR']
        pos_obj_id = pos_obj.create(pos_values)
        if line_list != '' and line_list != 'null':
            for line_value in line_values:
                line_value['line_id'] = pos_obj_id.id
                pos_line_obj.create(line_value)
        report_objs = self.current_env['report']
        pos_print_obj = pos_obj.search([])
        print_name = u'sdtx_ckgl_report.report_sdtx_pos_main'
        values = report_objs.get_pdf(pos_print_obj, print_name)
        return rest.render_pdf(values, filename)