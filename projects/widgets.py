from django.forms import DateInput

class FengyuanChenDatePickerInput(DateInput):
    template_name = 'projects/widgets/fengyuanchen_datepicker.html'