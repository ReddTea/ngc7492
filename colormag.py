# @auto-fold regex /^\s*if/ /^\s*else/ /^\s*def/
# -*- coding: utf-8 -*-
if True:
    import pandas as pd
    from bokeh.layouts import row, column
    from bokeh.models import Select, Label, ColumnDataSource, HoverTool
    from bokeh.palettes import Spectral5
    from bokeh.plotting import curdoc, figure, show, output_file
    from bokeh.io import output_notebook
    from bokeh.sampledata.autompg import autompg_clean as df
    import scipy as sp

#df = df.copy()

N = 15630
circles = True
CDM=False


datablock = sp.loadtxt('ngc7492_clay.erad', usecols=range(9), skiprows=len(df)-N)
head = ['ID', 'RA', 'DEC', 'g', 'gerr', 'r', 'rerr', 'chi', 'sharp']
df = pd.DataFrame(datablock, columns=head)


x = (df['g']-df['r']).values
y = df['g'].values

radii = df['g'].values / max(df['g'].values) * 0.015

rg = (x-min(x))/max(x) * 250
colors = [
    "#%02x%02x%02x" % (int(r), int(g), 0) for r, g in zip(rg, 250-rg)
]



df.insert(9, 'g-r', x)
df.insert(10, 'Radius', radii)
df.insert(11, 'Color', colors)

TOOLS="pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,save,hover,"

if CDM:
    source1 = ColumnDataSource(df)

    # figure and tools

    p = figure(tools=TOOLS, title="Color Magnitude Diagram", toolbar_location='below')
    p.plot_height=1000
    p.plot_width=1000
    p.y_range.flipped = True

    #str(df['ID'].values.astype('str')[:N])

    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [
        ('ID', '@ID'),
        ('RA(2000.0), DEC(2000.0)', '@RA, @DEC}'),
        ('g-r', '@{g-r}'),
        ('g', '@g'),
        ('chi', '@chi'),
        ('sharp', '@sharp')
        ]

    # title
    p.title.text_font_size = '24pt'
    p.title.align = "center"

    #axis
    p.xaxis.axis_label = 'g - r'
    p.yaxis.axis_label = 'g'
    p.xaxis.axis_label_text_font_size = "22pt"
    p.yaxis.axis_label_text_font_size = "22pt"

    p.xaxis.major_label_text_font_size = "20pt"
    p.yaxis.major_label_text_font_size = "20pt"

    # text
    bokeh_text = Label(x=2.8, y=15, text='N = %i' % N, text_font_size='20pt')
    p.add_layout(bokeh_text)

    # plot
    #p.scatter('g-r', 'g', source=source1, radius='Radius', fill_color='Color',
    #          fill_alpha=0.6, line_color=None)

    p.scatter('g-r', 'g', source=source1, radius='Radius', fill_color='Color',
              fill_alpha=0.6, line_color=None)

    # save and display
    output_file("colormag_diag.html", title="Color Magnitude Diagram")
    show(p)  # open a browser


if circles:
    # CIRCLES
    df['RA'] *= 21600./24
    df['DEC'] *= 60.

    df['RA'] -= sp.mean(df['RA'])
    df['DEC'] -= sp.mean(df['DEC'])

    df = df[df['g']>24]

    radii = (df['g'].values+0.1 - min(df['g'].values)) / max(df['g'].values)
    radii = radii*100
    df['Radius'] = radii


    N = len(df)
    source2 = ColumnDataSource(df)


    p1 = figure(tools=TOOLS, title="Observed Fields", toolbar_location='below')

    p1.plot_height=800
    p1.plot_width=800
    p1.x_range.flipped = True
    bokeh_text = Label(x=-10, y=13, text='N = %i' % N, text_font_size='20pt')
    p1.add_layout(bokeh_text)

    bokeh_text = Label(x=0, y=-9, text='r=8.35\"', text_font_size='16pt', text_color='red',
                       text_font_style='bold')
    p1.add_layout(bokeh_text)

    # title
    p1.title.text_font_size = '24pt'
    p1.title.align = "center"

    #axis
    p1.xaxis.axis_label = 'RA (arcmin)'
    p1.yaxis.axis_label = 'DEC (arcmin)'
    p1.xaxis.axis_label_text_font_size = "22pt"
    p1.yaxis.axis_label_text_font_size = "22pt"

    p1.xaxis.major_label_text_font_size = "20pt"
    p1.yaxis.major_label_text_font_size = "20pt"

    p1.scatter('RA', 'DEC', source=source2, size='Radius')
    p1.arc(2.5, -0.5, radius=8.35, start_angle=0, end_angle=2*sp.pi, color='red')

    output_file("observed_field.html", title="Observed Field")
    show(p1)  # open a browser
