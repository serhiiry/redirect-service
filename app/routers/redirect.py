import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from ..redirect_logic import perform_redirection

router = APIRouter()

with open("app/config.json", "r") as f:
    domain_pools = json.load(f)


@router.get("/redirect/{pool_id}/{path:path}")
def redirect(pool_id: str, path: str, request: Request):
    new_url, custom_headers, error = perform_redirection(
        pool_id, path, str(request.query_params), request.client.host, domain_pools
    )

    if error:
        raise HTTPException(status_code=404, detail=error)

    response = RedirectResponse(url=new_url)
    for header, value in custom_headers.items():
        response.headers[header] = value

    return response
