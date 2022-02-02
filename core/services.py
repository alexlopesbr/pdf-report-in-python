from django.http import HttpResponse
from core.models import ProductSold, Config

from reportlab.platypus import Table, TableStyle, Image, PageBreak, SimpleDocTemplate
from reportlab.lib import utils, colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4


def generate_report(request):
    user = request.user
    user_color = user.color
    logo_image = Config.objects.all().first().logo

    date_from = request.GET.get('date_from', None)
    date_to = request.GET.get('date_to', None)
    product = request.GET.get('product', None)
    seller = request.GET.get('seller', None)
    client = request.GET.get('client', None)

    products_sold = ProductSold.objects.all()

    if date_from and date_to:
        products_sold = products_sold.filter(created_at__range=[date_from, date_to])

    if product:
        products_sold = products_sold.filter(product__name__icontains=product)

    if seller:
        products_sold = products_sold.filter(seller__user__name__icontains=seller)

    if client:
        products_sold = products_sold.filter(client__user__name__icontains=client)

    products_sold_report_pdf = 'products_sold_report.pdf'
    pdf = SimpleDocTemplate(products_sold_report_pdf, pagesize=A4, rightMargin=20, leftMargin=30,
                            topMargin=72, bottomMargin=18, title='product sold report')

    elems = []
    elems.append(header(date_from, date_to, logo_image))
    elems.append(table(products_sold, user_color))
    elems.append(results(products_sold))
    PageBreak()

    pdf.build(elems)

    response = HttpResponse(open(products_sold_report_pdf, 'rb'), content_type='application/pdf')
    return response


def header(date_from, date_to, logo_image):

    if logo_image:
        logo = get_image(logo_image, width=5 * cm)
    else:
        logo = 'Logo não encontrada'

    data = [['Período: {} - {}'.format(date_from, date_to), logo], ]
    table = Table(data, colWidths='*')

    style = TableStyle([
        ('ALIGN', (0, 0), (0, 1), 'LEFT'),
        ('ALIGN', (1, 0), (1, 1), 'RIGHT'),
    ])
    table.setStyle(style)

    return table


def get_image(path, width=1 * cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))


def table(products_sold, user_color):

    if user_color:
        color = colors.HexColor(hexa_or_rgb_converted(user_color))
    else:
        color = colors.coral

    lines = []
    for product_sold in products_sold:
        lines.append([product_sold.product.name,
                      product_sold.product.price,
                      wrap_name(product_sold.seller.user.name),
                      product_sold.client.user.name,
                      str(product_sold.created_at.strftime('%d/%m/%Y')),
                      str(product_sold.created_at.strftime('%H:%M'))])

    data = [['Product', 'Price', 'Seller', 'Client', 'Data', 'Hora'], ]

    for line in lines:
        data.append(line)

    table = Table(data, colWidths='*', repeatRows=1)

    style = TableStyle([
        # header
        ('BACKGROUND', (0, 0), (-1, 0), color),

        # body
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('FONT', (0, 1), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOX', (0, 0), (-1, -1), 1, color),
    ])
    table.setStyle(style)

    rowNumber = len(data)
    for i in range(1, rowNumber):
        if i % 2 == 0:
            table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), colors.lavender)]))

    return table


def wrap_name(name):
    name = name.split(' ')[0]
    return name


def hexa_or_rgb_converted(color):
    if color[0] == '#':
        return color

    numbers = color.replace(')', '').replace('(', '').replace('rgb', '').replace(',', ' ').split()
    return rgb_to_hexa_converter(int(numbers[0]), int(numbers[1]), int(numbers[2]))


def rgb_to_hexa_converter(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)


def results(wrong_flow_logs):
    data = [['Total de ocorrências: {}'.format(len(wrong_flow_logs)), ], ]

    table = Table(data, colWidths='*')

    style = TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
        ('FONTSIZE', (0, 0), (0, 0), 12),
        ('FONT', (0, 0), (0, 0), 'Helvetica'),
    ])
    table.setStyle(style)

    return table
