from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView
from faker.generator import random
from .forms import SchemaForm, ColumnForm, MyFormSet
import csv
from django.shortcuts import get_object_or_404
from .models import Schema, Column, DataSet
from faker import Faker
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.core.files import File
from io import StringIO


class SchemaListView(LoginRequiredMixin, ListView):
    model = Schema
    template_name = 'list_schemas.html'
    context_object_name = 'schemas'
    extra_context = {'title': "Schema"}


class SchemaDetailView(LoginRequiredMixin, DetailView):
    model = Schema
    template_name = "schema_detail.html"
    context_object_name = 'schema'
    extra_context = {'title': "schema detail"}

    def get_object(self):
        return Schema.get_by_id(self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        fake = Faker()
        num_records = int(request.POST['num-records'])
        schema = self.get_object()
        columns = schema.columns.order_by('order')
        data = []
        type_generators = {
            'full_name': fake.name,
            'job': fake.job,
            'email': fake.email,
            'domain_name': fake.domain_name,
            'phone_number': fake.phone_number,
            'company_name': fake.company,
            'text': lambda: fake.text(3),
            'integer': lambda column: random.randint(int(column.range_start) if column.range_start else 0,
                                                     int(column.range_end) if column.range_end else 100),
            'address': fake.address,
            'date': lambda: fake.date_between(start_date='-30d', end_date='today')
        }

        for i in range(num_records):
            record = {}
            for column in columns:
                if column.type in type_generators:
                    if column.type == 'integer':
                        record[column.name] = type_generators[column.type](column)
                    else:
                        record[column.name] = type_generators[column.type]()
            data.append(record)
        data_set = DataSet.objects.create(schema=schema, status=True)
        data_set.name = f'{schema.name}.csv'
        headers = [column.name for column in columns]
        data_set.csv.save(data_set.name, StringIO(f'{schema.column_separator}'
                                                  .join(headers)))

        with data_set.csv.open('w') as f:
            writer = csv.writer(f, delimiter=schema.column_separator,
                                quotechar=schema.column_characters,
                                quoting=csv.QUOTE_MINIMAL)

            # Write the headers
            headers = [column.name for column in columns]
            writer.writerow(headers)

            # Write the data
            for record in data:
                row = [record.get(column.name, '') for column in columns]
                writer.writerow(row)

        schema.status = 'ready'
        schema.save()

        download_link = reverse('download_csv',
                                kwargs={'dataset_id': data_set.id})
        serialized_dataset = serializers.serialize('json', [data_set])
        data = {'download_link': download_link,
                'data_set': serialized_dataset}

        return JsonResponse(data)

@login_required
def create_schema(request):
    schema_form = SchemaForm(request.POST or None)
    column_formset = modelformset_factory(Column, ColumnForm, extra=0, can_delete=True, formset=MyFormSet)
    column_set = column_formset(request.POST or None, queryset=Column.objects.none())
    context = {
        'schema_form': schema_form,
        'column_formset': column_set
    }
    if request.method == 'POST':
        if schema_form.is_valid() and column_set.is_valid():
            _schema = schema_form.save(commit=False)
            _schema.owner = request.user
            _schema.save()
            for form in column_set:
                if form.is_valid() and form.cleaned_data:
                    column = form.save(commit=False)
                    column.schema = _schema
                    column.save()
                else:
                    messages.error(request, 'Fill out the form!!')
                    return HttpResponseRedirect(reverse('create_schema'))
            return redirect('schema_detail', pk=_schema.id)
    return render(request, 'create_schema.html', context)


@login_required
def delete_schema(request, pk):
    Schema.get_by_id(pk).delete()
    return HttpResponseRedirect(reverse('schemas'))


@login_required
def update_schema(request, pk):
    schema = get_object_or_404(Schema, pk=pk)
    schema_form = SchemaForm(request.POST or None, instance=schema)
    column_formset = modelformset_factory(Column, ColumnForm, extra=0, formset=MyFormSet, can_delete=True)
    column_set = column_formset(request.POST or None, queryset=schema.columns.all())
    context = {
        'schema_form': schema_form,
        'column_formset': column_set
    }
    if request.method == 'POST':
        if schema_form.is_valid() and column_set.is_valid():
            _schema = schema_form.save(commit=False)
            _schema.owner = request.user
            _schema.save()
            for form in column_set:
                if form.is_valid() and form.cleaned_data:
                    column = form.save(commit=False)
                    column.schema = _schema
                    column.save()
                else:
                    messages.error(request, 'Fill out the form!!')
                    return HttpResponseRedirect(reverse('create_schema'))
            return redirect('schema_detail', pk=_schema.id)
    return render(request, 'create_schema.html', context)


def download(request, dataset_id):
    dataset = get_object_or_404(DataSet, pk=dataset_id)
    file_path = dataset.csv.path
    if file_path:
        with open(file_path, 'rb') as f:
            csv_file = File(f)
            response = HttpResponse(csv_file, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{dataset.name}.csv"'
        return response
    return HttpResponse(status=404)

class DeleteColumnView(LoginRequiredMixin, View):

    def delete(self, request, pk):
        if request.method == "DELETE":
            try:
                Column.delete_by_id(pk)
                return JsonResponse({'success': True})
            except:
                return JsonResponse({'success': False})
        else:
            return JsonResponse({"error": "Invalid request method"})
