from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

class ServiceTeam(models.Model):
    _name = "service.team"

    name = fields.Char(string="Team Name")
    leader = fields.Many2one('res.users', string="Team Leader", required=True)
    members = fields.Many2many('res.users', 'service_team_res_user_rel', 'service_team_id', 'user_id', string="Members")