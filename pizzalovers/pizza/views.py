from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory

def home(request):
    return render(request, 'pizza/home.html')

def order(request):
    multiple_form = MultiplePizzaForm()
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST)
        if filled_form.is_valid():
             # Save the pizza in database
            filled_form.save()
            note = 'Thanks for ordering! Your %s %s and %s pizza is on its way!' %(filled_form.cleaned_data['size'],
            filled_form.cleaned_data['topping1'],
            filled_form.cleaned_data['topping2'],)
            new_form = PizzaForm()
            return render(request, 'pizza/order.html', {'pizzaform':new_form, 'note': note, 'multiple_form': multiple_form})
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

