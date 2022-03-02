from odoo import api, fields, models, _

class MessageAlert(models.TransientModel):
    _name = 'message.alert'

    message = fields.Text('Message', readonly=True)

    @api.multi
    def action_ok(self):
        """ close wizard"""
        return {'type': 'ir.actions.act_window_close'}