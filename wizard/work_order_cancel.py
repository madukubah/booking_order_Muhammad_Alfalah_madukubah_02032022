from odoo import api, fields, models, _

class WorkOrderCancel(models.TransientModel):
    _name = 'work.order.cancel'

    note = fields.Text(string='Reason for Cancelation')
    work_order_id = fields.Many2one('work.order', string="Work Order", readonly=True)

    @api.multi
    def action_ok(self):
        """ close wizard"""
        self.work_order_id.note = self.note
        self.work_order_id.state = 'cancel'
        return {'type': 'ir.actions.act_window_close'}