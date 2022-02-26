from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class RoomCostAttribute(models.Model):
    _name = 'room.cost.attribute'
    _rec_name = 'room_type_id'

    hotel_id = fields.Many2one('hotel.management', required=True)
    room_type_id = fields.Many2one('hotel.room.type', required=True, domain="[('hotel_id','=',hotel_id)]")
    ordered_by = fields.Many2one('res.partner', string='Partner')
    rate_supplier = fields.Many2one('res.partner', required=True)
    date_from = fields.Date(required=True)
    period_lead_id = fields.Many2one('date.range', string='Period', )
    date_to = fields.Date(required=True)
    note = fields.Char()
    price_ids = fields.One2many('cost.per.person', 'room_type_id', required=True)
    # remove this only for db
    cost = fields.Integer()

    meal_plan = fields.Selection([
        ('Soft Al Inclusive', 'Soft Al Inclusive'),

        ('Half Board (HB)', 'Half Board (HB)'),
        ('Full Board (FB)', 'Full Board (FB)'),

    ], required=True)

    # ('Al Inclusive', 'Al Inclusive'),
    # ('Board (B)', 'Board (B)'),
    @api.constrains('date_to', 'date_from')
    def condition_on_date(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                if rec.date_from > rec.date_to:
                    raise ValidationError(_('date from must be less than date to'))

    @api.constrains('date_to', 'date_from')
    def condition_on_date_all_conditions(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                all_room_cost = self.env['room.cost.attribute'].search(
                    [('id','!=',rec.id),('hotel_id', '=', rec.hotel_id.id), ('room_type_id', '=', rec.room_type_id.id),
                     ('rate_supplier', '=', rec.rate_supplier.id),
                     ('meal_plan', '=', rec.meal_plan),
                     '|', '&', ('date_from', '<=', rec.date_from), ('date_to', '>=', rec.date_from),
                     '&', ('date_from', '<=', rec.date_to), ('date_from', '<=', rec.date_to), ])
                raise ValidationError(all_room_cost)
                for room in all_room_cost:
                    if rec.date_from > rec.date_to:
                        raise ValidationError(_('date from must be less than date to'))

    @api.onchange('period_lead_id')
    def get_period_lead_dates(self):
        for rec in self:
            rec.date_from = rec.period_lead_id.date_start
            rec.date_to = rec.period_lead_id.date_end


class CostPerPerson(models.Model):
    _name = 'cost.per.person'

    person_per_room = fields.Selection([
        ('1', 'Single'), ('2', 'Double'),
        ('3', 'Triple'), ('4', '4 Persons'),
        ('5', '5 Persons')], string="Occupancy", default='1')
    hotel_cost = fields.Integer("Room Cost")
    guest_price = fields.Integer("Selling Price")
    room_type_id = fields.Many2one('room.cost.attribute')
