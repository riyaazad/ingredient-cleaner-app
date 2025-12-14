import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

#test for regular inputs (at least 10)
test_inputs = [
    ("Phenoxyehtanol", "phenoxyethanol"),
    ("Niacinimide", "niacinamide"),
    ("Vitamin B-3", "niacinamide"),
    ("Sodum Hyaluronate", "hyaluronic acid"),
    ("Butyrospermum Parkii Butter", "shea butter"),
    ("Cocamidopropyl betaine", "cocamidopropyl betaine"),
    ("Ethylhexyl Methoxycinnamate", "ethylhexyl methoxycinnamate"),
    ("Tocopherol", "tocopherol"),
    ("Aloe barbadensis leaf jucie", "aloe vera leaf juice"),
    ("CI 19140", "ci 19140")
]

#test for inputs that should not be merged
do_not_merge = [
    ("Sodium Chloride", "Sodium Chlorite"),
    ("Chloride", "Chlorite")
]


@pytest.mark.parametrize("raw,expected_inci", test_inputs)
def test_normalize(raw, expected_inci):
    response = client.post("/v1/ingredient/normalize", json={"raw": raw})
    assert response.status_code == 200
    data = response.json()
    assert data["normalized_inci"] == expected_inci

@pytest.mark.parametrize("raw1,raw2", do_not_merge)
def test_do_not_merge(raw1, raw2):
    resp1 = client.post("/v1/ingredient/normalize", json={"raw": raw1}).json()
    resp2 = client.post("/v1/ingredient/normalize", json={"raw": raw2}).json()
    # They should NOT map to the same normalized_inci
    assert resp1["normalized_inci"] != resp2["normalized_inci"]
