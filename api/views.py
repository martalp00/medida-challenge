from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import EventsResponseSerializer
import requests
import datetime

# Create your views here.

@api_view(['POST'])
def eventEndpoint(request):
    try:
        # Get parameters
        params = request.data
        league = params.get('league')
        start_date_str = params.get('startDate')
        end_date_str = params.get('endDate')

        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None

        # First endpoint call
        scoreboard_response = requests.get('http://localhost:9000/NFL/scoreboard')
        scoreboard_data = scoreboard_response.json()

        # Second endpoint call
        team_rankings_response = requests.get('http://localhost:9000/NFL/team-rankings')
        team_rankings_data = team_rankings_response.json()
        #pdb.set_trace()
        # filter for the selected fields
        response_data = []

        for event in scoreboard_data:
            timestamp_str = event['timestamp']
            timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
            
            if event_matches_params(league, start_date, end_date, timestamp.date()):
                home_teamRank, home_teamRankPoints, away_teamRank, away_teamRankPoints = eventSearchRankPoints(event['home']['id'],event['away']['id'], team_rankings_data)

                event_data = {
                    'eventId' : event['id'],
                    'eventDate' : timestamp.date(),
                    'eventTime' : timestamp.time(),
                    'homeTeamId' : event['home']['id'],
                    'homeTeamNickName' : event['home']['nickName'],
                    'homeTeamCity' : event['home']['city'],
                    'homeTeamRank' : home_teamRank,
                    'homeTeamRankPoints' : home_teamRankPoints,
                    'awayTeamId' : event['away']['id'],
                    'awayTeamNickName' : event['away']['nickName'],
                    'awayTeamCity' : event['away']['city'],
                    'awayTeamRank' : away_teamRank,
                    'awayTeamRankPoints' :  away_teamRankPoints,
                }

                response_data.append(event_data)

        serializer = EventsResponseSerializer(data=response_data, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    except requests.ConnectionError as e:
        error_message = f"Failed to connect to API: {str(e)}"
        return Response({"error": error_message}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    except Exception as e:
        error_message = f"Internal Error: {str(e)}"
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def event_matches_params(league, start_date, end_date, event_date):
    # As the Third Party API mock does not filter, it is filetered here
    if league and 'NFL' != league:
        return False
    if start_date and event_date < start_date:
        return False
    if end_date and event_date > end_date:
        return False
    return True


def eventSearchRankPoints(home_teamId, away_teamId, team_rankings_data: list[str]):
    otherDataFound = False
    home_teamRank, home_teamRankPoints, away_teamRank, away_teamRankPoints = None, None, None, None
    for scores in team_rankings_data:
        if home_teamId == scores['teamId']:
            home_teamRank = scores['rank']
            home_teamRankPoints = scores['rankPoints']
            if otherDataFound: 
                return home_teamRank, home_teamRankPoints, away_teamRank, away_teamRankPoints
            else :
                otherDataFound = True
        elif away_teamId == scores['teamId']:
            away_teamRank = scores['rank'] 
            away_teamRankPoints = scores['rankPoints']
            if otherDataFound: 
                return home_teamRank, home_teamRankPoints, away_teamRank, away_teamRankPoints
            else :
                otherDataFound = True
    return home_teamRank, home_teamRankPoints, away_teamRank, away_teamRankPoints