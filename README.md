# Odoo Starshipit Skip Manifest

> [!WARNING]
> I am not a Python developer and this module was created primarily from an operational understanding of Odoo and the Starshipit workflow, with assistance from AI tooling.
>
> The code works for our use case on Odoo Enterprise 19.0, but it should still be reviewed, tested and used at your own discretion before production deployment.

Small Odoo addon set for Odoo Enterprise's built-in Starshipit delivery integration.

The production addon prevents Odoo from automatically calling Starshipit's `orders/manifest` endpoint after shipment/label creation. Labels, tracking and normal shipment creation are left untouched.

It also suppresses the harmless chatter warning generated when Odoo tries to attach a manifest PDF after the manifest request has intentionally been skipped.

---

# Addons

## `starshipit_skip_manifest`

Production version.

### Features

- Blocks only `orders/manifest`
- Leaves other Starshipit API calls untouched
- Logs normal patch and skipped-manifest messages at `INFO`
- Suppresses the related missing manifest PDF chatter warning
- Keeps label generation, shipment creation and tracking retrieval intact

### Recommended use

Production environments.

---

## `starshipit_skip_manifest_debug`

Debug/staging version.

### Features

- Blocks only `orders/manifest`
- Logs every Starshipit endpoint seen by Odoo
- Logs failed Starshipit requests with traceback
- Suppresses the related missing manifest PDF chatter warning

### Recommended use

Staging or troubleshooting environments only.

Do not keep the debug addon enabled in production unless verbose Starshipit request logging is specifically required.

---

# Requirements

- Odoo Enterprise 19.0
- `delivery_starshipit`
- `stock`
- `mail`

---

# Installation

## Odoo.sh

1. Copy the selected addon folder into your custom addons repository.
2. Push to Odoo.sh.
3. Update the Apps list.
4. Install or upgrade the module.

## On-premise / self-hosted

1. Copy the addon folder into your custom addons path.
2. Restart Odoo.
3. Update the Apps list.
4. Install or upgrade the module.

---

# Important Notes

This module uses a `post_load` monkey patch because the Starshipit API wrapper is implemented as a plain service class rather than an Odoo model.

The module intentionally does **not** modify:

- Starshipit credentials
- Shipment creation
- Label generation
- Tracking retrieval
- Carrier configuration

It only intercepts:

```text
orders/manifest
```

and prevents Odoo from sending the shipment manifest to Starshipit automatically after validation.

---

# Why This Exists

By default, Odoo Enterprise's built-in Starshipit integration automatically manifests shipments immediately after validation.

For some operational workflows this is undesirable because:

- manifests may need to be sent later in bulk
- warehouse teams may validate shipments before final dispatch
- manifesting can trigger carrier charges or dispatch processes too early
- users may want Starshipit labels and tracking without immediate carrier manifest submission

This addon allows Odoo to:

- create shipments
- generate labels
- retrieve tracking
- attach labels to pickings

without automatically manifesting the shipment.

---

# Chatter Warning Suppression

Odoo's Enterprise Starshipit flow still attempts to retrieve a manifest PDF after calling `orders/manifest`.

Since this addon intentionally blocks that API call, no manifest PDF exists.

Without this patch, Odoo posts a harmless warning like:

```text
Error: ShippingDoc-starshipit-manifest-report-xxxxx.pdf file could not be obtained for order XXXXX
```

This addon suppresses only that specific chatter message.

---

# Logging

## Production addon

Logs only:

```text
Starshipit manifest request skipped.
```

at INFO level.

## Debug addon

Logs:

- every Starshipit endpoint seen by Odoo
- failed Starshipit API calls
- blocked manifest requests

Example:

```text
STARSHIPIT REQUEST SEEN. Endpoint: orders/import
STARSHIPIT MANIFEST API REQUEST BLOCKED.
```

---

# Compatibility

Tested with:

- Odoo Enterprise 19.0
- Built-in `delivery_starshipit` module

Other versions may require adjustments depending on internal Starshipit service implementation changes.

---

# License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
