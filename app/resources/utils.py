import base64
import io


def pandas_plot_to_html(fig):
    """Convert a matplotlib figure object to an html element

    Args:
        fig (matplotlib.figure.Figure): Figure to be plotted.

    Returns:
        str: An html img element containig the figure sent.
    """
    img = io.BytesIO()
    fig.set_tight_layout(True)
    fig.savefig(img, format='png')
    fig.clf()
    img_str = base64.b64encode(img.getvalue()).decode()
    html = '<img src="data:image/png;base64,{}"/>'.format(img_str)
    return html
