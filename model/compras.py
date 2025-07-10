from odoo import models, fields, api


class ComprasState(models.Model):
    _inherit = "purchase.order"
    _description = "Estado de orden de compra"

    state = fields.Selection(
        selection_add=[
            ('parcial', 'Recepción Parcial'),
            ('recepcionado', 'Recepcionado'),
            ('devuelto', 'Devuelto'),  # opcional
        ]
    )

    def _compute_entrega_state(self):
        """Calcula y actualiza el estado de recepción según el estado de los pickings."""
        for order in self:
            group = self.env["procurement.group"].search([('name', '=', order.name)], limit=1)
            if not group:
                continue

            pickings = self.env["stock.picking"].search([('group_id', '=', group.id)])
            if not pickings:
                continue

            done_count = 0
            cancelled_count = 0
            partial = False

            for picking in pickings:
                if picking.state == 'done':
                    done_count += 1
                elif picking.state in ('assigned', 'confirmed', 'waiting'):
                    partial = True
                elif picking.state == 'cancel':
                    cancelled_count += 1

            # Lógica corregida fuera del bucle
            if cancelled_count == len(pickings):
                order.state = 'devuelto'
            elif done_count == len(pickings):
                order.state = 'recepcionado'
            elif done_count > 0 or partial:
                order.state = 'parcial'
            else:
                order.state = 'pendiente'



    def open_wizard_descuento (self):
        return {
            "type": "ir.actions.act_window",
            "name": "Descuento Global",
            "res_model": "wizard.descuento.compras",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_compra_id": self.id,
            },
        }









class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super().button_validate()
        if self.group_id:
            purchase_order = self.env['purchase.order'].search([('name', '=', self.group_id.name)], limit=1)
            if purchase_order:
                purchase_order._compute_entrega_state()
        return res

    def action_cancel(self):
        res = super().action_cancel()
        if self.group_id:
            purchase_order = self.env['purchase.order'].search([('name', '=', self.group_id.name)], limit=1)
            if purchase_order:
                purchase_order._compute_entrega_state()
        return res
