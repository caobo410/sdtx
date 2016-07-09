# -*- coding: utf-8 -*-
import logging
from openerp import fields,models,api
from datetime import datetime
date_ref = datetime.now().strftime('%Y-%m-%d')
_logger = logging.getLogger(__name__)

class sdtx_express(models.Model):
    _name = "sdtx.express"
    _description = "sdtx.express"

    code = fields.Char(string='NO.', size=64, required=True, help="NO.")
    name = fields.Char(string='Express', size=64, required=True, help="Express")
    field = fields.Char(string='Express', size=64, help="Express")
    user_id = fields.Many2one('res.users', string='Opertor')
    date_confirm = fields.Date(string='Date', size=64, required=True, help="Date")

    _defaults = {
        'date_confirm': date_ref,
        'user_id': lambda cr, uid, id, c={}: id,
    }