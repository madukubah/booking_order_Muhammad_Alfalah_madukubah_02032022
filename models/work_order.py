from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime
import logging

class WorkOrder(models.Model):
    _name = "work.order"

    name = fields.Char(string="Name", readonly=True)
    sale_order_id = fields.Many2one('sale.order', string="Booking Order Reference", readonly=True)
    
    service_team_id = fields.Many2one('service.team', string="Team", required=True)
    service_team_leader = fields.Many2one('res.users', string="Team Leader", required=True)
    service_team_members = fields.Many2many('res.users', 'work_order_res_user_rel', 'work_order_id', 'user_id', string="Members")
    planned_start = fields.Datetime(string="Planned Start", required=True)
    planned_end = fields.Datetime(string="Planned End", required=True)

    start = fields.Datetime(string="Start", readonly=True)
    end = fields.Datetime(string="End", readonly=True)
    
    state = fields.Selection([
        ('pending', 'Pending'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='pending')

    note = fields.Text(string="Notes")
    
    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].next_by_code('work_order') or _('New')

        res = super(WorkOrder, self ).create(values)
        return res

    @api.multi
    def action_start(self):
        for order in self:
            order.start = datetime.datetime.now()
            order.state = 'progress'
    
    @api.multi
    def action_end(self):
        for order in self:
            order.end = datetime.datetime.now()
            order.state = 'done'
    
    @api.multi
    def action_reset(self):
        for order in self:
            order.start = ''
            order.end = ''
            order.state = 'pending'
    
    @api.multi
    def action_cancel(self):
        for order in self:
            cancel_id = self.env['work.order.cancel'].create(
                {
                    'note': '',
                    'work_order_id': order.id,
                })
            return {
                'name': _('Cancel'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'work.order.cancel',
                'res_id': cancel_id.id,
                'target': 'new'
            }
    
    @api.multi
    def action_print(self):
        return self.env['report'].get_action(self, 'booking_order.report_work_order')