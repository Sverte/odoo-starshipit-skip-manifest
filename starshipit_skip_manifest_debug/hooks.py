import importlib
import inspect
import logging

_logger = logging.getLogger(__name__)


def post_load():
    """
    Debug patch for Starshipit's request method.

    Logs every Starshipit endpoint and blocks only orders/manifest.
    """
    try:
        service_module = importlib.import_module(
            "odoo.addons.delivery_starshipit.models.starshipit_service"
        )
    except Exception:
        _logger.exception(
            "Could not import delivery_starshipit.models.starshipit_service while applying skip-manifest debug patch."
        )
        return

    patched_classes = []

    for name, obj in inspect.getmembers(service_module, inspect.isclass):
        if getattr(obj, "__module__", "") != service_module.__name__:
            continue

        original_send_request = getattr(obj, "_send_request", None)

        if original_send_request is None:
            continue

        if getattr(original_send_request, "_skip_manifest_debug_patch", False):
            patched_classes.append(name)
            continue

        def _patched_send_request(self, endpoint, method="GET", data=None, params=None, route=None):
            endpoint_text = str(endpoint or "").strip().lower().strip("/")

            _logger.warning(
                "STARSHIPIT REQUEST SEEN. Endpoint: %s | Method: %s | Data: %s | Params: %s | Route: %s",
                endpoint,
                method,
                data,
                params,
                route,
            )

            if endpoint_text == "orders/manifest":
                _logger.warning(
                    "STARSHIPIT MANIFEST API REQUEST BLOCKED. Endpoint: %s | Method: %s | Data: %s | Params: %s",
                    endpoint,
                    method,
                    data,
                    params,
                )

                return {
                    "success": True,
                    "message": "Manifest skipped by custom Odoo module",
                    "errors": [],
                    "order_ids": (data or {}).get("order_ids", []),
                    "manifest": {
                        "success": True,
                        "manifest_id": "SKIPPED-BY-ODOO",
                    },
                }

            try:
                if route is None:
                    return original_send_request(
                        self,
                        endpoint,
                        method=method,
                        data=data,
                        params=params,
                    )

                return original_send_request(
                    self,
                    endpoint,
                    method=method,
                    data=data,
                    params=params,
                    route=route,
                )
            except Exception:
                _logger.exception(
                    "STARSHIPIT REQUEST FAILED. Endpoint: %s | Method: %s | Data: %s | Params: %s | Route: %s",
                    endpoint,
                    method,
                    data,
                    params,
                    route,
                )
                raise

        _patched_send_request._skip_manifest_debug_patch = True
        _patched_send_request._original_send_request = original_send_request

        setattr(obj, "_send_request", _patched_send_request)
        patched_classes.append(name)

    if patched_classes:
        _logger.warning(
            "Starshipit skip-manifest debug patch applied successfully to: %s",
            ", ".join(patched_classes),
        )
    else:
        _logger.error(
            "Could not apply Starshipit skip-manifest debug patch. No class with _send_request was found in %s.",
            service_module.__name__,
        )
