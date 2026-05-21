{
    "name": "Starshipit Skip Manifest Debug",
    "version": "19.0.1.0.0",
    "category": "Inventory/Delivery",
    "summary": "Debug version of Starshipit Skip Manifest with endpoint logging",
    "description": "Skips automatic Starshipit manifest requests, suppresses the related missing manifest PDF chatter warning, and logs all Starshipit endpoints seen by Odoo.",
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
