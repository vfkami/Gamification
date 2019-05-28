for line in open('ez.txt').readlines():
    if line.strip() != '':
        try:
            data=line.split(',')
            print('''<li class="single-event"  data-start="{start}" data-end="{end}" data-content="{name}" data-event="event-1">
                            <a id="{name}" href="#0">
                                <em class="event-name">{name}</em>
                                <b>??</b><br><p style="font-size:14px">???</p>
                            </a>
                        </li>'''.format(start=data[0],end=data[1],name=data[2],id=data[2]))
        except:
            print('''<li class="events-group">
                    <div class="top-info"><span>%s</span></div>''' % line)