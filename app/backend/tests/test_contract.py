import pytest

@pytest.mark.asyncio
async def test_create_contract(auth_client):
    response = await auth_client.post(
        "/contracts",
        json={
            "company": "Vodafone",
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