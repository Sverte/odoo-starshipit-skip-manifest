{
    "name": "Starshipit Skip Manifest",
    "version": "19.0.1.0.0",
    "category": "Inventory/Delivery",
    "summary": "Prevents Odoo Starshipit integration from automatically manifesting orders",
    "description": "Skips automatic Starshipit manifest requests and suppresses the related missing manifest PDF chatter warning.",
    "author": "Community",
    "website": "https://github.com/",
    "depends": ["delivery_starshipit", "stock", "mail"],
    "data": [],
    "post_load": "post_load",
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3"
}
