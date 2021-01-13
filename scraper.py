import sys
import requests
import json
import requests

def get_season(league_id, season_id, swid, espn_s2): 
  # Set up URL to the scoreboard page of ESPN FFL
  url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/{}/segments/0/leagues/{}?scoringPeriodId=2&view=mBoxscore&view=mMatchupScore&view=mRoster&view=mSettings&view=mStatus&view=mTeam&view=modular&view=mNav'.format(season_id, league_id)

  # Get response and parse into JSON
  r = requests.get(url, cookies={"swid": swid, "espn_s2": espn_s2})
  json_resp = json.loads(r.text)

  # Iterate through matchups 
  print ("Season: ", season_id)
  for iter, matchup in zip(range(len(json_resp['schedule'])), json_resp['schedule']):

    # Print week number and headers 
    if (iter % 5 == 0):
      if (iter / 5 == 13): 
        print ("\nPlayoff Round 1")
        print ("{:<10} {:<10} {:<10} {:<10} {:<10} {:<15} {:<10} {:<10} {:<10}".format("Matchup", "Away", "Away TD", "Home", "Home TD", "  ", "Away", "Home", "Change?")) 
      elif (iter / 5 == 14):
        print ("\nPlayoff Round 2")
        print ("{:<10} {:<10} {:<10} {:<10} {:<10} {:<15} {:<10} {:<10} {:<10}".format("Matchup", "Away", "Away TD", "Home", "Home TD", "  ", "Away", "Home", "Change?")) 
      else:
        print ("\nWeek ", int(iter / 5 + 1))
        print ("{:<10} {:<10} {:<10} {:<10} {:<10} {:<15} {:<10} {:<10} {:<10}".format("Matchup", "Away", "Away TD", "Home", "Home TD", "  ", "Away", "Home", "Change?")) 

    # Find home and away points from JSON data
    away_points = matchup['away']['totalPoints']
    home_points = matchup['home']['totalPoints']
    result = True if home_points > away_points else False 

    # Find home and away TDs from JSON data
    away_tds =  matchup['away']['cumulativeScore']['scoreByStat']['4']['score']
    home_tds = matchup['home']['cumulativeScore']['scoreByStat']['4']['score']

    # Calculated adjusted points using home and away TDs
    adj_away_points = away_points + away_tds * 2
    adj_home_points = home_points + home_tds * 2

    # Check if the result of the matchup changed
    new_result = True if adj_home_points > adj_away_points else False

    # Print in tabular format
    if (new_result != result): 
      print ("{:<10} {:<10} {:<10} {:<10} {:<10} {:<15} {:<10} {:<10} {:<10}".format(iter, round(away_points,2), int(away_tds),round(home_points, 2), int(home_tds), "AFTER ADJ", round(adj_away_points, 2),  round(adj_home_points,2), "CHANGE"))
    else:
      print ("{:<10} {:<10} {:<10} {:<10} {:<10} {:<15} {:<10} {:<10} {:<10}".format(iter, round(away_points,2), int(away_tds),round(home_points, 2), int(home_tds), "AFTER ADJ", round(adj_away_points, 2),  round(adj_home_points,2), "    "))

def main():

  # League Info
  league_id = 64277082
  season_id = [2019, 2020]

  # Cookies for auth
  swid = "8E5C85B4-8348-4287-B50E-2934FBF02237"
  espn_s2 = "AEAUz4TTMHN8PwK5TvznQcrJUMNsBAZ4Q6j92vjE57ZXItMqj1wB2PKbDtX2aqVlrs%2BLYoWrW6gfJ7q8kWbQ9eTg47nE3No7AbgUVsLv2wBEp8ihJx3PRQV7zKh81%2FJHUt%2FaR9%2F4Fb2s%2FN%2FvseQPVdU6azZQ4x2WwSHSazh9Y8C%2B9N8GUTbeGNFiWAPReJE63qZ6q1jnzmXcxTRjx4WM2SwAxUzNrtLWOyVTIlclpHL8q6Re5Iz%2Bh7ylJ3nKX0qE3vQCEAP7Mpvj8hLtVZ1XIftMmX%2BmMQZRbQrcZN7tx%2BDBXq%2F2B7f%2BWappTFEVPNCjGEA%3D"

  # Iterate through seasons
  for season in season_id:
    get_season(league_id, season, swid, espn_s2)

if __name__ == '__main__':
  main()
  sys.exit(0)