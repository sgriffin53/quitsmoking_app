
# Flask app

from flask import Flask, request, make_response
import datetime

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(int(value), name))
    return ', '.join(result[:granularity])

benefits = []
benefits.append([60 * 20, '20 minutes: Your resting heart rate has already reduced (this is a key indicator of your overall fitness level)'])
benefits.append([3600 * 8, '8 hours: Nicotine in your system has halved'])
benefits.append([3600 * 12, '12 hours: The carbon monoxide level in your blood has decreased dramatically<br><li> 12 hours:Oxygen levels in your blood have improved'])
benefits.append([3600 * 24, '24 hours: The nicotine level in your blood drops to a negligible amount.'])
benefits.append([3600 * 48, '48 hours: All carbon monoxide is flushed out. Your lungs are clearing out mucus and your senses of taste and smell are improving'])
benefits.append([3600 * 48, '48 hours: Previously damaged nerve endings start to regrow.'])
benefits.append([3600 * 72, '72 hours: If you notice that breathing feels easier, it\'s because your bronchial tubes have started to relax. Also your energy will be increasing'])
benefits.append([3600 * 72, '72 hours: In addition, your lung capacity, or the ability of the lungs to fill up with air, increases about three days after quitting.'])
benefits.append([3600 * 24 * 7, '7 days: After a week without smoking, the carbon monoxide in your blood drops to normal levels.'])
benefits.append([604800 * 2, '''2 weeks: You now have a lower risk of heart attack<br>
<li> 2 weeks: You find breathing easier<br>
<li> 2 weeks: Your circulation is better<br>
<li> 2 weeks: You find exercise much easier<br>
<li> 2 weeks: Your lung function has improved'''])
benefits.append([604800 * 4, '''1 month: You now cough less and have fewer instances of shortness of breath<br>
<li> 1 month: Fibers in the lungs that help keep the lungs healthy are growing back. These fibers can help reduce excess mucus buildup and protect against bacterial infections.'''])
benefits.append([604800 * 52, '''1 year: Your risk of coronary heart disease is now about half that of someone who continues to smoke'''])
benefits.append([604800 * 52 * 10, '''10 years: More great news! Your risk of death from lung cancer will have halved compared with a smoker's.'''])

moneymilestones = []
moneymilestones.append([108000, 'A university degree'])
moneymilestones.append([45000, 'A deposit for a house'])
moneymilestones.append([27146, 'A year of university study'])
moneymilestones.append([5000, 'A luxury cruise'])
moneymilestones.append([2000, 'A new gaming PC'])
moneymilestones.append([500, 'A new smartphone'])
moneymilestones.append([300, 'A new bed and mattress'])
moneymilestones.append([200, 'Concert tickets'])
moneymilestones.append([50, 'Dinner at a nice restaurant'])
moneymilestones.append([20, 'A takeaway meal'])
moneymilestones.append([10, 'A movie ticket'])


app = Flask(__name__)

@app.route('/quitsmoking', methods=['GET', 'POST'])
def page():
    cookie_name = str(request.cookies.get('name'))
    cookie_date = str(request.cookies.get('quit-date'))
    cookie_saved = str(request.cookies.get('saved-per-day'))
    get_name = str(request.args.get('name'))
    get_quit_date = str(request.args.get('quit-date'))
    get_saved = str(request.args.get('saved-per-day'))
    now = datetime.datetime.now()
    outtext = '<center><h2>Stop smoking tracker</h2><h3>Sign Up</h3>'
    outtext += '<form><table>'
    outtext += '<tr><td>Name: </td><td><input type="text" name="name"></td></tr>'
    outtext += '<tr><td>Quit date: </td><td><input type="text" name="quit-date"></td></tr>'
    outtext += '<tr><td></td><td>(Format: DD-MM-YYYY HH:MM)</td></tr>'
    outtext += '<tr><td></td><td>Enter quit date in server timezone for accuracy.<br>Current server time is: '
    outtext += datetime.datetime.now().strftime('%d-%m-%Y %H:%M') + '</td></tr>'
    outtext += '<tr><td>Money saved per day: </td><td> $<input type="text" name="saved-per-day"></td></tr>'
    outtext += '</td></tr>'
    outtext += '<tr><td></td><td><input type="submit" value="Sign Up"></td></tr></table></form>'
    signup_page = outtext
    if get_name == 'None' and cookie_name == 'None':
        return signup_page
    if get_name != 'None':
        if get_name == 'None' and get_quit_date == 'None' and get_saved == 'None':
            return signup_page
        elif get_name == '' or get_quit_date == '':
                return signup_page
        else:
            if " " not in get_quit_date:
                outtext = signup_page
                outtext += "<P>Invalid quit date."
                return outtext
            date = get_quit_date.split(" ")[0]
            time = get_quit_date.split(" ")[1]
            if date.count("-") < 2 or time.count(":") < 1:
                outtext = signup_page
                outtext += "<P>Invalid quit date."
                outtext += "<P>" + str(date.count("-")) + ":::" + str(time.count(":")) + "<br>"
                return outtext
            day = int(date.split("-")[0])
            month = int(date.split("-")[1])
            year = int(date.split("-")[2])
            hour = int(time.split(":")[0])
            mins = int(time.split(":")[1])
            if day < 1 or day > 31 or month < 1 or month > 12 or year < 1 or year < 1000 or hour < 0 or hour > 24 or mins < 0 or mins > 60:
                outtext = signup_page
                outtext += "<P>Invalid quit date."
                return outtext
            # check if date is in the future
            date_format = "%d-%m-%Y %H:%M"
            quit_date = datetime.datetime.strptime(get_quit_date, date_format)
            if quit_date > now:
                outtext = signup_page
                outtext += "<P>Quit date is in the future."
                return outtext
            if not get_saved.replace('.','',1).isdigit():
                outtext = signup_page
                outtext += "<P>Money saved per day must be a number."
                return outtext
            outtext = "<center>Successfully signed up as " + get_name + "<br>"
            outtext += "Your data has been saved to your browser.<br>"
            outtext += '<a href="/quitsmoking">Click here to go to your quit smoking page.</a><br>'
            resp = make_response(outtext)
            resp.set_cookie('name', get_name, samesite='Lax')
            resp.set_cookie('quit-date', get_quit_date, samesite='Lax')
            resp.set_cookie('saved-per-day', get_saved, samesite='Lax')
            myfile = open('log.txt','a')
            myfile.write(datetime.datetime.now().strftime('%d-%m-%Y %H:%M') + " - " + get_name + " - " + get_quit_date + " - " + get_saved + "\n")
            myfile.close()
            return resp
    else:
        quit_date = cookie_date
        date = quit_date.split(" ")[0]
        time = quit_date.split(" ")[1]
        day = int(date.split("-")[0])
        month = int(date.split("-")[1])
        year = int(date.split("-")[2])
        hour = int(time.split(":")[0])
        mins = int(time.split(":")[1])
        #quit_date = '13-16-00-08-07-2024'
        #segments = quit_date.split("-")
        quitdate_dt = datetime.datetime(year, month, day, hour, mins, 0)
        current_dt = datetime.datetime.now()
        time_difference = current_dt - quitdate_dt
        quittime_seconds = time_difference.total_seconds()

        quittime_display = display_time(int(time_difference.total_seconds()), 4)
        saved_per_day = float(cookie_saved)
        saved_per_second = saved_per_day / 24 / 60 / 60
        total_saved = saved_per_second * time_difference.total_seconds()
        total_saved = round(total_saved,2)
        outtext = ''
        outtext += '<html><body>'
        outtext += '<center><h1>' + cookie_name + '\'s Quit Smoking Tracker</h1>'
        outtext += '<p style=\'font-family:verdana; font-size:26px;\'>'
        outtext += 'Quit Date: ' + str(day) + "/" + str(month) + "/" + str(year) + " " + str(hour) + ":" + str(mins) + ":" + "00" + "<br>"
        outtext += 'Time Quit: <b>' + quittime_display + '</b><br>'
        outtext += 'Money Saved: $' + str(total_saved) + ''
        outtext += '</p><p style="font-family:verdana; font-size: 26px"> With your savings, you could buy:<br><p style="font-size:22px">'
        money_left = total_saved
        for milestone in moneymilestones:
            amount = milestone[0]
            text = milestone[1]
            if money_left > amount:
                money_left -= amount
                outtext += "<li> " + text + " ($" + str(amount) + ")"
        if money_left == total_saved:
            outtext += "<li> Nothing yet"
        outtext += '</p><p style="font-family:verdana; font-size: 26px"> Health benefits: <br>'
        still_locked = 0
        next_at = 'None'
        for benefit in benefits:
            seconds = benefit[0]
            desc = benefit[1]
            if quittime_seconds >= seconds:
                outtext += '<li> ' + desc + '<br>'
            else:
                still_locked += desc.count("<li>") + 1
                if next_at == 'None': next_at = desc.split(":")[0]
        outtext += '<p style="font-size:16px">' + str(still_locked) + ' benefits still to unlock (next at ' + next_at + ').</p>'
        outtext += '<hr><br><br><br><br>'
        outtext += '<center><h2>Change Details:</h3>'
        outtext += '<form><table>'
        outtext += '<tr><td>Name: </td><td><input type="text" name="name" value="' + cookie_name + '"></td></tr>'
        outtext += '<tr><td>Quit date: </td><td><input type="text" name="quit-date" value="' + cookie_date + '"></td></tr>'
        outtext += '<tr><td></td><td>(Format: DD-MM-YYYY HH:MM)</td></tr>'
        outtext += '<tr><td></td><td>Enter quit date in server timezone for accuracy.<br>Current server time is: '
        outtext += datetime.datetime.now().strftime('%d-%m-%Y %H:%M') + '</td></tr>'
        outtext += '<tr><td>Money saved per day: </td><td> $<input type="text" name="saved-per-day" value="' + cookie_saved + '"></td></tr>'
        outtext += '<tr><td></td><td><input type="submit" value="Change Details"></td></tr></table></form>'
        outtext += '</body></html>'
        return outtext
    return 'None'


@app.route('/')
def page2():
    outtext = '<h2><a href="/quitsmoking">Try the quit smoking tracker</a></h2>'
    return outtext