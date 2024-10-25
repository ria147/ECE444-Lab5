import pytest
from application import application

@pytest.fixture
def client():
    application.config["TESTING"] = True

    with application.app_context():
        
        yield application.test_client()  # tests run here


def test_model(client):
    headlines = [
        "UofT is the best university in Canada", 
        "Aliens discovered in Mars", 
        "TTC Line 1 is not working", 
        "Eating rice causes cancer"
        ]
    
    correct_predictions = ["REAL", "FAKE", "REAL", "FAKE"]

    for i in range(len(headlines)):
        headline = headlines[i].replace(' ', '+')
        response = client.get("/?query="+headline, follow_redirects=True)
        assert response.status_code == 200
        if correct_predictions[i] == "REAL":
            assert b"REAL" in response.data
        elif correct_predictions[i] == "FAKE":
            assert b"FAKE" in response.data