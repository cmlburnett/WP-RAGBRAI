# Transforms RAGBRAI route data into other formats
# Written and tested with Python 3.3
# 
# By Colin ML Burnett
# July 19, 2015

import re, sys

if len(sys.argv) != 2:
	print("Must provide a file name to process")
	sys.exit(-1)

# File name to process
fname = sys.argv[1]

# Open file and read all data
lines = open(fname, 'r').readlines()


# Map year to 2-tuple of distance & cities in that year
by_year = {}
# Map city 2-tuple to a list of years
by_city = {}

# Split each line of wiki markup
#     |-
#     | 1994 || 511 || [[Council Bluffs, Iowa|Council Bluffs]] || [[Harlan, Iowa|Harlan]] || [[Carroll, Iowa|Carroll]] || [[Perry, Iowa|Perry]] || [[Marshalltown, Iowa|Marshalltown]] || [[Marion, Iowa|Marion]] || [[Maquoketa, Iowa|Maquoketa]] || [[Clinton, Iowa|Clinton]]
# Then break each city up based on if it's [[foo]] or [[foo|bar]] into ('foo',None) or ('foo','bar'), respectively
years = {}
for line in lines:
	line = line.strip()

	# Ignore empty lines
	if not line: continue
	# Ignore row-start lines
	if line.startswith('|-'): continue

	# No need for leading pipe on row data
	line = line.strip('|').strip()

	# Split on cell delimeter ||
	res = [p.strip() for p in re.split('(\|\|)', line) if p!='||']
	# Year, distance travelled on the route, and cities visited in that year
	year = res[0]
	distance = res[1]
	_cities = res[2:]

	# Iterate through each city and map year to that city
	cities = []
	for city in _cities:
		parts = re.match('\[\[([^|]+)(\|([^\]]+))?\]\]', city)

		# [[wname|dname]]
		# wname = wiki article name
		# dname = display name
		wname = parts.group(1)
		dname = parts.group(3)

		# If no display name, then mark that with a None
		if dname == None:
			cities.append( (wname.strip(), None) )
		else:
			cities.append( (wname.strip(), dname.strip()) )

	# Index by year
	by_year[year] = (distance, cities)

	# Map each city to the year(s)
	for city in cities:
		if city not in by_city:
			by_city[city] = []

		by_city[city].append(year)


# Iterate through cities in order so that index by cnt will already be sorted
cities = list(by_city.keys())
cities.sort()

# Index cities by the number of visits to that city
by_cnt = {}
for city in cities:
	cnt = len(by_city[city])

	if cnt not in by_cnt:
		by_cnt[cnt] = []

	by_cnt[cnt].append(city)

# Now iterate through counts from highest to lowest
cnts = list(by_cnt.keys())
cnts.sort()
cnts.reverse()

# Spit out tables based on # of visits to each city
print("==By visitation frequency==")
for cnt in cnts:
	cities = by_cnt[cnt]

	if cnt == 1:
		print("===%d Time===" % cnt)
		print('{| class="wikitable"')
		print('|-')
		print('! City !! Year')
		for city in cities:
			print('|-')
			if city[1] == None:
				print('| [[%s]] || %s' % (city[0], ", ".join(by_city[city])))
			else:
				print('| [[%s|%s]] || %s' % (city[0], city[1], ", ".join(by_city[city])))

	else:
		print("===%d Times===" % cnt)
		print('{| class="wikitable"')
		print('|-')
		print('! City !! First Year !! Most Recent Year !! Years')
		for city in cities:
			print('|-')
			if city[1] == None:
				print('| [[%s]] || %s || %s || %s' % (city[0], min(by_city[city]), max(by_city[city]), ", ".join(by_city[city])))
			else:
				print('| [[%s|%s]] || %s || %s || %s' % (city[0], city[1], min(by_city[city]), max(by_city[city]), ", ".join(by_city[city])))

	print("|}")
	print("")

# Spit out table based on city name
print("==By city==")
print('{| class="wikitable sortable"')
print('|-')
print('! City !! # of Visits !! First Year !! Most Recent Year !! Years')

cities = list(by_city.keys())
cities.sort()

for city in cities:
	print('|-')
	
	if city[1] == None:
		print('| [[%s]] || %d || %s || %s || %s' % (city[0], len(by_city[city]), min(by_city[city]), max(by_city[city]), ", ".join(by_city[city])))
	else:
		print('| [[%s|%s]] || %d || %s || %s || %s' % (city[0], city[1], len(by_city[city]), min(by_city[city]), max(by_city[city]), ", ".join(by_city[city])))

print("|}")

