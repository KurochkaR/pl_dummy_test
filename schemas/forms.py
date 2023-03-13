from django import forms
from django.forms import BaseModelFormSet
from django.forms.formsets import DELETION_FIELD_NAME

from .models import Schema, Column


class SchemaForm(forms.ModelForm):

    class Meta:
        model = Schema
        fields = ['name', 'column_separator', 'column_characters']
        labels = {'name': 'Name',
                  'column_separator': 'Column separator',
                  'column_characters': 'String character',
                  }
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'column_separator': forms.Select(attrs={'class': 'form-control'}),
                   'column_characters': forms.Select(attrs={'class': 'form-control'}),
                   }


class ColumnForm(forms.ModelForm):

    class Meta:
        model = Column
        fields = ['name', 'type', 'range_start', 'range_end', 'order']
        required = (
            'name',
            'type',
            'order',
        )

        labels = {'name': 'Column name',
                  'type': 'Type',
                  'range_start': 'From',
                  'range_end': 'To',
                  'order': 'Order'
                  }
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'type': forms.Select(attrs={'class': 'form-control'}),
                  'range_start': forms.NumberInput(attrs={'class': 'form-control'}),
                  'range_end': forms.NumberInput(attrs={'class': 'form-control'}),
                  'order': forms.NumberInput(attrs={'class': 'form-control'})
                   }


class MyFormSet(BaseModelFormSet):
    def add_fields(self, form, index):
        super(MyFormSet, self).add_fields(form, index)
        form.fields[DELETION_FIELD_NAME].widget = forms.HiddenInput()
