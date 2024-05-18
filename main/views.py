from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from . import models


# --------------------AUTH_-------------------------------

def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('log_in')

    return render(request, 'auth/auth-login.html')


def log_out(request):
    logout(request)
    return redirect('log_in')


# -----------------Home-------------------------------
@login_required(login_url='log_in')
def home(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    products = models.Product.objects.all()
    enter_products = models.EnterProduct.objects.all()
    eport_products = models.ExportProduct.objects.all()

    if start_date and end_date:
        products = products.filter(created_at__range=[start_date, end_date])
        enter_products = enter_products.filter(created_at__range=[start_date, end_date])
        eport_products = eport_products.filter(created_at__range=[start_date, end_date])
    elif start_date:
        products = products.filter(created_at__gte=start_date)
        enter_products = enter_products.filter(created_at__gte=start_date)
        eport_products = eport_products.filter(created_at__gte=start_date)
    elif end_date:
        products = products.filter(created_at__lte=end_date)
        enter_products = enter_products.filter(created_at__lte=end_date)
        eport_products = eport_products.filter(created_at__lte=end_date)

    chiqim = 0
    kirim = 0

    enter_producs_quantity = 0
    export_producs_quantity = 0

    for product in products:
        chiqim += float(product.price) * int(product.quantity)

    for enter_product in enter_products:
        chiqim += float(enter_product.product.price) * int(enter_product.quantity)
        enter_producs_quantity += int(enter_product.quantity)

    for eport_product in eport_products:
        kirim += float(eport_product.product.price) * int(eport_product.quantity)
        export_producs_quantity += int(eport_product.quantity)

    context = {
        'kirim': kirim,
        'chiqim': chiqim,
        'export_producs_quantity': export_producs_quantity,
        'enter_producs_quantity': enter_producs_quantity,
    }

    return render(request, 'index.html', context)


# -----------------Category------------


@login_required(login_url='log_in')
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        category = models.Category.objects.create(
            name=name,
            image=image,
        )
        return redirect('category_list')

    return render(request, 'category/create.html')


@login_required(login_url='log_in')
def category_list(request):
    categories = models.Category.objects.all()
    return render(request, 'category/list.html', {'categories': categories})


@login_required(login_url='log_in')
def category_edit(request, id):
    category = models.Category.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if request.FILES.get('image'):
            image = request.FILES.get('image')
            category.image = image
        category.name = name
        category.save()
        return redirect('category_list')

    return render(request, 'category/edit.html', {'category': category})


@login_required(login_url='log_in')
def category_delete(request, id):
    category = models.Category.objects.get(id=id)
    category.delete()
    return redirect('category_list')


# ------------------------Product-----------------------------
@login_required(login_url='log_in')
def product_create(request):
    categories = models.Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        category = models.Category.objects.get(id=request.POST.get('category'))
        image = request.FILES.get('image')
        description = request.POST.get('description')
        price = request.POST.get('price').replace(',', '.')
        price = float(price)
        quantity = request.POST.get('quantity')
        product = models.Product.objects.create(
            name=name,
            category=category,
            image=image,
            description=description,
            price=price,
            quantity=quantity,
        )
        return redirect('product_list')

    return render(request, 'product/create.html', {'categories': categories})


@login_required(login_url='log_in')
def product_list(request):
    products = models.Product.objects.all()
    return render(request, 'product/list.html', {'products': products})


@login_required(login_url='log_in')
def product_detail(request, code):
    product = models.Product.objects.get(code=code)
    return render(request, 'product/detail.html', {'product': product})


@login_required(login_url='log_in')
def product_edit(request, code):
    product = models.Product.objects.get(code=code)
    context = {'product': product}
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        price = request.POST.get('price').replace(',', '.')
        product.price = price
        product.quantity = request.POST.get('quantity')
        if request.FILES.get('images'):
            product.image = request.FILES.get('images')
        product.save()
        return redirect('product_list')

    return render(request, 'product/edit.html', context)


@login_required(login_url='log_in')
def product_delete(request, code):
    product = models.Product.objects.get(code=code)
    product.delete()
    return redirect('product_list')


# -------------------------------EnterProduct--------------------------
@login_required(login_url='log_in')
def enter_product_create(request):
    products = models.Product.objects.all()
    if request.method == 'POST':
        product = models.Product.objects.get(code=request.POST.get('product'))
        quantity = request.POST.get('quantity')
        enter_product = models.EnterProduct.objects.create(
            product=product,
            quantity=quantity,
        )
        return redirect('enter_product_list')

    return render(request, 'enter_product/create.html', {'products': products})


@login_required(login_url='log_in')
def enter_product_list(request):
    enter_products = models.EnterProduct.objects.all()
    return render(request, 'enter_product/list.html', {'enter_products': enter_products})


@login_required(login_url='log_in')
def enter_product_edit(request, code):
    enter_product = models.EnterProduct.objects.get(code=code)
    context = {'export_product': enter_product}
    if request.method == 'POST':
        enter_product.quantity = request.POST.get('quantity')
        enter_product.save()
        return redirect('enter_product_list')

    return render(request, 'enter_product/edit.html', context)


# ------------------ExportProducts  --------------------------------
@login_required(login_url='log_in')
def export_product_create(request):
    products = models.Product.objects.all()
    if request.method == 'POST':
        product = models.Product.objects.get(code=request.POST.get('product'))
        quantity = request.POST.get('quantity')
        export_product = models.ExportProduct.objects.create(
            product=product,
            quantity=quantity,
        )
        return redirect('export_product_list')

    return render(request, 'export_product/create.html', {'products': products})


@login_required(login_url='log_in')
def export_product_list(request):
    export_products = models.ExportProduct.objects.all()
    return render(request, 'export_product/list.html', {'export_products': export_products})


@login_required(login_url='log_in')
def export_product_edit(request, code):
    export_product = models.ExportProduct.objects.get(code=code)
    context = {'export_product': export_product}
    if request.method == 'POST':
        export_product.quantity = request.POST.get('quantity')
        export_product.save()
        return redirect('export_product_list')

    return render(request, 'export_product/edit.html', context)


# ---------------- Return Product ------------------------

@login_required(login_url='log_in')
def return_product(request):
    products = models.ExportProduct.objects.all()
    if request.method == 'POST':
        product = models.ExportProduct.objects.get(code=request.POST.get('product'))
        quantity = request.POST.get('quantity')
        return_product = models.ReturnProduct.objects.create(
            product=product,
            quantity=quantity,
        )
        return redirect('return_product_list')

    return render(request, 'return_product/create.html', {'products': products})


@login_required(login_url='log_in')
def return_product_list(request):
    return_products = models.ReturnProduct.objects.all()
    return render(request, 'return_product/list.html', {'return_products': return_products})


@login_required(login_url='log_in')
def return_product_edit(request, code):
    return_product = models.ReturnProduct.objects.get(code=code)
    context = {'return_product': return_product}
    if request.method == 'POST':
        return_product.quantity = request.POST.get('quantity')
        return_product.save()
        return redirect('return_product_list')

    return render(request, 'return_product/edit.html', context)


# --------------QUERY----------------------------
@login_required(login_url='login')
def query(request):
    q = request.GET.get('q')
    products = models.Product.objects.filter(name__icontains=q)

    return render(request, 'query.html', {'products': products})
