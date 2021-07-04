import io

from django.core.files.base import File
from django.utils import timezone

from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.styles import Alignment
from openpyxl.styles.borders import Border, Side, BORDER_THIN

from ..models import ExcelReport


class BaseExcelReport:

    def __init__(self, sheet_name=None):
        self.workbook = Workbook()
        self.worksheet = self.workbook.worksheets[0]
        if sheet_name:
            self.worksheet.title = sheet_name

        self._border_style = Side(border_style=BORDER_THIN, color='00000000')
        self.border = Border(
            left=self._border_style,
            right=self._border_style,
            top=self._border_style,
            bottom=self._border_style
        )

        self.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        self.now = timezone.now()

        self.filename = 'report_{}.xlsx'.format(self.now.strftime('%d.%m.%Y'))

    def _write_cell(self, cell, value):
        self.worksheet[cell] = value
        self.worksheet[cell].border = self.border
        self.worksheet[cell].alignment = self.alignment

    def _column_width(self, column, width):
        self.worksheet.column_dimensions[column].width = width

    def _row_height(self, row, height):
        self.worksheet.row_dimensions[row].height = height

    def _merge_cells(self, cell_start, cell_end):
        self.worksheet.merge_cells(cell_start + ':' + cell_end)

    def write_header(self):
        raise NotImplementedError('write_header')

    def write_data(self, qs=None):
        raise NotImplementedError('write_data')

    def for_http_response(self):
        return save_virtual_workbook(self.workbook)

    def for_django_file_field(self):
        virtual_file = io.BytesIO()
        self.workbook.save(virtual_file)
        django_file = File(virtual_file, name=self.filename)
        return django_file


class OfferExcelReport(BaseExcelReport):

    def _get_quarter(self):
        if 1 <= self.now.month <= 3:
            return 1

        if 4 <= self.now.month <= 6:
            return 2

        if 7 <= self.now.month <= 9:
            return 3

        if 10 <= self.now.month <= 12:
            return 4

    def write_header(self):

        self._write_cell('A1', 'Дата формирования отчета')
        self._merge_cells('A1', 'B1')

        self._write_cell('A2', 'Дата')
        self._write_cell('B2', 'Квартал')

        self._write_cell('A3', self.now.strftime('%d.%m.%Y'))
        self._write_cell('B3', self._get_quarter())


        self._write_cell('A5', 'Строительный ресурс')
        self._merge_cells('A5', 'G5')

        self._write_cell('A6', 'КСР')
        self._column_width('A', 30)

        self._write_cell('B6', 'Наименование')
        self._column_width('B', 40)

        self._write_cell('C6', 'Полное наименование (обосновывающий документ)')
        self._column_width('C', 40)

        self._write_cell('D6', 'Единица измерения')
        self._column_width('D', 25)

        self._write_cell('E6', 'Единица измерения (обосновывающий документ)')
        self._column_width('E', 30)

        self._write_cell('F6', 'Цена за единицу с НДС, руб.')
        self._column_width('F', 30)

        self._write_cell('G6', 'Цена за единицу без НДС, руб.')
        self._column_width('G', 30)

        self._write_cell('H5', 'Производитель/поставщик')
        self._merge_cells('H5', 'J5')

        self._write_cell('H6', 'Наименование производителя/поставщика')
        self._column_width('H', 30)

        self._write_cell('I6', 'ИНН')
        self._column_width('I', 15)

        self._write_cell('J6', 'КПП')
        self._column_width('J', 15)

        self._write_cell('K5', 'Доставка')
        self._merge_cells('K5', 'L5')

        self._write_cell('K6', 'Оближайший адрес склада')
        self._column_width('K', 20)

        self._write_cell('L6', 'Стоиомсть доставки, руб.')
        self._column_width('L', 25)

    def write_data(self, qs=None):
        offset = 7

        if qs is None:
            return

        for index, offer in enumerate(qs):
            offer_product = offer.product
            if offer_product:
                resource_code_str = offer_product.resource_code
                name_str = offer_product.name
            else:
                resource_code_str = offer.resource_code or ''
                name_str = offer.name
            self._write_cell('A' + str(offset + index), resource_code_str)
            self._write_cell('B' + str(offset + index), name_str)
            self._write_cell('C' + str(offset + index), offer.name)

            measure_unit_str = offer.measure_unit or ''
            self._write_cell('D' + str(offset + index), measure_unit_str)
            self._write_cell('E' + str(offset + index), measure_unit_str)

            last_price = offer.last_offer_price
            if last_price:
                price_with_vat_str = last_price.price_with_vat
                price_without_vat_str = last_price.price_without_vat
                delivery_cost_str = last_price.delivery_cost
            else:
                price_with_vat_str = ''
                price_without_vat_str = ''
                delivery_cost_str = ''
            self._write_cell('F' + str(offset + index), price_with_vat_str)
            self._write_cell('G' + str(offset + index), price_without_vat_str)

            self._write_cell('H' + str(offset + index), offer.provider.name)
            self._write_cell('I' + str(offset + index), offer.provider.inn)
            self._write_cell('J' + str(offset + index), offer.provider.kpp)
            self._write_cell('K' + str(offset + index), offer.provider.warehouse_location)
            self._write_cell('L' + str(offset + index), delivery_cost_str)

    def generate(self, qs=None):
        self.write_header()
        self.write_data(qs=qs)
        ExcelReport.objects.create(excel=self.for_django_file_field())
