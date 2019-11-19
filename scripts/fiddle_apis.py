zomato_api_key = "e42ab2b0198c6b200d691f83761e76c7"

# === Zomato ===
# curl command for categories
curl -X GET --header "Accept: application/json" --header "user-key: e42ab2b0198c6b200d691f83761e76c7" "https://developers.zomato.com/api/v2.1/categories"
# sample responses
# Delivery, Dine-out, Nightlife, Catching-up, Takeaway, Cafes, Daily, Menus, Breakfast, Lunch, Dinner, Pubs & Bars, Clubs & Lounges

# get 'establishments': sampe
# Café, Bakery, Casual Dining, Pub, Food Court, Bar, Fine Dining, Club, Brewery, Winery


# get cities
curl -X GET --header "Accept: application/json" --header "user-key: e42ab2b0198c6b200d691f83761e76c7" "https://developers.zomato.com/api/v2.1/cities?lat=-37.806&lon=144.95"
# each city has an unique ID (string/number)
{  "location_suggestions": [{
      "id": 259,
      
      "country_id": 14,
      "country_name": "Australia",
      "country_flag_url": "https://b.zmtcdn.com/images/countries/flags/country_14.png",
      "should_experiment_with": 0,
      "has_go_out_tab": 0,
      "discovery_enabled": 0,
      "has_new_ad_format": 1,
      "is_state": 0,
      "state_id": 132,
      "state_name": "Victoria",
      "state_code": "VIC"
    }]}

# get all cuisine:
curl -X GET --header "Accept: application/json" --header "user-key: e42ab2b0198c6b200d691f83761e76c7" "https://developers.zomato.com/api/v2.1/cuisines?city_id=280"
# sample in melbourne: Afghan, African, American, Arabian, Argentine, Asian, Asian Fusion, Australian, Austrian, BBQ, Bakery, Bangladeshi, Bar Food, Basque, Belgian, Beverages, Brazilian, British, Bubble Tea, Burger, Burmese, Cafe Food, Cambodian, Cantonese, Caribbean, Charcoal Chicken, Chinese, Coffee and Tea, Colombian, Contemporary, Continental, Creole, Crepes, Croatian, Danish, Deli, Desserts, Drinks Only, Dumplings, Dutch, Eastern European, Egyptian, Ethiopian, European, Falafel, Fast Food, Fijian, Filipino, Finger Food, Fish and Chips, French, Fried Chicken, Frozen Yogurt, Fusion, Georgian, German, Greek, Grill, Hawaiian, Healthy Food, Hot Pot, Hungarian, Ice Cream, Indian, Indonesian, International, Iranian, Iraqi, Irish, Israeli, Italian, Japanese, Japanese BBQ, Jewish, Juices, Kebab, Korean, Korean BBQ, Latin American, Lebanese, Malatang, Malaysian, Mauritian, Meat Pie, Mediterranean, Mexican, Middle Eastern, Modern Australian, Modern European, Mongolian, Moroccan, Nepalese, North Indian, Pacific, Pakistani, Pan Asian, Parma, Pastry, Patisserie, Peruvian, Pho, Pizza, Poké, Polish, Portuguese, Pub Food, Ramen, Roast, Russian, Salad, Sandwich, Scandinavian, Scottish, Seafood, Shanghai, Sichuan, Singaporean, Soul Food, South African, South Indian, Spanish, Sri Lankan, Steak, Street Food, Sushi, Swedish, Swiss, Syrian, Taiwanese, Tapas, Tea, Teppanyaki, Teriyaki, Tex-Mex, Thai, Tibetan, Turkish, Ukrainian, Uruguayan, Uyghur, Vegan, Vegetarian, Venezuelan, Vietnamese, Yum Cha

curl -X GET --header "Accept: application/json" --header "user-key: e42ab2b0198c6b200d691f83761e76c7" "https://developers.zomato.com/api/v2.1/geocode?lat=-37.806&lon=144.95"



# they found dodee paidang restaurant id: 18584637 image https://b.zmtcdn.com/data/pictures/7/18584637/ba831c6e6673272bb603eea11f5d7899.jpg
curl -H @{"user-key" = "e42ab2b0198c6b200d691f83761e76c7"} "https://developers.zomato.com/api/v2.1/geocode?lat=-37.806&lon=144.95"