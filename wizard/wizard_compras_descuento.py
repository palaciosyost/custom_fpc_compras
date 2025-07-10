from odoo import models, api, fields, _

class WizardDescuento(models.TransientModel):
    _name = 'wizard.descuento.compras'
    _description = 'Wizard para aplicar descuento en orden de compra'

    orden_compra = fields.Many2one(
        "purchase.order",
        string="Orden de compra",
        default=lambda self: self._context.get("compra_id"),
        required=True
    )
    descuento = fields.Float(string="Descuento (%)", required=True)

    def confirm_descuento(self):
        self.ensure_one()
        for line in self.orden_compra.order_line:
            line.discount = self.descuento
