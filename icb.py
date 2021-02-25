# import libraries
from selenium import webdriver
import json
import csv
import sys
import mysql.connector
from astropy.table import Table
from astropy.io import ascii
from oauth2client.service_account import ServiceAccountCredentials
import gspread

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="plootberg",
    database="statsdatabase"
)

mycursor = db.cursor(buffered=True)

#mycursor.execute("DROP TABLE IF EXISTS Player")
mycursor.execute("CREATE TABLE IF NOT EXISTS Player (playerName VARCHAR(60), number VARCHAR(3), team VARCHAR(50), gp int UNSIGNED, goals int UNSIGNED, assists int UNSIGNED, ppg int UNSIGNED, ppa int UNSIGNED, shg int UNSIGNED, sha int UNSIGNED, gwg int UNSIGNED, gwa int UNSIGNED, psg int UNSIGNED, eng int UNSIGNED, sog int UNSIGNED, pts int UNSIGNED, fantasyPts int UNSIGNED, playerID int PRIMARY KEY AUTO_INCREMENT)")
#mycursor.execute("CREATE TABLE IF NOT EXISTS Stats (playerName VARCHAR(60), games int UNSIGNED, goals int UNSIGNED, assists int UNSIGNED, ppg int UNSIGNED, ppa int UNSIGNED, shg int UNSIGNED, sha int UNSIGNED, gwg int UNSIGNED, gwa int UNSIGNED, psg int UNSIGNED, eng int UNSIGNED, sog int UNSIGNED, pts int UNSIGNED, fantasyPts int UNSIGNED)")
mycursor.execute("DESCRIBE Player")

sql = ""
val = ""

#scope = ['https://spreadsheets.google.com/feeds',
#         'https://www.googleapis.com/auth/drive']

#credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

#gc = gspread.authorize(credentials)

#sht = gc.open("icb summer '18")
#stats_wks = sht.get_worksheet(0)
#summary_wks = sht.get_worksheet(1)
# stats_wks.update_cell(1, 1, 'Foo')
# summary_wks.update_cell(1, 1, 'Foo')

print("Starting chromedriver")
driver = webdriver.Chrome('C:/Users/Matt/chromedriver.exe')

icb_pages = ['https://stats.sharksice.timetoscore.com/display-schedule.php?team=2610&season=42&tlev=0&tseq=0&league=1',
             'https://stats.sharksice.timetoscore.com/display-schedule.php?team=2708&season=42&tlev=0&tseq=0&league=1',
             'https://stats.sharksice.timetoscore.com/display-schedule?team=2965&season=42&league=1&stat_class=1',
             'https://stats.sharksice.timetoscore.com/display-schedule.php?team=4122&season=42&tlev=0&tseq=0&league=1'
            ]
data = {}
teams = {
    'Austin': ['Mickey Colombo', 'Dylan Viskochil', 'Jaron Nazaroff', 'Sean Dunbar', 'Jerred Oconnell', 'John Roth',
               'Codie Oconnell', 'Austin Gardiner'],
    'Schlink': ['William Robinson', 'Kevin Hutchins', 'Todd Myers', 'Andrew Germond', 'Jose Arias', 'Victor Cruz',
                'Jonathan Sebring', 'Steven Schlinkert'],
    'Markham': ['Steven Scott', 'Joseph Friesen', 'Kyle Skjerven', 'Martin Jensen Iii', 'Jay Marvin Marvin',
                'Jason Perrucci', 'Daniel Watson', 'Matthew Markham'],
    'Bobby': ['Eric King', 'Derek Truesdale', 'Albert Hong', 'Kevin Kalman', 'Michael Moore', 'Coryndon Coles Iv',
              'Briana Steadman', 'Robert Victorino'],
    'Grant': ['Cecile Nguyen', 'Jordan Dodge', 'Chinh Bui', 'Olli-Pekka Tossavainen', 'Adam Scianna', 'Raymond Bernal',
              'Darrin Ng', 'Grant Gardiner'],
    'Don': ['Tyler Jue', 'Gabe Villalovos', 'Gino Escalante', 'Thomas Dong', 'Antrico Forbes', 'William Jelavich',
            'Jerry Hsu', 'Don Labarbera'],
    'Dunn': ['Eric Sokol', 'Chris Rathjen', 'Rick Chaput', 'Zachary Piper', 'Michael Reed', 'Brian Miyakusu',
             'Yuri Macauley', 'Nickolas Dunn']
}

try:
    for page in icb_pages:
        url = page
        driver.get(url)
        skatersTable = driver.find_element_by_xpath("//center[3]/table/tbody")
        skaterRows = skatersTable.find_elements_by_xpath(".//tr")
        playersStats = {}
        for row in skaterRows:
            player = row.find_elements_by_xpath(".//td")
            if len(player) == 15:
                name = player[0].text
                number = player[1].text
                gp = int(player[2].text)
                goals = int(player[3].text)
                assists = int(player[4].text)
                ppg = int(player[5].text)
                ppa = int(player[6].text)
                shg = int(player[7].text)
                sha = int(player[8].text)
                gwg = int(player[9].text)
                gwa = int(player[10].text)
                psg = int(player[11].text)
                eng = int(player[12].text)
                sog = int(player[13].text)
                pts = int(player[14].text)
                fantasy_pts = (goals*4) + (assists*2) + (ppg*2) + (ppa*1) + (shg*2) + (sha*1) + (gwg*2) + (gwa*1)\
                    + (psg*2) + (eng*2) + (sog*2)
                team = ''
                for t in teams:
                    if name in teams['Austin']:
                        team = 'Austin'
                    elif name in teams['Schlink']:
                        team = 'Schlink'
                    elif name in teams['Markham']:
                        team = 'Markham'
                    elif name in teams['Bobby']:
                        team = 'Bobby'
                    elif name in teams['Grant']:
                        team = 'Grant'
                    elif name in teams['Don']:
                        team = 'Don'
                    elif name in teams['Dunn']:
                        team = 'Dunn'

                if name not in data:
                    data[name] = {}
                    data[name].update({
                        'name': name,
                        'number': number,
                        'gp': gp,
                        'goals': goals,
                        'assists': assists,
                        'ppg': ppg,
                        'ppa': ppa,
                        'shg': shg,
                        'sha': sha,
                        'gwg': gwg,
                        'gwa': gwa,
                        'psg': psg,
                        'eng': eng,
                        'sog': sog,
                        'pts': pts,
                        'fantasy_pts': fantasy_pts,
                        'team': team
                    })
                else:
                    person = data[name]
                    person['gp'] += gp
                    gp = person['gp']
                    person['goals'] += goals
                    goals = person['goals']
                    person['assists'] += assists
                    assists = person['assists']
                    person['ppg'] += ppg
                    ppg = person['ppg']
                    person['ppa'] += ppa
                    ppa = person['ppa']
                    person['shg'] += shg
                    shg = person['shg']
                    person['sha'] += sha
                    sha = person['sha']
                    person['gwg'] += gwg
                    gwg = person['gwg']
                    person['gwa'] += gwa
                    gwa = person['gwa']
                    person['psg'] += psg
                    psg = person['psg']
                    person['eng'] += eng
                    eng = person['eng']
                    person['sog'] += sog
                    sog = person['sog']
                    person['pts'] += pts
                    pts = person['pts']
                    person['fantasy_pts'] += fantasy_pts
                    fantasy_pts = person['fantasy_pts']
                
                #write to db, if row exists update the row, else insert row
                print("Inserting row")
                sql = "REPLACE INTO Player (playerName, number, team, gp, goals, assists, ppg, ppa, shg, sha, gwg, gwa, psg, eng, sog, pts, fantasyPts) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = name, number, team, gp, goals, assists, ppg, ppa, shg, sha, gwg, gwa, psg, eng, sog, pts, fantasy_pts
                mycursor.execute(sql, val)

                
    mycursor.execute("SELECT * FROM Player")
    #myresult = mycursor.fetchall()

    for x in mycursor:
        print(x)

    db.commit()

    # Add data to Google Sheet
    """
    cols = ['Name', 'Number', 'GP', 'Goals(2)', 'Assists(1)', 'PPG(1)', 'PPA(.5)', 'SHG(1)', 'SHA(.5)', 'GWG(1)', 'GWA(.5)',
            'PSG(1)', 'ENG(1)', 'SOG(1)', 'PTS', 'Fantasy Pts', 'Team']
    rows = []
    stats_wks.clear()
    stats_wks.append_row(cols)
    for key, v in data.items():
        row = [v['name'], v['number'], v['gp'], v['goals'], v['assists'], v['ppg'], v['ppa'], v['shg'], v['sha'],
            v['gwg'], v['gwa'], v['psg'], v['eng'], v['sog'], v['pts'], v['fantasy_pts'], v['team']]
        rows.append(row)
        strRow = ''.join(str(e) for e in row)
        stats_wks.append_row(row)
    t = Table(rows=rows, names=cols)
    print(t)
    ascii.write(t, 'icb.csv', format='csv', overwrite=True)
    """

    cols2 = ['Name', 'Number', 'GP', 'Goals(2)', 'Assists(1)', 'PPG(1)', 'PPA(.5)', 'SHG(1)', 'SHA(.5)', 'GWG(1)',
            'GWA(.5)', 'PSG(1)', 'ENG(1)', 'SOG(1)', 'PTS', 'Fantasy Pts']
    rows2 = []
    teamCols = ['Austin', 'Schlink', 'Markham', 'Bobby', 'Grant', 'Don', 'Dunn']
    blankRow = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    # summary_wks.clear()
    # summary_wks.append_row(['Summary:', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
    for i in range(len(teamCols)):
        teamRow = [teamCols[i], '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        teamPts = 0
        rows2.append(teamRow)
        rows2.append(cols2)
        # summary_wks.append_row(teamRow)
        # summary_wks.append_row(cols2)
        for key, v in data.items():
            if v['team'] == teamCols[i]:
                row = [v['name'], v['number'], v['gp'], v['goals'], v['assists'], v['ppg'], v['ppa'], v['shg'], v['sha'],
                    v['gwg'], v['gwa'], v['psg'], v['eng'], v['sog'], v['pts'], v['fantasy_pts']]
                rows2.append(row)
                # summary_wks.append_row(row)
                teamPts += v['fantasy_pts']
        totalPts = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Total:', teamPts]
        # summary_wks.append_row(totalPts)
        rows2.append(totalPts)

    tbl = Table(rows=rows2, names=blankRow)
    print(tbl)
    ascii.write(tbl, 'summary.csv', format='csv', overwrite=True)

    with open('icb.json', 'w') as outfile:
        json.dump(data, outfile)

except Exception as e:
    print(e)
    driver.quit()

print ("Closing chromedriver")
driver.quit()
sys.exit()
