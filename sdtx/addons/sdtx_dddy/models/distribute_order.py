# -*- coding: utf-8 -*-
import logging
from openerp import fields,models,api
from datetime import datetime
from openerp.tools.translate import _
import string

date_ref = datetime.now().strftime('%Y-%m-%d')
_logger = logging.getLogger(__name__)

class distribute_order(models.Model):
    """
    This wizard will confirm the all the selected draft invoices
    """
    _name = "distribute.order"
    _description = "distribute.order"

    start = fields.Char('Express Start', required=True)
    end = fields.Char('Express End')
    express_id = fields.Many2one('sdtx.express', string='Express', required=True, select=True, track_visibility='onchange')

    @api.multi
    def distribute_order(self):
        if self.env.context is None:
            self.env.context = {}
        active_ids = self.env.context.get('active_ids', []) or []
        if self.start is None:
            start = 0
        else:
            start = string.atoi(self.start, 10)
        if self.end is None:
            end = 0
        else:
            end = string.atoi(self.start, 10)
        proxy = self.pool['sdtx.dddy'].browse(self.env.cr,self.env.uid,active_ids,context=None)
        for record in proxy:
            if start > 0 and end != 0 and start < end:
                record.update({'express': start, 'express_id': self.express_id})
            elif start > 0:
                record.update({'express': start, 'express_id': self.express_id})
            start = start +1
        return {'type': 'ir.actions.act_window_close'}
