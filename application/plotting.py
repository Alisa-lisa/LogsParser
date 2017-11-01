import plotly.offline as offline


def plot(input):
    max_value = max(input.values())
    normalized = [x/max_value for x in input.values()]
    data = [dict(
            type = 'choropleth',
            locations = list(input.keys()),
            z = normalized,
            colorscale = [[0,"rgb(5, 10, 172)"],[0.25*max_value,"rgb(40, 60, 190)"],[0.5*max_value,"rgb(70, 100, 245)"],
                [0.75*max_value,"rgb(106, 137, 247)"],[max_value,"rgb(220, 220, 220)"]],
            autocolorscale = False,
            reversescale = True,
            marker = dict(
                line = dict (
                    color = 'rgb(180,180,180)',
                    width = 0.5
                ) ),
            colorbar = dict(
                tickprefix = 'calls',
                showexponent = 'none',
                title = 'IP calls distribution'),
          )]
    layout = dict(
            title = 'visitors geographically distributed according to the uploaded log',
            geo = dict(
                showframe = False,
                showcoastlines = False,
                projection = dict(
                type = 'Mercator'
            )
        )
    )
    offline.plot({'data': data,
                  'layout': layout})


if __name__ == '__main__':
    input_dict = {"CZE":10, "FRA":30, "DEU":50, "USA":80, "AFG":100}
    plot(input=input_dict)