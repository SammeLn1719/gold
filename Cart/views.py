from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Category.models import Product
from .cart import Cart

@login_required
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))

        if quantity < 1:
            messages.error(request, 'Количество должно быть больше 0')
            return redirect('category:product_detail', pk=product_id)

        cart.add(product=product, quantity=quantity)
        messages.success(request, f'✓ "{product.name}" добавлен в корзину')

    except (ValueError, TypeError):
        messages.error(request, 'Неверное количество товара')
        return redirect('category:product_detail', pk=product_id)

    return redirect('cart:cart_detail')

@login_required
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    messages.success(request, f'✓ "{product.name}" удален из корзины')

    return redirect('cart:cart_detail')

@login_required
@require_POST
def cart_update(request, product_id):
    cart = Cart(request)

    try:
        quantity = int(request.POST.get('quantity', 1))

        if quantity < 1:
            messages.warning(request, 'Количество должно быть больше 0')
            return redirect('cart:cart_detail')

        cart.update_quantity(product_id, quantity)
        messages.success(request, '✓ Количество обновлено')

    except (ValueError, TypeError):
        messages.error(request, 'Неверное количество товара')

    return redirect('cart:cart_detail')

@login_required
def cart_detail(request):
    cart = Cart(request)

    cart_items_with_warnings = []
    has_warnings = False

    for item in cart:
        item_data = {
            'item': item,
            'has_warning': False,
            'warning_message': ''
        }

        if item['quantity'] > item['product'].stock:
            item_data['has_warning'] = True
            item_data['warning_message'] = f"На складе только {item['product'].stock} шт. Количество будет скорректировано при оформлении."
            has_warnings = True

        elif item['product'].stock == 0:
            item_data['has_warning'] = True
            item_data['warning_message'] = "Товар закончился на складе. Он будет удален при оформлении."
            has_warnings = True

        cart_items_with_warnings.append(item_data)

    return render(request, 'cart/detail.html', {
        'cart': cart,
        'cart_items_with_warnings': cart_items_with_warnings,
        'has_warnings': has_warnings
    })
