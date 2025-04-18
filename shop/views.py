from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from .models import Category, Product, Order, OrderItem, ShippingAddress
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Sum
from django.urls import reverse
from decimal import Decimal
from django.http import JsonResponse

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(available=True)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)
        else:
            self.category = None
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = self.category
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    # Convert product_id to string since session stores keys as strings
    product_id = str(product_id)
    
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1,
            'image': product.image.url if product.image else None
        }
    
    request.session['cart'] = cart
    messages.success(request, f'{product.name} added to your cart.')
    return redirect('shop:cart_detail')

@login_required
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = Decimal('0.00')
    shipping_cost = Decimal('50.00')
    tax_rate = Decimal('0.18')
    
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = Decimal(str(item['price'])) * Decimal(str(item['quantity']))
        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'total': item_total
        })
        subtotal += item_total
    
    tax = subtotal * tax_rate
    total = subtotal + shipping_cost + tax
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'tax': tax,
        'total': total
    }
    return render(request, 'shop/cart_detail.html', context)

@login_required
def update_cart_quantity(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if product_id in cart:
            if quantity > 0:
                cart[product_id]['quantity'] = quantity
            else:
                del cart[product_id]
            
            request.session['cart'] = cart
            messages.success(request, 'Cart updated successfully.')
        else:
            messages.error(request, 'Product not found in cart.')
    
    return redirect('shop:cart_detail')

@login_required
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(product_id)
        
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            messages.success(request, 'Item removed from cart.')
        else:
            messages.error(request, 'Product not found in cart.')
    
    return redirect('shop:cart_detail')

class UserProfileView(LoginRequiredMixin, View):
    template_name = 'shop/profile.html'

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user).order_by('-created_at')
        
        # Calculate statistics
        total_orders = orders.count()
        completed_orders = orders.filter(status='completed').count()
        pending_orders = orders.filter(status='pending').count()
        total_spent = orders.filter(status='completed').aggregate(
            total=Sum('total')
        )['total'] or 0

        context = {
            'user': user,
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'pending_orders': pending_orders,
            'total_spent': total_spent,
            'orders': orders,
        }
        return render(request, self.template_name, context)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'shop/order_detail.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        # Ensure users can only view their own orders
        return Order.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        
        # Add order items to context
        context['order_items'] = order.items.all()
        
        # Add shipping address to context
        context['shipping_address'] = {
            'full_name': f"{order.first_name} {order.last_name}",
            'address': order.shipping_address,
            'phone': order.phone,
            'email': order.email
        }
        
        # Add order totals to context
        context['subtotal'] = order.subtotal
        context['shipping_cost'] = order.shipping_cost
        context['tax'] = order.tax
        context['total'] = order.total
        
        return context

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('shop:cart_detail')
    
    # Get user's saved addresses
    saved_addresses = ShippingAddress.objects.filter(user=request.user)
    default_address = saved_addresses.filter(is_default=True).first()
    
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pin_code = request.POST.get('pin_code')
        payment_method = request.POST.get('payment_method')
        save_address = request.POST.get('save_address') == 'on'
        make_default = request.POST.get('make_default') == 'on'

        # Save the address if requested
        if save_address:
            shipping_address = ShippingAddress.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                pin_code=pin_code,
                is_default=make_default
            )

        # Calculate order totals
        subtotal = Decimal('0.00')
        shipping_cost = Decimal('50.00')  # Fixed shipping cost
        tax_rate = Decimal('0.18')  # 18% tax

        # Create order
        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            shipping_address=f"{address}, {city}, {pin_code}",
            payment_method=payment_method,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax=Decimal('0.00'),
            total=Decimal('0.00')
        )

        # Add order items
        for product_id, item in cart.items():
            product = get_object_or_404(Product, id=product_id)
            price = Decimal(str(item['price']))
            quantity = int(item['quantity'])
            item_total = price * Decimal(str(quantity))
            subtotal += item_total

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )

        # Update order totals
        tax = subtotal * tax_rate
        total = subtotal + shipping_cost + tax

        order.subtotal = subtotal
        order.tax = tax
        order.total = total
        order.save()

        # Clear cart
        request.session['cart'] = {}

        # Redirect to order confirmation
        return redirect('shop:order_confirmation', order_id=order.id)

    # Get cart items for display
    cart_items = []
    subtotal = Decimal('0.00')
    shipping_cost = Decimal('50.00')
    tax_rate = Decimal('0.18')

    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        price = Decimal(str(item['price']))
        quantity = int(item['quantity'])
        item_total = price * Decimal(str(quantity))
        subtotal += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total
        })

    tax = subtotal * tax_rate
    total = subtotal + shipping_cost + tax

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'tax': tax,
        'total': total,
        'saved_addresses': saved_addresses,
        'default_address': default_address
    }
    return render(request, 'shop/checkout.html', context)

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Parse the shipping address string into components
    address_parts = order.shipping_address.split(', ')
    street_address = address_parts[0] if len(address_parts) > 0 else ''
    city = address_parts[1] if len(address_parts) > 1 else ''
    state_zip = address_parts[2] if len(address_parts) > 2 else ''
    
    # Split state and zip if they exist
    state = ''
    zip_code = ''
    if state_zip:
        state_zip_parts = state_zip.split(' ')
        state = state_zip_parts[0] if len(state_zip_parts) > 0 else ''
        zip_code = state_zip_parts[1] if len(state_zip_parts) > 1 else ''
    
    context = {
        'order': order,
        'shipping_address': {
            'full_name': f"{order.first_name} {order.last_name}",
            'street_address': street_address,
            'city': city,
            'state': state,
            'zip': zip_code,
            'phone': order.phone,
            'email': order.email
        }
    }
    return render(request, 'shop/order_confirmation.html', context)

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Only allow cancellation of pending orders
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order #{order.id} has been cancelled.')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    
    return redirect('shop:user_profile')

@login_required
def get_address(request, address_id):
    address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
    data = {
        'first_name': address.first_name,
        'last_name': address.last_name,
        'email': address.email,
        'phone': address.phone,
        'address': address.address,
        'city': address.city,
        'pin_code': address.pin_code
    }
    return JsonResponse(data)
