from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory
from .models import Pizza

def home(request):
    return render(request, 'pizza/home.html')

def order(request):
    multiple_form = MultiplePizzaForm()
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST)
        if filled_form.is_valid():
             # Save the pizza in database
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
            note = 'Thanks for ordering! Your %s %s and %s pizza is on its way!' %(filled_form.cleaned_data['size'],
            filled_form.cleaned_data['topping1'],
            filled_form.cleaned_data['topping2'],)
            new_form = PizzaForm()
            return render(request, 'pizza/order.html', {'created_pizza_pk': created_pizza_pk, 'pizzaform':new_form, 'note': note, 'multiple_form': multiple_form})
    else:
        form = PizzaForm()
        return render(request, 'pizza/order.html', {'pizzaform':form, 'multiple_form':multiple_form})

# A function for the pizzas view.

def pizzas(request):
    number_of_pizzas = 2
    filled_multiple_pizza_form = MultiplePizzaForm(request.GET)

    # Checking if user has provided valid number.

    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data['number'] 
    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()

    # Checking if request method is post or get.
        
    if request.method == 'POST':
        filled_formset = PizzaFormSet(request.POST)

        # Checking if filled_formset has valid value.
        
        if filled_formset.is_valid():
            note = 'Pizzas have been ordered!'
        else: 
            note = 'Order was not created, please try again.'
        return render(request, 'pizza/pizzas.html', {'note' : note, 'formset' : formset})
    else:
        return render(request, 'pizza/pizzas.html', {'formset' : formset})

# A function to handle editing and order

def edit_order(request, pk):
    # Grab the selected pizza from the database.
    pizza = Pizza.objects.get(pk = pk)
    # To have a filled out form if user whants to change data.
    form = PizzaForm(instance=pizza)
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
    return render(request, 'pizza/edit_order.html', {'pizzaform':form, 'pizza' : pizza})