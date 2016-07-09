# -*- coding: utf-8 -*-
import base64
from openerp.osv import fields, osv
import httplib, urllib


class Report(osv.Model):
    _inherit = 'report'

    def render(self, cr, uid, ids, template, values=None, context=None):
        if values is None:
            values = {}
        else:
            if values['doc_ids']:
                express_objs=[]
                i = 0
                for doc_id in values['doc_ids']:
                    doc_model = values['doc_model']
                    return
                    if doc_model == 'sdtx.dddy':
                        sdtx_dddy_obj = self.pool['sdtx.dddy']
                        sdtx_dddy_id_obj = sdtx_dddy_obj.search(cr, uid, [('id', '=', doc_id)])
                        if sdtx_dddy_id_obj:
                            sdtx_dddy_print_obj = sdtx_dddy_obj.browse(cr, uid, sdtx_dddy_id_obj[0])
                            sdtx_dddy_obj.write(cr, uid, sdtx_dddy_print_obj.id,{'is_print': 'yes'}, context)
                            i = i+1
                            express_name = sdtx_dddy_print_obj.express_id.field
                            express_name =express_name.encode('utf-8')
                            rec_id = sdtx_dddy_print_obj.rec_id
                            rec_id = str(rec_id)
                            express = sdtx_dddy_print_obj.express
                            express =express.encode('utf-8')
                            if i == 1:
                                str_express = rec_id+u'_'+express + u','
                            else:
                                str_express = str_express+rec_id+u'_'+express+u','
                missing_padding = 4 - len(str_express) % 4
                if missing_padding:
                    str_express += b'='* missing_padding
                str_express = str_express.encode('utf-8')
                strs_express = base64.b64encode(str_express)
                httpClient = None
                try:
                    params = urllib.urlencode({'rec_id': strs_express, 'wlcode': express_name})
                    headers = {"Content-type": "application/x-www-form-urlencoded"
                        , "Accept": "text/plain"}
                    httpClient = httplib.HTTPConnection("wl.76sd.com", 80, timeout=30)
                    httpClient.request("POST", "/index.php?s=/sd/Common/printStatus", params, headers)
                    response = httpClient.getresponse()
                    # print response.status
                    # print response.reason
                    # print response.read()
                    # print response.getheaders() #获取头信息
                except Exception, e:
                    print '22222'
                    print e
                finally:
                    if httpClient:
                        httpClient.close()
            return super(Report, self).render(cr, uid, ids, template, values, context)

    # def httplib(self,values=None):
    #     if values is None:
    #         values = {}
    #         return
    #     else:
    #         httpClient = None
    #         try:
    #             params = urllib.urlencode(express_objs)
    #             # headers = {"Content-type": "application/x-www-form-urlencoded"
    #             #     , "Accept": "text/plain"}
    #             httpClient = httplib.HTTPConnection("localhost", 8069, timeout=30)
    #             httpClient.request("POST", "/ceshi/", params)
    #
    #             response = httpClient.getresponse()
    #             print response.status
    #             print response.reason
    #             print response.read()
    #             print response.getheaders() #获取头信息
    #         except Exception, e:
    #             print e
    #         finally:
    #             if httpClient:
    #                 httpClient.close()