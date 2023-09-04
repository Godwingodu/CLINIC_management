from django.forms import CheckboxSelectMultiple
from django.utils.html import format_html


class CustomCheckboxSelectMultiple(CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        if not isinstance(value, list):
            value = [value]

        output = []
        for choice in self.choices:
            checkbox_attrs = self.build_attrs(self.attrs, {'type': 'checkbox', 'name': name})
            if str(choice[0]) in value:
                checkbox_attrs['checked'] = 'checked'

            output.append(self.create_option(name, choice, checkbox_attrs))

        return '\n'.join(output)

    def create_option(self, name, value, attrs):
        option_value = self.get_option_value(value)
        if option_value is None:
            option_value = ''
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(self.option_attrs, attrs, {'type': self.input_type, 'name': name, 'value': option_value})
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'])

        return format_html('<label class="checkbox-inline"><input{} /> {}</label>',
                          self.tag(attrs=option_attrs), value)