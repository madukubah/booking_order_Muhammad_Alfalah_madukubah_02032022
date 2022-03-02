from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_booking_order = fields.Boolean(string="Is Booking Order", default=True)
    service_team_id = fields.Many2one('service.team', string="Team", required=True)
    service_team_leader = fields.Many2one('res.users', string="Team Leader", required=True)
    service_team_members = fields.Many2many('res.users', 'sale_res_user_rel', 'sale_id', 'user_id', string="Members")
    booking_start = fields.Datetime(string="Booking Start", required=True)
    booking_end = fields.Datetime(string="Booking End", required=True)

    @api.onchange("service_team_id" )
    def onchange_service_team_id(self):
        for order in self:
            service_team = order.service_team_id
            # _logger.warning(team_id)
            if service_team : 
                order.service_team_leader = service_team.leader
                order.service_team_members = service_team.members

    @api.multi
    def action_check(self):
        for order in self:
            WorkOrder = self.env['work.order']  
            work_orders = WorkOrder.search([ ( 'state', 'not in', ['cancel', 'done'] ), ( 'service_team_id', '=', order.service_team_id.id ) ])
            if not len(work_orders) == 0 :
                raise UserError(_('Team already has work order during that period on  %s .')  % (work_orders.sale_order_id.name) )
            else :
                message_id = self.env['message.alert'].create({'message': _("Team is available for booking") })
                return {
                    'name': _('Successfull'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'message.alert',
                    # pass the id
                    'res_id': message_id.id,
                    'target': 'new'
                }

        return True
    
    @api.multi
    def action_confirm(self):
        for order in self:
            WorkOrder = self.env['work.order']  
            work_orders = WorkOrder.search([ ( 'state', 'not in', ['cancel', 'done'] ), ( 'service_team_id', '=', order.service_team_id.id ) ])
            if not len(work_orders) == 0 :
                raise UserError(_('Team is not available during this period, already booked on %s . Please book on another date .')  % (work_orders.sale_order_id.name) )

            result = super(SaleOrder, self).action_confirm()
            work_order = self.env['work.order'].create({
                'name': 'name',
                'sale_order_id': order.id,
                'service_team_id': order.service_team_id.id,
                'service_team_leader': order.service_team_leader.id,
                'planned_start': order.booking_start,
                'planned_end': order.booking_end
            })
            work_order.service_team_members = order.service_team_members
            return result

    @api.multi
    def action_view_work_order(self):
        WorkOrder = self.env['work.order']  
        work_orders = WorkOrder.search([( 'sale_order_id', '=', self.id ) ])
        return {
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'work.order',
                    # pass the id
                    'res_id': work_orders.ids[0],
                    # 'target': 'new'
                }
