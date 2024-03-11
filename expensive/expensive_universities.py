import sqlite3

conn = sqlite3.connect('universities_tuition.sqlite')
cur = conn.cursor()

cur.execute('SELECT id, year FROM Years')
years = dict()
for message_row in cur :
    years[message_row[0]] = message_row[1]

# Query for top 10 most expensive universities
cur.execute("""
    SELECT Universities.id, Universities.university_name
    FROM Universities
    JOIN (
        SELECT university_id, AVG(tuition) as average_tuition
        FROM Tuition
        GROUP BY university_id
    ) Tuition ON Universities.id = Tuition.university_id
    ORDER BY Tuition.average_tuition DESC
    LIMIT 10;
""")
universities = dict()
for message_row in cur :
    universities[message_row[0]] = message_row[1].replace("'", "\\'")  # Escape single quotes

cur.execute('SELECT id, university_id, year_id, tuition FROM Tuition')
tuitions = dict()
for message_row in cur :
    tuitions[message_row[0]] = (message_row[1],message_row[2],message_row[3])

print("Loaded tuitions=",len(tuitions),"years=",len(years),"universities=",len(universities))

counts = dict()
years_list = list()
university_list = list(universities.values())

for (tuition_id, tuition) in list(tuitions.items()):
    year = years[tuition[1]]
    university = universities.get(tuition[0])
    if university is None:
        continue
    if year not in years_list:
        years_list.append(year)
    key = (year, university)
    if tuition[2] is not None and key not in counts:
        counts[key] = float(tuition[2])

years_list.sort()

fhand = open('expensive/expensive_universities.js','w')
fhand.write("expensiveUniversities = [ ['Year'")
for university in university_list:
    fhand.write(",'"+university+"'")
fhand.write("]")

for year in years_list:
    fhand.write(",\n['"+year+"'")
    for university in university_list:
        key = (year, university)
        val = counts.get(key,0)
        fhand.write(","+str(val))
    fhand.write("]");

fhand.write("\n];\n")
fhand.close()

print("Output written to gline.js")
print("Open gline.htm to visualize the data")

conn.close()