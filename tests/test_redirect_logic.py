from datetime import datetime, timezone
import pytest

from app.redirect_logic import (
    construct_log_data,
    perform_redirection,
    POOL_NOT_FOUND_MESSAGE,
)

HTTPS_PREFIX = "https://"
HOST_IP_ADDRESS = "127.0.0.1"
CUSTOM_HEADER = "X-Custom-Header"
DOMAIN_A = "domain-a.xyz"
DOMAIN_B = "domain-b.xyz"
DOMAIN_C = "domain-c.xyz"
DOMAIN_D = "domain-d.xyz"
DOMAIN_E = "domain-e.xyz"
DOMAIN_F = "domain-f.xyz"
DOMAIN_G = "domain-g.xyz"
DOMAIN_H = "domain-h.xyz"


domain_pools = {
    "pool1": {
        "domains": [[DOMAIN_A, 2], [DOMAIN_B, 1]],
        "path_based_domains": {
            "news/": [[DOMAIN_C, 2], [DOMAIN_D, 1]],
            "contact/": [[DOMAIN_E, 2], [DOMAIN_F, 1]],
        },
        "custom_headers": {CUSTOM_HEADER: "Value"},
    },
    "pool2": {"domains": [[DOMAIN_G, 2], [DOMAIN_H, 1]]},
}


def test_construct_log_data():
    log_data = construct_log_data("pool1", "path/", HOST_IP_ADDRESS)
    assert log_data["pool_id"] == "pool1"
    assert log_data["requested_path"] == "path/"
    assert log_data["client_ip"] == HOST_IP_ADDRESS

    log_time = datetime.fromisoformat(log_data["datetime"])
    current_time = datetime.now(timezone.utc)
    assert log_time.tzinfo is not None
    assert abs((current_time - log_time).total_seconds()) < 60


@pytest.mark.parametrize(
    "pool_id, path, expected_error, expected_url_starts, expected_header",
    [
        (
            "pool1",
            "news/article1",
            None,
            [f"{HTTPS_PREFIX}{DOMAIN_C}", f"{HTTPS_PREFIX}{DOMAIN_D}"],
            CUSTOM_HEADER,
        ),
        (
            "pool1",
            "contact/info",
            None,
            [f"{HTTPS_PREFIX}{DOMAIN_E}", f"{HTTPS_PREFIX}{DOMAIN_F}"],
            CUSTOM_HEADER,
        ),
        (
            "pool1",
            "other/path",
            None,
            [f"{HTTPS_PREFIX}{DOMAIN_A}", f"{HTTPS_PREFIX}{DOMAIN_B}"],
            CUSTOM_HEADER,
        ),
        (
            "pool2",
            "some/path",
            None,
            [f"{HTTPS_PREFIX}{DOMAIN_G}", f"{HTTPS_PREFIX}{DOMAIN_H}"],
            None,
        ),
        ("pool3", "news/article1", POOL_NOT_FOUND_MESSAGE, None, None),
    ],
)
def test_perform_redirection(
    pool_id, path, expected_error, expected_url_starts, expected_header
):
    url, headers, error = perform_redirection(
        pool_id, path, "", HOST_IP_ADDRESS, domain_pools
    )

    assert error == expected_error
    if expected_url_starts:
        assert any(url.startswith(start_url) for start_url in expected_url_starts)
    if expected_header:
        assert headers.get(expected_header) is not None
    else:
        assert not headers


def test_domain_weights():
    pool_id = "pool2"
    path = "some/path"
    query_params = ""
    client_ip = HOST_IP_ADDRESS

    domain_counts = {DOMAIN_G: 0, DOMAIN_H: 0}
    total_runs = 100000

    for _ in range(total_runs):
        url, _, _ = perform_redirection(
            pool_id, path, query_params, client_ip, domain_pools
        )
        if DOMAIN_G in url:
            domain_counts[DOMAIN_G] += 1
        elif DOMAIN_H in url:
            domain_counts[DOMAIN_H] += 1

    ratio = domain_counts[DOMAIN_G] / domain_counts[DOMAIN_H]
    assert 1.95 <= ratio <= 2.05
