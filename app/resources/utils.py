import base64
import io


def pandas_plot_to_html(pd_plot, img_format='png'):
    """Convert a pandas plot object to an html element

    Args:
        pd_plot: Pandas plot object.
        img_format (str): Format of the image ot produce.

    Returns:
        An html img element.
    """
    img = io.BytesIO()
    fig = pd_plot.get_figure()
    fig.set_tight_layout(True)
    fig.savefig(img, format=img_format)
    img_str = base64.b64encode(img.getvalue()).decode()
    html = '<img src="data:image/png;base64,{}"/>'.format(img_str)
    return html
