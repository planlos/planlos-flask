# coding: utf-8

from jinja2 import contextfunction, Markup
from flask import current_app as app
import calendar as cal
from datetime import datetime, timedelta, date
from planlos.extensions import db
from planlos.documents import Event

widgets = {}


class Day:
    def __init__(self, date, month):
        if date.month == month:
            self.date = date
        else:
            self.date = None
        self.map = {0: 'mon', 1: 'tue', 2: 'wed',
                    3: 'thu', 4: 'fri', 5: 'sat',
                    6: 'sun'}

    def _has_event(self):
        today = datetime(int(self.date.year),
                         int(self.date.month),
                         int(self.date.day),
                         0, 0, 0, 0)
        tomorrow = today + timedelta(days=1)
        events = db.Event.find({'eventdate':
                                    {'$lt': tomorrow, '$gt': today}}).count()
        print "DEBUG (events.count() )", events
        if events > 0:
            return True
        else:
            return False

    def __str__(self):
        if self.date is None:
            return """<td class="unknown">&nbsp;</td>"""
        elif self._has_event():
            return """<td class="%s"><a href="/events/%s/%s/%s">%s</a></td>""" % (self.map[self.date.weekday()], self.date.year, self.date.month, self.date.day, self.date.day)
        else:
            return """<td class="%s">%s</td>""" % (self.map[self.date.weekday()],
                                                   self.date.day)


class Week:
    def __init__(self, days, month):
        self.days = days
        self.month = month

    def __str__(self):
        htmlstring = "<tr>"
        for day in self.days:
            htmlstring += day.__str__()
        htmlstring += "</tr>"
        return htmlstring


class EventCalendar:
    def __init__(self, year, month):
        self.date = date(year, month, 1)
        self.cal = cal.Calendar()
        self.month = self.build_calendar(year, month)

    def __str__(self):
        inner_cal = ''
        for week in self.month:
            inner_cal += week.__str__()
        htmlstring = """<div class='eventcalendar'><span class"monthheader">%s</span><table><tr><th>Mo</th><th>Di</th><th>Mi</th><th>Do</th><th>Fr</th><th>Sa</th><th>So</th></tr>%s</table></div>""" % (self.date.strftime("%B"), inner_cal)
        return htmlstring

    def build_calendar(self, year, month):
        c = cal.Calendar()
        weeks = []
        for week in c.monthdatescalendar(year, month):
            days = []
            for day in week:
                days.append(Day(day, month))
            weeks.append(Week(days, month))
        return weeks


def _next_month(year, month):
    month = month + 1
    if month > 12:
        month = 1
        year += 1
    return year, month


def calendar(context, **extra_context):
    t = app.jinja_env.get_template('widgets/calendar_widget.html')
    ctx = dict(context.items())
    ctx.update(extra_context)
    today = date.today()
    ctx.update({'cal': EventCalendar(today.year,
                                     today.month)})
    year, month = _next_month(today.year, today.month)
    ctx.update({'cal2': EventCalendar(year, month)})
    year, month = _next_month(year, month)
    ctx.update({'cal3': EventCalendar(year, month)})
    return Markup(t.render(ctx))


@contextfunction
def widget(context, func, **extra_context):
    return widgets[func](context, **extra_context)


widgets.update({'calendar': calendar})



#app.jinja_env.globals['widget'] = widget
