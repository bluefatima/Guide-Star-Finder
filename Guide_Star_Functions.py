
########################################
def angnorm(angle):
    
    ##when given an angle in degrees, output is angle 0<θ<360
    
    while angle >=360:
        angle -= 360
    while angle < 0:
        angle += 360
    return angle

def J2000(year, month, day, hour, minute):

    ## converts observing time/date into days since J2000
    ##WILL ONLY WORK UNTIL 2021

    monthdays = {1:0, 2:31, 3:59, 4:90, 5:120, 6:151, 7:181, 8:212, 9:243, 10:273, 11:304, 12:334}
    yeardays = {1998:-731.5, 2008:2920.5, 2016:5842.5, 2017:6208.5, 2018:6573.5, 2019:6938.5, 2020:7303.5, 2021:7669.5}

    days = monthdays[month] + yeardays[year] + day + ((hour + (minute / 60)) / 24)
    if year % 4 == 0 and monthdays[month] > 2:
        days += 1
    return days

def locsidtime(d, long, UT):
    
    ##Local sidereal time calculator (output in degrees)
    #inputs: d = days from J2000, long=longitude(degrees),
    ##UT = univeral time in decimal hours
    
    LST = 100.46 + (0.985647 * d) + long + (15 * UT)
    return angnorm(LST)

def airmass2alt(X):

    ## converts airmass to zenith angle in degrees
    
    from numpy import arccos, rad2deg
    z = rad2deg(arccos(1/X))
    #alt = 90 - z #gives altitude angle
    return(z)
