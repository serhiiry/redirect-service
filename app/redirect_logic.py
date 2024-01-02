import json
import logging
import random
from datetime import datetime, UTC
from typing import Dict, Optional, Tuple

POOL_NOT_FOUND_MESSAGE = "Pool not found"
NO_DOMAINS_MESSAGE = "No domains available for redirection"

logger = logging.getLogger("redirect_service")
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def construct_log_data(pool_id: str, path: str, client_ip: str) -> Dict[str, str]:
    """
    Constructs a dictionary containing logging data.

    Args:
        pool_id (str): The ID of the domain pool.
        path (str): The requested path.
        client_ip (str): The IP address of the client.

    Returns:
        Dict[str, str]: A dictionary with the log data.
    """
    return {
        "pool_id": pool_id,
        "requested_path": path,
        "client_ip": client_ip,
        "datetime": datetime.now(UTC).isoformat(),
    }


def perform_redirection(
    pool_id: str,
    path: str,
    query_params: str,
    client_ip: str,
    domain_pools: Dict[str, Dict[str, any]]
) -> Tuple[Optional[str], Optional[Dict[str, str]], Optional[str]]:
    """
    Performs the redirection logic based on the provided domain pool configurations.

    Args:
        pool_id (str): The ID of the domain pool.
        path (str): The path of the request.
        query_params (str): The query parameters of the request.
        client_ip (str): The IP address of the client.
        domain_pools (Dict[str, Dict[str, any]]): A dictionary containing the domain pool configurations.

    Returns:
        Tuple[Optional[str], Optional[Dict[str, str]], Optional[str]]: A tuple containing the new URL, custom headers,
        and an error message (if any).
    """
    pool_config = domain_pools.get(pool_id)
    common_log_data = construct_log_data(pool_id, path, client_ip)

    if not pool_config:
        logger.error(
            json.dumps(
                {
                    **common_log_data,
                    "event": "error",
                    "error_message": POOL_NOT_FOUND_MESSAGE,
                }
            )
        )
        return None, None, POOL_NOT_FOUND_MESSAGE

    path_based_domains = pool_config.get("path_based_domains", {})
    for path_key, domains in path_based_domains.items():
        if path.startswith(path_key):
            selected_domains = domains
            break
    else:
        selected_domains = pool_config.get("domains", [])

    if not selected_domains:
        logger.error(
            json.dumps(
                {
                    **common_log_data,
                    "event": "error",
                    "error_message": NO_DOMAINS_MESSAGE,
                }
            )
        )
        return None, None, NO_DOMAINS_MESSAGE

    domain = random.choices(
        [domain for domain, weight in selected_domains],
        weights=[weight for domain, weight in selected_domains],
        k=1,
    )[0]

    new_url = f"https://{domain}/{path}"
    if query_params:
        new_url += f"?{query_params}"

    custom_headers = pool_config.get("custom_headers", {})

    logger.info(
        json.dumps(
            {
                **common_log_data,
                "event": "redirect",
                "redirected_to": new_url,
                "custom_headers": custom_headers,
            }
        )
    )

    return new_url, custom_headers, None
