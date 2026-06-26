import pytest

@pytest.mark.asyncio
async def test_create_contract(auth_client):
    response = await auth_client.post(
        "/contracts",
        json={
            "company": "Vodafone",
            "company_address": "Musterstraße 1, 10115 Berlin, Deutschland",
            "contract_type": "Internet",
            "monthly_price": 69.9,
            "end_date": "2027-01-01",
            "notice_period_months": 3
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["company"] == "Vodafone"
    assert data["contract_type"] == "Internet"
    
@pytest.mark.asyncio
async def test_update_contract(auth_client):
    response1 = await auth_client.post(
        "/contracts",
        json={
            "company": "Vodafone",
            "company_address": "Musterstraße 1, 10115 Berlin, Deutschland",
            "contract_type": "Internet",
            "monthly_price": 69.9,
            "end_date": "2027-01-01",
            "notice_period_months": 3
        }
    )

    assert response1.status_code == 201

    contract_id = response1.json()["id"]

    response2 = await auth_client.patch(
        f"/contracts/{contract_id}",
        json={
            "company": "Test",
            "company_address": "Musterstraße 1, 10115 Berlin, Deutschland",
            "contract_type": "test2",
            "monthly_price": 69.9,
            "end_date": "2027-01-01",
            "notice_period_months": 1
        }
    )
    
    data = response2.json()

    assert response2.status_code == 200
    
    assert data["company"] == "Test"
    assert data["contract_type"] == "test2"
    
@pytest.mark.asyncio
async def test_delete_contract(auth_client):
    response1 = await auth_client.post(
        "/contracts",
        json={
            "company": "Vodafone",
            "company_address": "Musterstraße 1, 10115 Berlin, Deutschland",
            "contract_type": "Internet",
            "monthly_price": 69.9,
            "end_date": "2027-01-01",
            "notice_period_months": 3
        }
    )

    assert response1.status_code == 201
    
    contract_id = response1.json()["id"]
    
    response2 = await auth_client.delete(
        f"/contracts/{contract_id}"
    )
    
    assert response2.status_code == 200
    
@pytest.mark.asyncio
async def test_all_contracts(auth_client):
    response = await auth_client.get(
        "/contracts"
    )
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_expiring_contracts(auth_client):
    response = await auth_client.get(
        "/contracts/expiring"
    )
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    
@pytest.mark.asyncio
async def test_get_contract_pdf(auth_client):
    response1 = await auth_client.post(
        "/contracts",
        json={
            "company": "Vodafone",
            "company_address": "Musterstraße 1, 10115 Berlin, Deutschland",
            "contract_type": "Internet",
            "monthly_price": 69.9,
            "end_date": "2027-01-01",
            "notice_period_months": 3
        }    
    )
    
    assert response1.status_code == 201
    
    contract_id = response1.json()["id"]
    
    response2 = await auth_client.get(
        f"/contracts/{contract_id}/pdf"
    )
    
    assert response2.status_code == 200
    assert response2.headers["content-type"] == "application/pdf"
    assert len(response2.content) > 0
    
@pytest.mark.asyncio
async def test_create_contract_missing_company(auth_client):
    response = await auth_client.post("/contracts", json={
        "contract_type": "Internet",
        "monthly_price": 10,
        "end_date": "2027-01-01",
        "notice_period_months": 3
    })

    assert response.status_code == 422
    
@pytest.mark.asyncio
async def test_create_contract_negative_price(auth_client):
    response = await auth_client.post("/contracts", json={
        "company": "Vodafone",
        "company_address": "Musterstraße 1, 10115 Berlin, Deutschland",
        "contract_type": "Internet",
        "monthly_price": -10,
        "end_date": "2027-01-01",
        "notice_period_months": 3
    })

    assert response.status_code == 422
    
@pytest.mark.asyncio
async def test_create_contract_past_end_date(auth_client):
    response = await auth_client.post("/contracts", json={
        "company": "Vodafone",
        "company_address": "Musterstraße 1, 10115 Berlin, Deutschland",
        "contract_type": "Internet",
        "monthly_price": 10,
        "end_date": "2020-01-01",
        "notice_period_months": 3
    })

    assert response.status_code in (400, 422)
    
@pytest.mark.asyncio
async def test_update_nonexistent_contract(auth_client):
    response = await auth_client.patch("/contracts/999999", json={
        "company": "New"
    })

    assert response.status_code == 404
    
@pytest.mark.asyncio
async def test_delete_nonexistent_contract(auth_client):
    response = await auth_client.delete("/contracts/999999")

    assert response.status_code == 404
    
@pytest.mark.asyncio
async def test_contract_pagination(auth_client):
    for i in range(10):
        await auth_client.post("/contracts", json={
            "company": f"Vodafone{i}",
            "company_address": "Musterstraße 1, 10115 Berlin, Deutschland",
            "contract_type": "Internet",
            "monthly_price": 10,
            "end_date": "2027-01-01",
            "notice_period_months": 3
        })

    r = await auth_client.get("/contracts?limit=2&offset=0")

    assert r.status_code == 200
    assert len(r.json()) == 2
    
@pytest.mark.asyncio
async def test_expiring_contracts_empty(auth_client):
    r = await auth_client.get("/contracts/expiring?days=1")
    assert r.status_code == 200
    
@pytest.mark.asyncio
async def test_pdf_invalid_contract(auth_client):
    r = await auth_client.get("/contracts/999999/pdf")
    assert r.status_code == 404
    
@pytest.mark.asyncio
async def test_pdf_headers(auth_client):
    r1 = await auth_client.post("/contracts", json={
        "company": "Vodafone",
        "company_address": "Musterstraße 1, 10115 Berlin, Deutschland",
        "contract_type": "Internet",
        "monthly_price": 10,
        "end_date": "2027-01-01",
        "notice_period_months": 3
    })
    
    cid = r1.json()["id"]

    r2 = await auth_client.get(f"/contracts/{cid}/pdf")

    assert r2.headers["content-type"] == "application/pdf"
    
@pytest.mark.asyncio
async def test_pdf_not_empty(auth_client):
    r1 = await auth_client.post("/contracts", json={
        "company": "Vodafone",
        "company_address": "Musterstraße 1, 10115 Berlin, Deutschland",
        "contract_type": "Internet",
        "monthly_price": 10,
        "end_date": "2027-01-01",
        "notice_period_months": 3
    })

    id = r1.json()["id"]
    print(r1.json())
    r2 = await auth_client.get(f"/contracts/{id}/pdf")

    assert len(r2.content) > 100
    
@pytest.mark.asyncio
async def test_no_auth_access(client):
    r = await client.get("/contracts")
    assert r.status_code in (401, 403)
    
@pytest.mark.asyncio
async def test_invalid_token(client):
    client.headers.update({"Authorization": "Bearer WRONG"})
    r = await client.get("/contracts")
    assert r.status_code in (401, 403)
    
@pytest.mark.asyncio
async def test_logout_invalidates_refresh(auth_client, refresh_token):
    await auth_client.post("/auth/logout", json={
        "refresh_token": refresh_token
    })

    r = await auth_client.post("/auth/refresh", json={
        "refresh_token": refresh_token
    })

    assert r.status_code in (401, 400)