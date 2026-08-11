from datetime import datetime

date1 = "20/06/2013"
date2 = "25/06/2013"
date3 = "01/07/2013"
date4 = "07/07/2013"

date1 = datetime.strptime(date1, "%d/%m/%Y").astimezone()
date2 = datetime.strptime(date2, "%d/%m/%Y").astimezone()
date3 = datetime.strptime(date3, "%d/%m/%Y").astimezone()
date4 = datetime.strptime(date4, "%d/%m/%Y").astimezone()

datelist = [date1, date2, date3]

for j in datelist:
    if j <= date4:
        print(j.strftime('%d/%m/%Y'))