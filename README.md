# Travis Optimiser

# Deployed via google cloud functions

Endpoint: (GET)
https://asia-east2-travis-mvp-v2.cloudfunctions.net/travis-recommender

To make a request:
attach requested google places id in a header, accepts either 1 or 2 headers in a list:
ids:["ChIJczgQh8lC1moR9r9gP44FRvY", "ChIJdedaLk5d1moRQOX0CXZWBB0"]

- These are Chinatown and Southern Cross respectively, so search should return shops in the middle

Response format (json):
{"33":"ChIJ9RT5wLRC1moRpIkhaxraJMc","37":"ChIJcxVwKrVC1moRcHnRJ0dR5vM"}

- responses generally should be list of 5, unless places cannot be found
- to check a id, use https://maps.googleapis.com/maps/api/place/details/json?key=<>&place_id=<>
    - key=<> add your gmaps api key
    - place_id=<> insert the id that was returned


Curl test (status test):
curl -X GET -k -H 'ids: ["ChIJczgQh8lC1moR9r9gP44FRvY", "ChIJdedaLk5d1moRQOX0CXZWBB0"]' -i 'https://asia-east2-travis-mvp-v2.cloudfunctions.net/travis-recommender'

- Flat file location: Stored on a GCP Cloud Storage bucket, see config.yml (not published to github)

# To do list:
- Add google search for different types of establishments, in an area
- Add single radius search

- Add controller for search, that 
    - check if search is single radius or between two locations
    - makes sure there are 5 results, and saves any additional searches to the csv file

- Deploy to google cloud functions - DONE
    - Modify storage location to a GCP cloud storage filepath - DONE
    - Update IAM Authorisation

- Content based recommender that classifies restaurants by type
- Create a list of types of restaurants, for recommendation
- System that links to accounts
-