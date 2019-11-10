### ==== Main file for GCP cloud functions deployment ==== ### 

# from flask import jsonify
from travis_optimiser.recommender import get_best_recs, get_gmaps
from utils.utilities import get_cfg


def run_recommender(request):
    # NOTE TESTING, static headers
    # headers = json.loads(request.headers.get('ids'))
    # print(headers)
    headers = request.args.get('ids', "ChIJdedaLk5d1moRQOX0CXZWBB0")
    cfg = get_cfg()
    gmaps = get_gmaps()
    headers = [
        "ChIJdedaLk5d1moRQOX0CXZWBB0",  # sthn cross
        "ChIJczgQh8lC1moR9r9gP44FRvY",  # chinatown
    ]    
    recs = get_best_recs(gmaps, headers, rectype='restaurant', cfg=cfg)
    return recs.to_json()