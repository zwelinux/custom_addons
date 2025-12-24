# stock_serial_hint/__manifest__.py
{
    "name": "Stock Serial Hint",
    "version": "17.0.1.0.0",
    "summary": "Show last used serial/lot and prefill first SN in Assign Serial Numbers wizard",
    "category": "Inventory",
    "author": "You",
    "license": "LGPL-3",
    "depends": ["stock"],   # mrp may also be relevant if you need produce flow
    "data": [
        "views/stock_assign_serial_view.xml",
    ],
    "installable": True,
    "application": False,
}
