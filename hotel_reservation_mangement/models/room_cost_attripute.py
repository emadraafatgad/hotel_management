from odoo import api , fields ,models


class RoomCostAttribute(models.Model):
    _name = 'room.cost.attribute'
    _rec_name = 'room_type_id'

    hotel_id = fields.Many2one('hotel.management',)
    room_type_id = fields.Many2one('hotel.room.type',domain="[('hotel_id','=',hotel_id)]")
    ordered_by = fields.Many2one('res.partner',string='Partner')
    rate_supplier = fields.Many2one('res.partner')
    date_from = fields.Date()
    period_lead_id = fields.Many2one('date.range',string='Period')
    date_to = fields.Date()
    note = fields.Char()
    price_ids = fields.One2many('cost.per.person','room_type_id')
    # remove this only for db
    cost = fields.Integer()

    meal_plan = fields.Selection([
        ('Soft Al Inclusive','Soft Al Inclusive'),
        ('Al Inclusive','Al Inclusive'),
        ('Half Board (HB)','Half Board (HB)'),
        ('Full Board (FB)', 'Full Board (FB)'),
        ('Board (B)', 'Board (B)'),
    ])

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
        ('5', '5 Persons')],string="Occupancy", default='1')
    hotel_cost = fields.Integer("Room Cost")
    guest_price = fields.Integer("Selling Price")
    room_type_id = fields.Many2one('room.cost.attribute')


