from unittest.mock import MagicMock
import pytest
import requests
from api.views import eventEndpoint
from rest_framework.test import APIRequestFactory
# Create your tests here.

@pytest.mark.django_db
def test_eventEndpoint_with_empty_response():
    mock_response = MagicMock()
    mock_response.json.return_value = []
    requests_get_mock = MagicMock(return_value=mock_response)

    with pytest.MonkeyPatch.context() as m:
        m.setattr("requests.get", requests_get_mock)

        request_factory = APIRequestFactory()
        request = request_factory.post('http://localhost:8000/events/', {'league': 'NFL', 'startDate': '2023-01-01', 'endDate': '2023-01-31'})

        response = eventEndpoint(request)

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_eventEndpoint_with_ConnectionError():
    requests_get_mock = MagicMock(side_effect=requests.ConnectionError("Failed to connect to API"))

    with pytest.MonkeyPatch.context() as m:
        m.setattr("requests.get", requests_get_mock)

        request_factory = APIRequestFactory()
        request = request_factory.post('http://localhost:8000/events/', {'league': 'NFL', 'startDate': '2023-01-01', 'endDate': '2023-01-31'})

        response = eventEndpoint(request)

    assert response.status_code == 503


@pytest.mark.django_db
def test_eventEndpoint_with_Exception():
    requests_get_mock = MagicMock(side_effect=Exception("Internal Error"))

    with pytest.MonkeyPatch.context() as m:
        m.setattr("requests.get", requests_get_mock)

        request_factory = APIRequestFactory()
        request = request_factory.post('http://localhost:8000/events/', {'league': 'NFL', 'startDate': '2023-01-01', 'endDate': '2023-01-31'})

        response = eventEndpoint(request)

    assert response.status_code == 500


@pytest.mark.django_db
def test_eventEndpoint_with_data_correct_param():
    mock_scoreboard_response = MagicMock()
    mock_scoreboard_response.json.return_value = [
       {
            'away': {'city': 'B', 'id': 'ae5132a4-e4b2-4bda-9933-b75c542b8d35', 'nickName': 'Team B'},
            'home': { 'city': 'A', 'id': '8da0c96d-7b3d-41f3-9e68-29607f3babcf', 'nickName': 'Team A'},
            'id': '5055c2a2-af68-4082-9834-ceb36dd0a807',
            'timestamp': '2023-01-11T14:00:00Z'
        },
        {
            'away': { 'city': 'A', 'id': '8da0c96d-7b3d-41f3-9e68-29607f3babcf', 'nickName': 'Team A'},
            'home': {'city': 'B', 'id': 'ae5132a4-e4b2-4bda-9933-b75c542b8d35', 'nickName': 'Team B'},
            'id': '5055c2a2-af68-4082-9834-ceb36dd0a807',
            'timestamp': '2023-02-11T18:00:00Z'
        },
    ]

    mock_team_rankings_response = MagicMock()
    mock_team_rankings_response.json.return_value =  [
        {'rank': 1, 'rankPoints': 100.3, 'teamId': 'ae5132a4-e4b2-4bda-9933-b75c542b8d35'},
        {'rank': 2, 'rankPoints': 90, 'teamId': '8da0c96d-7b3d-41f3-9e68-29607f3babcf'},
    ]

    with pytest.MonkeyPatch.context() as m:
        m.setattr("requests.get", MagicMock(side_effect=lambda url: mock_scoreboard_response
                                             if url == 'http://localhost:9000/NFL/scoreboard' else mock_team_rankings_response))       

        request_factory = APIRequestFactory()
        request = request_factory.post('http://localhost:8000/events/', {'league': 'NFL', 'startDate': '2023-01-01', 'endDate': '2023-01-31'})

        response = eventEndpoint(request)
    assert response.status_code == 200
    assert response.data == [
    {
        "eventId": "5055c2a2-af68-4082-9834-ceb36dd0a807",
        "eventDate": "2023-01-11",
        "eventTime": "14:00:00",
        "homeTeamId": "8da0c96d-7b3d-41f3-9e68-29607f3babcf",
        "homeTeamNickName": "Team A",
        "homeTeamCity": "A",
        "homeTeamRank": 2,
        "homeTeamRankPoints": 90,
        "awayTeamId": "ae5132a4-e4b2-4bda-9933-b75c542b8d35",
        "awayTeamNickName": "Team B",
        "awayTeamCity": "B",
        "awayTeamRank": 1,
        "awayTeamRankPoints": 100.3
    }]


@pytest.mark.django_db
def test_eventEndpoint_with_data_incorrect_date_param():
    mock_scoreboard_response = MagicMock()
    mock_scoreboard_response.json.return_value = [
       {
            'away': {'city': 'B', 'id': 'ae5132a4-e4b2-4bda-9933-b75c542b8d35', 'nickName': 'Team B'},
            'home': { 'city': 'A', 'id': '8da0c96d-7b3d-41f3-9e68-29607f3babcf', 'nickName': 'Team A'},
            'id': '5055c2a2-af68-4082-9834-ceb36dd0a807',
            'timestamp': '2023-01-11T14:00:00Z'
        },
    ]

    mock_team_rankings_response = MagicMock()
    mock_team_rankings_response.json.return_value =  [
        {'rank': 1, 'rankPoints': 100.3, 'teamId': 'ae5132a4-e4b2-4bda-9933-b75c542b8d35'},
        {'rank': 2, 'rankPoints': 90, 'teamId': '8da0c96d-7b3d-41f3-9e68-29607f3babcf'},
    ]

    with pytest.MonkeyPatch.context() as m:
        m.setattr("requests.get", MagicMock(side_effect=lambda url: mock_scoreboard_response
                                             if url == 'http://localhost:9000/NFL/scoreboard' else mock_team_rankings_response))       

        request_factory = APIRequestFactory()
        request = request_factory.post('http://localhost:8000/events/', {'league': 'NFL', 'startDate': '2023-03-15', 'endDate': '2023-01-31'})

        response = eventEndpoint(request)
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_eventEndpoint_with_data_incorrect_league_param():
    mock_scoreboard_response = MagicMock()
    mock_scoreboard_response.json.return_value = [
       {
            'away': {'city': 'B', 'id': 'ae5132a4-e4b2-4bda-9933-b75c542b8d35', 'nickName': 'Team B'},
            'home': { 'city': 'A', 'id': '8da0c96d-7b3d-41f3-9e68-29607f3babcf', 'nickName': 'Team A'},
            'id': '5055c2a2-af68-4082-9834-ceb36dd0a807',
            'timestamp': '2023-01-11T14:00:00Z'
        },
    ]

    mock_team_rankings_response = MagicMock()
    mock_team_rankings_response.json.return_value =  [
        {'rank': 1, 'rankPoints': 100.3, 'teamId': 'ae5132a4-e4b2-4bda-9933-b75c542b8d35'},
        {'rank': 2, 'rankPoints': 90, 'teamId': '8da0c96d-7b3d-41f3-9e68-29607f3babcf'},
    ]

    with pytest.MonkeyPatch.context() as m:
        m.setattr("requests.get", MagicMock(side_effect=lambda url: mock_scoreboard_response
                                             if url == 'http://localhost:9000/NFL/scoreboard' else mock_team_rankings_response))       

        request_factory = APIRequestFactory()
        request = request_factory.post('http://localhost:8000/events/', {'league': 'UEFA', 'startDate': '2023-01-01', 'endDate': '2023-01-31'})

        response = eventEndpoint(request)
    assert response.status_code == 200
    assert response.data == []