from travis_optimiser.recommender import rec_search_gmaps_at_latlon, rec_search_list_at_latlon, get_best_recs, get_gmaps, rec_from_list
# from travis_optimiser.recommender_data import get_df_loc
from travis_optimiser.recommender import get_df_loc
from utils import utilities

cfg = utilities.get_cfg()

def test_rec_from_list():
    # NOTE TESTING PASS
    # NOTE OLD - Deprecated, do not use
    id1 = "ChIJdedaLk5d1moRQOX0CXZWBB0"
    id2 = "ChIJczgQh8lC1moR9r9gP44FRvY"
    gmaps = get_gmaps()
    dfLoc = get_df_loc()
    rec_from_list(gmaps, id1, id2, dfLoc)

def test_search_gmap_at_latlon():
    # NOTE: Testing pass
    target_lat_lon = (-37.81493625, 144.96061525)
    # rectype = 'eat'
    gmaps = get_gmaps()
    # dfLoc = get_df_loc(method='local')
    rec_search_gmaps_at_latlon(gmaps, target_lat_lon, rectype='restaurant')

def test_search_list_at_latlon():
    # NOTE: Testing Pass
    target_lat_lon = (-37.81493625, 144.96061525)
    # rectype = 'eat'  # NOTE: Rectype different for built in vs gmaps
    dfLoc = get_df_loc()
    test_result = rec_search_list_at_latlon(dfLoc, target_lat_lon, rectype='eat')
    print(test_result)

def test_get_best_recs():
    # NOTE: TESTING
    gmaps = get_gmaps()
    rectype = 'restaurant'
    input_gpids = [
        "ChIJdedaLk5d1moRQOX0CXZWBB0",  # sthn cross
        "ChIJczgQh8lC1moR9r9gP44FRvY",  # chinatown
    ]
    cfg = utilities.get_cfg()
    test_result = get_best_recs(gmaps=gmaps, input_gpids=input_gpids, rectype=rectype,
                                cfg=cfg)
    print(test_result)

if __name__ == "__main__":
    # test_search_list_at_latlon()
    test_get_best_recs()