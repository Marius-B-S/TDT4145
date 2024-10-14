import sqlite3 as sql
import pandas as pd
import utilities as util

# Remember to change LoadValues to False afer the first run
removeVals = True


# \\ Brukstilfelle 1 //
print('\nBrukertilfelle 1\n')
###----- Start by insertin all standar values (Eks: Seter, Visninger, Ansatte, osv)-----###

conn = sql.connect('TrondelagTeater.db')
cur = conn.cursor()

# with open("TeaterDB.sql") as file:
#     sql_script = file.read()
# cur.executescript(sql_script)
if removeVals is True:
    print('remove tabels')
    util.removeAllTabels('TrondelagTeater.db')
    print('Insering values')
    with open("PreVals.sql") as file:
        sql_script = file.read()
    cur.executescript(sql_script)
else:
    print('keep tabels')


cur.close()
conn.close()



###-----------------------###
# \\ Brukstilfelle 2 //
print('\nBrukertilfelle 2\n')
# Read the file for hovedscenen and returns a text string (and the assigned date) 
# wich will be uesed to assigne the tickets
dato, HoverdsceneSeeting = util.readHovedscene('hovedscenen.txt')


# Using the new stirng and date we assigne tickets to a Ticket 
# purches for a standar user in the system
util.assignSeeting(dato, HoverdsceneSeeting, 'TrondelagTeater.db')

# Reads the file for gamle-scene.txt and assign seets to the
# assigned places on the theater map
util.readGamleScene(file='gamle-scene.txt', database='TrondelagTeater.db', ShowTitle='Størst av alt er kjærligheten')

# \\ Brukstilfelle 3 //
print('\nBrukertilfelle 3\n')
### --- Eksempel på hvordan en lager en ny bruker
util.createUser('Per Arne', '40080276', 'Gløshaugen', 'TrondelagTeater.db')
conn = sql.connect('TrondelagTeater.db')
# Henter BrukerID fra den nyeste genererte brukeren
cur = conn.cursor()
cur.execute("SELECT BrukerID FROM Bruker")
UserID = (cur.fetchall()[-1])[0]
cur.close()
conn.close()

# Her skulle den skulle util.PurchaseTickets kjøre og kjøpe 9 ordinære billetter
# til Størst av alt er kjærligheten den 3. februar. Denne funksjonen endte tilslutt
# og ikke virke som ønsket. Den er dermed ikke med i kjøringen, men ligger under 
# utilities.py med alle andre funksjoner
###-----------------------------
# util.PurchaseTickets(UserID, 'Ordinær', 9, 'Størst av alt er kjærligheten', '2024-02-03', 'TrondelagTeater.db')
###-----------------------------

# \\ Brukstilfelle 4 //
print('\nBrukertilfelle 4\n')

util.getSoldSeets('2024-02-03', 'TrondelagTeater.db')

# \\ Brukstilfelle 5 //
print('\nBrukertilfelle 5\n')
conn = sql.connect('TrondelagTeater.db')
cur = conn.cursor()

### ----- Kommentert ut ligger den prefererte måten å utføre spørringen, men grunnet 
### ----- at ikke alle rader blir skrevet er heller en non-pandas funksjon brukt

# SkuespillerSpiller = pd.read_sql_query(f'''SELECT StykkeTittel, Skuespiller.Navn AS Skuespiller_Navn, RolleNavn AS Rolle_Navn 
#                                 FROM ((((Skuespiller
#                                 INNER JOIN Spiller ON Skuespiller.AnsattID=Spiller.AnsattID)
#                                 INNER JOIN Rolle ON Spiller.RolleID=Rolle.RolleID)
#                                 INNER JOIN RolleTilAkt ON Rolle.RolleID=RolleTilAkt.RolleID)
#                                 INNER JOIN Akt ON RolleTilAkt.AktNr=Akt.AktNr)
                                
#                                 ''', conn)

# print(SkuespillerSpiller)
print('\n')
for row in cur.execute(f'''SELECT StykkeTittel, Skuespiller.Navn AS Skuespiller_Navn, RolleNavn AS Rolle_Navn 
                                FROM ((((Skuespiller
                                INNER JOIN Spiller ON Skuespiller.AnsattID=Spiller.AnsattID)
                                INNER JOIN Rolle ON Spiller.RolleID=Rolle.RolleID)
                                INNER JOIN RolleTilAkt ON Rolle.RolleID=RolleTilAkt.RolleID)
                                INNER JOIN Akt ON RolleTilAkt.AktNr=Akt.AktNr)
                                
                                '''):
        print(row)

cur.close()
conn.close()

# \\ Brukstilfelle 6 //
print('\nBrukertilfelle 6\n')
conn = sql.connect('TrondelagTeater.db')
cur = conn.cursor()

BestSale = pd.read_sql_query(f'''SELECT Visning.StykkeTittel AS Stykke_Tittel, Visning.Dato, COUNT(BillettID) AS Solgte_Billetter 
                                    FROM VISNING
                                    INNER JOIN Billett USING(VisningsID)
                                    GROUP BY Visning.VisningsID
                                    ORDER BY Solgte_Billetter DESC
                                ''', conn)
print(BestSale)



cur.close()
conn.close()

# \\ Brukstilfelle 7 //
# Grunnet problemer med æ,ø og å i en .py fil 
# skapte dette store problemer rundt fremgjøring
# av navn med disse bokstavene