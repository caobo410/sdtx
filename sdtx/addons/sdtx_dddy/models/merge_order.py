# -*- coding: utf-8 -*-
import logging
from openerp import fields,models,api
from datetime import datetime
from openerp.tools.translate import _
import string

date_ref = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
_logger = logging.getLogger(__name__)

class merge_order(models.Model):
    """
    This wizard will confirm the all the selected draft invoices
    """
    _name = "merge.order"
    _description = "merge.order"

    name = fields.Text('order')
    date_time = fields.Datetime('Date', required=True, readonly=True)
    user_id = fields.Many2one('res.users', string='Operator', readonly=True, select=True, track_visibility='onchange')

    _defaults = {
        'date_time': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }

    @api.multi
    def merge_order(self):
        if self.env.context is None:
            self.env.context = {}
        active_ids = self.env.context.get('active_ids', []) or []
        proxy = self.pool['sdtx.dddy'].browse(self.env.cr,self.env.uid,active_ids,context=None)
        order_name = ''
        i = 0
        for record in proxy:
            i=i+1
            if i == 1:
                order_name = record.name
            else:
                order_name = order_name +' '+ record.name
                record.update({'is_print': 'yes'})
        self.name = order_name
        print order_name
        print self.name
        return {'type': 'ir.actions.act_window_close'}
