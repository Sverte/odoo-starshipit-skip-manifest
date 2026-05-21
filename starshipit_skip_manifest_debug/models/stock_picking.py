import logging

from odoo import models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def message_post(self, *args, **kwargs):
        """
        Suppress only the chatter warning generated after this module skips
        Starshipit's manifest request.
        """
        body = kwargs.get("body")

        if body is None and args:
            body = args[0]

        body_text = str(body or "")

        is_missing_manifest_pdf_warning = (
            "file could not be obtained for order" in body_text
            and (
                "manifest-report" in body_text
                or "ShippingDoc-starshipit" in body_text
            )
        )

        if is_missing_manifest_pdf_warning:
            _logger.info(
                "Suppressed Starshipit missing manifest PDF chatter warning for picking(s): %s",
                ", ".join(self.mapped("name")),
            )
            return self.env["mail.message"]

        return super().message_post(*args, **kwargs)
