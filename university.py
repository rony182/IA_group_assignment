import time
import gzip
import json
import sqlite3
import ssl
import urllib.request

universities = [
    'https://zircon.datausa.io/api/data?University=484613:similar,484613,484613:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=150987:similar,150987,150987:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=104717:similar,104717,104717:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=433387:similar,433387,433387:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=232557:similar,232557,232557:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=193900:similar,193900,193900:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=132903:similar,132903,132903:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=228778:similar,228778,228778:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=228723:similar,228723,228723:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=204796:similar,204796,204796:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=123961:similar,123961,123961:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=134130:similar,134130,134130:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=104151:similar,104151,104151:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=154022:similar,154022,154022:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=170976:similar,170976,170976:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=174066:similar,174066,174066:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=236948:similar,236948,236948:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=135717:similar,135717,135717:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=133951:similar,133951,133951:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=214777:similar,214777,214777:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=145637:similar,145637,145637:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=240444:similar,240444,240444:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=110662:similar,110662,110662:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=134097:similar,134097,134097:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=138187:similar,138187,138187:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=110635:similar,110635,110635:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=190150:similar,190150,190150:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=171100:similar,171100,171100:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=137351:similar,137351,137351:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=186380:similar,186380,186380:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=151351:similar,151351,151351:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=163286:similar,163286,163286:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=228769:similar,228769,228769:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=125231:similar,125231,125231:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=163204:similar,163204,163204:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=132709:similar,132709,132709:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=243780:similar,243780,243780:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=139959:similar,139959,139959:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=449339:similar,449339,449339:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=164988:similar,164988,164988:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=110644:similar,110644,110644:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=104179:similar,104179,104179:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=110565:similar,110565,110565:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=183026:similar,183026,183026:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=201885:similar,201885,201885:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=215293:similar,215293,215293:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=110583:similar,110583,110583:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=260901:similar,260901,260901:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=110608:similar,110608,110608:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=131469:similar,131469,131469:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=225511:similar,225511,225511:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=204857:similar,204857,204857:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=199120:similar,199120,199120:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=232186:similar,232186,232186:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=110653:similar,110653,110653:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=216339:similar,216339,216339:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=215062:similar,215062,215062:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=110680:similar,110680,110680:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=227216:similar,227216,227216:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=122409:similar,122409,122409:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=147767:similar,147767,147767:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=178396:similar,178396,178396:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=199193:similar,199193,199193:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=218663:similar,218663,218663:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=187532:similar,187532,187532:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=122755:similar,122755,122755:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=100751:similar,100751,100751:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=129020:similar,129020,129020:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=233921:similar,233921,233921:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=162928:similar,162928,162928:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=196088:similar,196088,196088:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=166629:similar,166629,166629:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=153658:similar,153658,153658:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=230764:similar,230764,230764:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=413413:similar,413413,413413:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=166027:similar,166027,166027:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=227182:similar,227182,227182:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=126614:similar,126614,126614:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=153603:similar,153603,153603:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=228459:similar,228459,228459:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=230038:similar,230038,230038:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=229115:similar,229115,229115:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=133702:similar,133702,133702:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=234030:similar,234030,234030:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=234076:similar,234076,234076:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=133669:similar,133669,133669:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=139940:similar,139940,139940:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=232946:similar,232946,232946:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=105330:similar,105330,105330:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=151111:similar,151111,151111:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=122597:similar,122597,122597:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=196097:similar,196097,196097:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=145600:similar,145600,145600:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=242422:similar,242422,242422:parents&measures=Median%20Average%20Net%20Price%20Grant%20Or%20Scholarship%20Aid',
    'https://zircon.datausa.io/api/data?University=236939:similar,236939,236939:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=126818:similar,126818,126818:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=221759:similar,221759,221759:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=190415:similar,190415,190415:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=228547:similar,228547,228547:parents&measures=State%20Tuition',
    'https://zircon.datausa.io/api/data?University=450933:similar,450933,450933:parents&measures=State%20Tuition'
]

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('tuition.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Universities
    (id INTEGER PRIMARY KEY AUTOINCREMENT, id_university TEXT, year TEXT, name TEXT,
     tuition TEXT)''')

count_records = 0
count_universities = 0
for university in universities:
    conn.commit()

    url = university
    print("Retrieving", url)
    count_universities = count_universities + 1

    text = "None"
    try:
        # Open with a timeout of 30 seconds
        document = urllib.request.urlopen(url, None, 30, context=ctx)
        if document.getcode() != 200:
            print("Error code=", document.getcode(), url)
            break
        if document.info().get('Content-Encoding') == 'gzip':
            # Decompress the gzip-encoded content
            content = gzip.decompress(document.read())
        else:
            content = document.read()
        text = content.decode()
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    except Exception as e:
        print("Unable to retrieve or parse page", url)
        print("Error", e)
        fail = fail + 1
        if fail > 5:
            break
        continue

    print(url, len(text))

    try:
        # Parse the JSON data
        data = json.loads(text)
        if 'data' in data:
            print("Data found in the response")
            for entry in data['data']:
                id_year = entry.get('ID Year', None)
                year = entry.get('Year', None)
                state_tuition = entry.get('State Tuition', None)
                university = entry.get('University', None)
                id_university = entry.get('ID University', None)
                # Insert the data into the database
                cur.execute('''INSERT OR IGNORE INTO Universities
                            (id_university, year, name, tuition)
                            VALUES (?, ?, ?, ?)''',
                            (id_university, year, university, state_tuition))
                count_records = count_records + 1
    except Exception as e:
        print("Failed to parse or insert data:", e)

print("Done. ", count_universities, "universities processed.")
print("Done. ", count_records, "records added to the database.")

cur.close()
