import sqlite3 as sql
import pandas as pd

def remove_table_data(database, tabell):
    try:
        conn = sql.connect(database)
        cur = conn.cursor()

        sql_query = f'DELETE FROM {tabell}'

        cur.execute(sql_query)
        conn.commit()
        print(f'Data removed from {tabell}')

    except sql.Error as e:
        print('Error oppsto:', e)

    finally:
        if conn:
            conn.close()

def removeAllTabels(database):
    remove_table_data(database, 'Sete')
    remove_table_data(database, 'Sal')
    remove_table_data(database, 'Stykke')
    remove_table_data(database, 'Akt')
    remove_table_data(database, 'Bruker')
    remove_table_data(database, 'Visning')
    remove_table_data(database, 'Billett')
    remove_table_data(database, 'BillettKjop')
    remove_table_data(database, 'Gruppe')
    remove_table_data(database, 'Pris')
    remove_table_data(database, 'Rolle')
    remove_table_data(database, 'RolleTilAkt')
    remove_table_data(database, 'Skuespiller')
    remove_table_data(database, 'AnnenAnsatt')
    remove_table_data(database, 'Spiller')
    remove_table_data(database, 'JobberPa')


def readHovedscene(file='hovedscenen.txt'):
    ParkSeeting = ''
    eria = ''
    GalleriSeeting = ''
    with open(file, 'r') as f:
        for line in f:
            if "Dato" in line:
                    words = line.split()
                    for word in words:
                        if len(word) == 10 and word[4] == "-" and word[7] == "-":
                            dato =  word
            elif 'Galleri' in line:
                eria = line
            elif 'Parkett' in line:
                eria = line
            elif 'Parkett' in eria:
                ParkSeeting = line[:-1] + ParkSeeting
            elif 'Galleri' in eria:
                GalleriSeeting +=  line[:-1] 

    HovedsceneSeating = ParkSeeting+ GalleriSeeting
    f.close()
    return dato, HovedsceneSeating

def assignSeeting(dato, HoverdsceneSeeting, database):
    conn = sql.connect(database)
    cur = conn.cursor()

    cur.execute("SELECT VisningsID FROM Visning WHERE Dato =? AND StykkeTittel =?", (dato,'Kongsemnene'))
    VisID = (cur.fetchall()[0])[0]

    cur.execute("SELECT KjopRef FROM BillettKjop")
    rowBK = (cur.fetchall())
    print(rowBK)
    if len(rowBK) == 0:
        latestRef = 1
        cur.execute(f'''INSERT INTO BillettKjop VALUES ({latestRef}, '2024-02-01', '14:15', 1)''')
    else:
        # latestRef = cur.fetchall()[-1]
        # latestRef = latestRef[0]
        latestRef = rowBK[-1][0]
        print(latestRef)
        cur.execute(f'''INSERT INTO BillettKjop VALUES ({latestRef+1}, '2024-02-01', '14:15', 1)''')
        

    currSeet = 1
    for x in HoverdsceneSeeting:
        # cur.execute("SELECT * FROM Billett")
        # rows = cur.fetchall()
        # print(rows)
        # print(currSeet)
        if x == '0':
            currSeet += 1
            continue
        elif x == 'x':
            currSeet += 1
            continue
        elif x == '1':
            # print('Her is a booked seet')
            cur.execute("SELECT SeteID FROM Sete WHERE SeteNr =? AND SalNavn =?", (currSeet,'Hovedscene'))
            seetForTicket = (cur.fetchall()[0])[0]
            # BilRef = 1
            cur.execute("SELECT BillettID FROM Billett")
            rows = cur.fetchall()
            # print(rows)
            # print(len(rows))
            
            if len(rows) == 0:
                # print('there dont exsists a BilRef')
                cur.execute(f'''INSERT INTO Billett VALUES (1, 450.00, {latestRef}, {VisID}, {seetForTicket}, 1)''')
                currSeet += 1
                # continue
            else:# len(cur.fetchall()) != 0:
                # print('there exsists a BilRef')
                BilRef = rows[-1]
                BilRef = BilRef[0]
                cur.execute(f'''INSERT INTO Billett VALUES ({BilRef+1}, 450.00, {latestRef}, {VisID}, {seetForTicket}, 1)''')
                currSeet += 1
    # cur.execute("SELECT * FROM Billett")
    # rows = cur.fetchall()
    # print(rows)

    conn.commit()
    cur.close()
    conn.close()

def getShowID(database, date, ShowTitle):
    conn = sql.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT VisningsID FROM Visning WHERE Dato =? AND StykkeTittel =?", (date,ShowTitle))
    print('asad', cur.fetchall())
    VisID = (cur.fetchall()[0][0])
    print(VisID)
    cur.close()
    conn.close()

    return VisID

def generateTicketPurchase(database, dato, ShowTitle, UserID):
    conn = sql.connect(database)
    cur = conn.cursor()

    cur.execute("SELECT KjopRef FROM BillettKjop")
    rowBK = (cur.fetchall())
    if len(rowBK) == 0:
        latestRef = 1
        cur.execute(f'''INSERT INTO BillettKjop VALUES ({latestRef}, '2024-02-01', '14:15', {UserID})''')
    else:
        latestRef = (rowBK[-1])[0]
        cur.execute(f'''INSERT INTO BillettKjop VALUES ({latestRef+1}, '2024-02-01', '14:15', {UserID})''')

    conn.commit()
    cur.close()
    conn.close()
    return (latestRef+1)#, VisID

def addTicket(database, latestRef, currSeet, currRow, area, VisID, price):
    conn = sql.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT SeteID FROM Sete WHERE SeteNr =? AND RadNr =? AND Omerade =? AND SalNavn =?", (currSeet, currRow, area, 'Gamle Scene'))
    seetForTicket = (cur.fetchall()[0])[0]
    cur.execute("SELECT BillettID FROM Billett")
    rows = cur.fetchall()
    
    if len(rows) == 0:
        cur.execute(f'''INSERT INTO Billett VALUES (1, {price}, {latestRef}, {VisID}, {seetForTicket}, 1)''')
        conn.commit()
        cur.close()
        conn.close()
    else:
        BilRef = rows[-1]
        BilRef = BilRef[0]
        cur.execute(f'''INSERT INTO Billett VALUES ({BilRef+1}, {price}, {latestRef}, {VisID}, {seetForTicket}, 1)''')
        conn.commit()
        cur.close()
        conn.close()

def readGamleScene(file, database, ShowTitle='Storst av alt er kjaerligheten'):
    price = 450.00
    area = ''
    with open(file, 'r') as f:
        for line in f:
            if "Dato" in line:
                    words = line.split()
                    for word in words:
                        if len(word) == 10 and word[4] == "-" and word[7] == "-":
                            dato =  word
                            print(dato)
                            continue
                    print(dato)
                    latestRef = generateTicketPurchase(database, dato, ShowTitle, UserID=1)
                    # VisID = getShowID(database, dato, 'Storst av alt er kjaerligheten')
                    conn = sql.connect(database)
                    cur = conn.cursor()
                    cur.execute("SELECT VisningsID FROM Visning WHERE Dato=? AND StykkeTittel=?", (dato,'Storst av alt er kjaerligheten'))
                    # cur.execute("SELECT * FROM Visning WHERE Dato =? AND StykkeTittel =?", (dato,ShowTitle))
                    # print('asadøkøl', cur.fetchall()[0][0])
                    VisID = (cur.fetchall()[0][0])
                    print(VisID)
                    cur.close()
                    conn.close()

            elif 'Galleri' in line:
                area = line
                currRow = 4
            elif 'Balkong' in line:
                area = line
                currRow = 5
            elif 'Parkett' in line:
                area = line
                currRow = 11

            elif 'Galleri' in area:
                currSeet = 1
                currRow -= 1
                for x in line[:-1]:
                    if x == '0':
                        currSeet += 1
                        continue
                    elif x == '1':
                        addTicket(database, latestRef, currSeet, currRow, area[:-1], VisID, price)
                        currSeet += 1

            elif 'Balkong' in area:
                currSeet = 1
                currRow -= 1
                for x in line[:-1]:
                    if x == '0':
                        currSeet += 1
                        continue
                    elif x == '1':
                        addTicket(database, latestRef, currSeet, currRow, area[:-1], VisID, price)
                        currSeet += 1
                                    
            elif 'Parkett' in area:
                currSeet = 1
                currRow -= 1
                # print(f'row: {currRow}')
                for x in line[:-1]:                 
                    # print(f'Seet: {currSeet}', x)

                    if x == '0':
                        currSeet += 1
                        continue
                    elif x == '1':
                        addTicket(database, latestRef, currSeet, currRow, area[:-1], VisID, price)
                        currSeet += 1
            else:
                continue
    f.close()

    print('Seeting assigned')

    
def createUser(Name, Tlf, Adress, database):
    conn = sql.connect(database)
    cur = conn.cursor()

    cur.execute("SELECT BrukerID FROM Bruker")
    UserID = (cur.fetchall()[-1])[0]

    cur.execute(f'''INSERT INTO Bruker VALUES ({UserID+1}, '{Name}', {Tlf}, '{Adress}')''')
    cur.execute("SELECT BrukerID FROM Bruker")
    UserID = (cur.fetchall()[-1])[0]

    # for row in cur.execute("SELECT * FROM Bruker"):
    #     print(row)
    
    conn.commit()
    cur.close()
    conn.close()
    


def common_member(a, b):
    return any(i in b for i in a)

def PurchaseTickets(UserID, ticketType, numOfTickets, ShowTitle, date, database):
        latestKjopRef, VisID = generateTicketPurchase(database, date, ShowTitle, UserID)
        VisID = getShowID(database, date, ShowTitle)

        conn = sql.connect(database)
        cur = conn.cursor()
        cur.execute("SELECT GruppeID FROM Gruppe WHERE GruppeNavn =?", (ticketType,))

        GroupID = cur.fetchall()[0][0]
        print(GroupID)

        cur.execute("SELECT Pris.Pris FROM Pris WHERE GruppeID =? AND StykkeTittel =?", (GroupID, ShowTitle))
        singalTicketPrice = cur.fetchone()[0]
        print(singalTicketPrice)


        asd = pd.read_sql_query(f'''
                                SELECT RadNr AS RadNummer, Omerade, COUNT(SeteID) AS Num_Seter_Booket FROM Billett 
                                INNER JOIN Sete USING(SeteID)
                                GROUP BY VisningsID, Omerade, RadNr
                                HAVING Billett.VisningsID={VisID}
                                
                                ''', conn)

        SeetsTakenPerRow = []
        for i in range(len(asd)):
                row_list1 = asd.loc[i, :].values.flatten().tolist()
                SeetsTakenPerRow.append(row_list1)
        print(SeetsTakenPerRow)

        asdf = pd.read_sql_query(f'''
                                SELECT RadNr AS RadNummer, Omerade, COUNT(SeteID) AS Num_Seter_Booket 
                                FROM Sete 
                                INNER JOIN Stykke USING(SalNavn)
                                GROUP BY SalNavn, Omerade, RadNr
                                HAVING StykkeTittel='Storst av alt er kjaerligheten'
                                
                                ''', conn)
        # print(asdf)

        numOfSeetsPerRow = []
        for i in range(len(asdf)):
                row_list2 = asdf.loc[i, :].values.flatten().tolist()
                numOfSeetsPerRow.append(row_list2)
        print(numOfSeetsPerRow)
        print(numOfSeetsPerRow[0][2])
        for p in range(len(numOfSeetsPerRow)):
                for l in range(len(SeetsTakenPerRow)):
                        if numOfSeetsPerRow[p][:-1] == SeetsTakenPerRow[l][:-1]:
                                if numOfSeetsPerRow[p][-1] > SeetsTakenPerRow[l][-1]+9:
                                        row = SeetsTakenPerRow[l][0]
                                        area = SeetsTakenPerRow[l][1]
                                        break
                                else:
                                        continue
                        else:
                                continue
        # print(row, area)
        ListOfTickets = pd.read_sql_query(f'''
                                SELECT SeteID 
                                 FROM Billett 
                                 WHERE VisningsID={VisID}
                                ''', conn)
        ExistingTic = []
        for i in range(len(ListOfTickets)):
                row_list = ListOfTickets.loc[i, :].values.flatten().tolist()
                ExistingTic.append(row_list)
        currSeet = 1
        for i in range(numOfTickets+1):
                cur.execute("SELECT SeteID FROM Sete WHERE SeteNr =? AND RadNr =? AND Omerade =? AND SalNavn =?", (currSeet, row, area, 'Gamle Scene'))
                seetForTicket = (cur.fetchone())
                print(seetForTicket)
                seetForTicket
                

                if seetForTicket in ExistingTic:
                        # addTicket(database, latestKjopRef, currSeet, row, area, VisID, singalTicketPrice)
                        currSeet += 1
                        continue
                else:
                        addTicket(database, latestKjopRef, currSeet, row, area, VisID, singalTicketPrice)
                        currSeet += 1


        # cur.execute("SELECT SeteID FROM Billett WHERE VisningsID =?", (VisID,))
        # Tic = cur.fetchall()
        # print(Tic)




        cur.close()
        conn.close()


        # for n in range(numOfTickets):
        #     addTicket(database, latestKjopRef, currSeet, currRow, area, VisID, singalTicketPrice)

def getSoldSeets(date, database):
#     VisID = getShowID('testV3.db', '2024-02-03', 'Storst av alt er kjaerligheten')
#     print(VisID)
    VisID = []
    conn = sql.connect(database)
    cur = conn.cursor()
    

    cur.execute("SELECT VisningsID FROM Visning WHERE Dato =? ", (date,))
    VisIDs = (cur.fetchall())
    if len(VisIDs) > 1:
        for j in range(len(VisIDs)):
            VisID.append((VisIDs[j])[0])
        VisID = tuple(VisID)
        # print(VisID)
    else:
        VisID = [VisIDs[0][0]]
        # print(VisID)


    checkVisID_in_Tic = f'''
                        SELECT VisningsID FROM Billett
                        '''
    VisIDforTickets = pd.read_sql_query(checkVisID_in_Tic, conn)
    # print(VisIDforTickets)
    VisIDforTickets = VisIDforTickets['VisningsID'].tolist()
    # print(VisIDforTickets)
    VisID_Tup = tuple(VisID)
    if common_member(VisID, VisIDforTickets):
        if len(VisID_Tup) == 1:
            VisID_Tup = VisID_Tup[0]
            ShowCapTit = pd.read_sql_query(f'''SELECT Visning.VisningsID, Kapasitet AS Ledige_Billetter, Visning.StykkeTittel 
                                                FROM (( Visning
                                                INNER JOIN Stykke ON Visning.StykkeTittel=Stykke.StykkeTittel)
                                                INNER JOIN Sal ON Stykke.SalNavn=Sal.SalNavn)
                                                WHERE Visning.VisningsID = {VisID_Tup};
                                            ''', conn)
        else:
            ShowCapTit = pd.read_sql_query(f'''SELECT Visning.VisningsID, Kapasitet AS Ledige_Billetter, Visning.StykkeTittel 
                                                FROM (( Visning
                                                INNER JOIN Stykke ON Visning.StykkeTittel=Stykke.StykkeTittel)
                                                INNER JOIN Sal ON Stykke.SalNavn=Sal.SalNavn)
                                                WHERE Visning.VisningsID IN {VisID_Tup};
                                            ''', conn)
        # print(ShowCapTit)

        NumOfPutTic = pd.read_sql_query(f'''SELECT Visning.VisningsID, COUNT(Billett.SeteID) AS Solgte_Billetter, Visning.StykkeTittel 
                                            FROM (( Visning
                                            INNER JOIN Stykke ON Visning.StykkeTittel=Stykke.StykkeTittel)
                                            INNER JOIN Billett USING(VisningsID))
                                            GROUP BY VisningsID  
                                        ''', conn)
        print(NumOfPutTic)

        for i in range(len(VisID)):
            row_list1 = ShowCapTit.loc[i, :].values.flatten().tolist()
            row_list1 = tuple(row_list1)
            row_list2 = NumOfPutTic.loc[i, :].values.flatten().tolist()
            row_list2 = tuple(row_list2)
            print(f'Det har blitt solgt {row_list2[1]}/{row_list1[1]} for {row_list1[2]} den {date}')
    else:
        if len(VisID_Tup) == 1:
            VisID_Tup = VisID_Tup[0]
            ShowCapTit = pd.read_sql_query(f'''SELECT Visning.VisningsID, Kapasitet AS Ledige_Billetter, Visning.StykkeTittel 
                                                FROM (( Visning
                                                INNER JOIN Stykke ON Visning.StykkeTittel=Stykke.StykkeTittel)
                                                INNER JOIN Sal ON Stykke.SalNavn=Sal.SalNavn)
                                                WHERE Visning.VisningsID = {VisID_Tup};
                                            ''', conn)
        else:
            ShowCapTit = pd.read_sql_query(f'''SELECT Visning.VisningsID, Kapasitet AS Ledige_Billetter, Visning.StykkeTittel 
                                                FROM (( Visning
                                                INNER JOIN Stykke ON Visning.StykkeTittel=Stykke.StykkeTittel)
                                                INNER JOIN Sal ON Stykke.SalNavn=Sal.SalNavn)
                                                WHERE Visning.VisningsID IN {VisID_Tup};
                                            ''', conn)
        print(ShowCapTit)

        for i in range(len(VisID)):
            row_list = ShowCapTit.loc[i, :].values.flatten().tolist()
            row_list = tuple(row_list)
            print(f'Det har blitt solgt 0/{row_list[1]} for {row_list[2]} den {date}')

    cur.close()
    conn.close()
