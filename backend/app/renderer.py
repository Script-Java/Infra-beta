import plotly.express as px

class Renderer:
    def __init__(self, charts, df):
        self.charts = charts
        self.df = df

    def render_charts(self):
        rendered_charts = []

        for chart in self.charts:
            chart_type = chart.get('chart_type')
            x = chart.get('x')
            y = chart.get('y')
            title = chart.get('title')
            description = chart.get('description')

            # Handle list of Y columns
            if isinstance(y, list):
                y_valid = [col for col in y if col in self.df.columns]
                if not y_valid:
                    continue
            else:
                if x not in self.df.columns or y not in self.df.columns:
                    continue
                y_valid = [y]

            fig = None
            if chart_type == 'bar':
                fig = px.bar(self.df, x=x, y=y_valid, title=title)
            elif chart_type == 'line':
                fig = px.line(self.df, x=x, y=y_valid, title=title)
            elif chart_type == 'scatter' and len(y_valid) == 1:
                fig = px.scatter(self.df, x=x, y=y_valid[0], title=title)
            elif chart_type == 'histogram' and len(y_valid) == 1:
                fig = px.histogram(self.df, x=y_valid[0], title=title)

            if fig:
                rendered_charts.append({
                    "title": title,
                    "description": description,
                    "chart_type": chart_type,
                    "plotly_json": fig.to_json()
                })

        return rendered_charts
