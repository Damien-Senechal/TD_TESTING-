def test_get_invoice_by_id():
    response = client.get('/api/invoices/1')
    assert response.status_code == 200
    assert response.json["reference"] == "FAC20240201"
