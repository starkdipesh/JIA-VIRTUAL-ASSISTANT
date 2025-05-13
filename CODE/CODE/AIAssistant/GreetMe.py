import datetime

def gretme():
    hour=int(datetime.datetime.now().hour)
    if hour>=6 and hour<12:
        return "Good Morning Sir"
    elif hour>=12 and hour<16:
        return "Good Afternoon Sir"
    elif hour>=16 and hour<=20:
        return "Good Evening Sir"
    else:
        return "Good Evening Sir"