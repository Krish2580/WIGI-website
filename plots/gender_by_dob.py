import dateutil
import pandas
from bokeh.charts import TimeSeries
from bokeh.plotting import gridplot
from bokeh.resources import CDN
from bokeh.embed import autoload_static


def plot():
    ra_len = 1

    dox = pandas.DataFrame()
    nonbindox = pandas.DataFrame()

    for l in ['b', 'd']:
        acro = 'do'+l
        df = pandas.DataFrame.from_csv('/home/maximilianklein/snapshot_data/newest/%s-index.csv' % acro)
        del df['nan']
        df['total'] = df.sum(axis=1)
        df['nonbin'] = df['total'] - df['male'] - df['female']
        df['fem_per'] = df['female'] / (df['total'])
        df['nonbin_per'] = df['nonbin'] / df['total']

        ra = pandas.rolling_mean(df['fem_per'], ra_len)
        dox[acro] = ra

        nonbinra = pandas.rolling_mean(df['nonbin_per'], ra_len)
        nonbindox[acro] = nonbinra

    time_range = (1400, 2014)

    dox = dox[time_range[0]: time_range[1]]
    dox['Date'] = [dateutil.parser.parse(str(int(x)))
                   for x in dox['dob'].keys()]

    p1 = TimeSeries(dox, index='Date', legend=True, title="Female Ratios")
    p1.below[0].formatter.formats = dict(years=['%Y'])

    nonbindox = nonbindox[time_range[0]: time_range[1]]
    nonbindox['Date'] = [dateutil.parser.parse(str(int(x)))
                         for x in nonbindox['dob'].keys()]

    p2 = TimeSeries(nonbindox, index='Date', legend=True,
                    title="Non Binary Ratios")
    p2.below[0].formatter.formats = dict(years=['%Y'])

    p = gridplot([[p1], [p2]], toolbar_location=None)

    js_filename = "gender_by_dob.js"
    script_path = "./assets/js/"
    output_path = "./files/assets/js/"

    # generate javascript plot and corresponding script tag
    js, tag = autoload_static(p, CDN, script_path + js_filename)

    with open(output_path + js_filename, 'w') as js_file:
        js_file.write(js)

    return tag

if __name__ == "__main__":
    print(plot())