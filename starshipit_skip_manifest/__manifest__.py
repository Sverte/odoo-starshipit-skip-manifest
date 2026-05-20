{
    "name": "starshipit_skip_manifest",
    "version": "19.0.1.0.0",
    "category": "Inventory/Delivery",
    "summary": "Prevents Odoo Starshipit integration from automatically manifesting orders",
    "author": "Community",
    "website": "https://github.com/",
    "depends": ["delivery_starshipit", "stock", "mail"],
    "data": [],
    "post_load": "post_load",
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "MIT"
}
