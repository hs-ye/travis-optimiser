import json
# note json comma types matter when qualifying text, must be double quotes for json string
json.loads('{"0":["southern cross station", "luna park", "koko black",  "university of melbourne"]}')


json.loads('["southern cross station", "luna park", "koko black",  "university of melbourne"]')