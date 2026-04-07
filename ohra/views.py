import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Product


# ─── PUBLIC STOREFRONT ───────────────────────────────────────────────────────

def storefront(request):
    products = Product.objects.filter(is_active=True).order_by('order', 'name')
    return render(request, 'ohra/store.html', {'products': products})


# ─── AUTH ────────────────────────────────────────────────────────────────────

def admin_login(request):
    error = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_panel')
        error = 'Invalid credentials or not a staff account.'
    return render(request, 'ohra/login.html', {'error': error})


def admin_logout(request):
    logout(request)
    return redirect('storefront')


# ─── ADMIN PANEL ─────────────────────────────────────────────────────────────

@login_required
def admin_panel(request):
    products = Product.objects.all().order_by('order', 'name')
    return render(request, 'ohra/admin.html', {'products': products})


# ─── REST API (called by JavaScript in admin panel) ──────────────────────────

@login_required
@require_http_methods(['POST'])
def api_product_create(request):
    """Create a new product."""
    try:
        p = Product(
            name    = request.POST.get('name', '').strip(),
            brand   = request.POST.get('brand', 'Lattafa').strip(),
            notes   = request.POST.get('notes', '').strip(),
            price   = float(request.POST.get('price', 0)),
            badge   = request.POST.get('badge', '').strip(),
            accent  = request.POST.get('accent', 'ac-gold'),
            order   = int(request.POST.get('order', 0)),
            is_active = request.POST.get('is_active', 'true') == 'true',
        )
        if 'image' in request.FILES:
            p.image = request.FILES['image']
        p.save()
        return JsonResponse({'success': True, 'id': p.id, 'message': f'{p.name} added!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_http_methods(['GET', 'POST', 'DELETE'])
def api_product_detail(request, pk):
    """Get, update or delete a single product."""
    p = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        return JsonResponse({
            'id':        p.id,
            'name':      p.name,
            'brand':     p.brand,
            'notes':     p.notes,
            'price':     str(p.price),
            'badge':     p.badge,
            'accent':    p.accent,
            'order':     p.order,
            'is_active': p.is_active,
            'image_url': p.image.url if p.image else '',
        })

    if request.method == 'POST':
        p.name      = request.POST.get('name', p.name).strip()
        p.brand     = request.POST.get('brand', p.brand).strip()
        p.notes     = request.POST.get('notes', p.notes).strip()
        p.price     = float(request.POST.get('price', p.price))
        p.badge     = request.POST.get('badge', p.badge).strip()
        p.accent    = request.POST.get('accent', p.accent)
        p.order     = int(request.POST.get('order', p.order))
        p.is_active = request.POST.get('is_active', 'true') == 'true'
        if 'image' in request.FILES:
            p.image = request.FILES['image']
        p.save()
        return JsonResponse({'success': True, 'message': f'{p.name} updated!'})

    if request.method == 'DELETE':
        name = p.name
        p.delete()
        return JsonResponse({'success': True, 'message': f'{name} deleted.'})


@login_required
def api_products_list(request):
    """Return all products as JSON."""
    products = Product.objects.all().order_by('order', 'name')
    data = [{
        'id':        p.id,
        'name':      p.name,
        'brand':     p.brand,
        'notes':     p.notes,
        'price':     str(p.price),
        'badge':     p.badge,
        'accent':    p.accent,
        'order':     p.order,
        'is_active': p.is_active,
        'image_url': p.image.url if p.image else '',
    } for p in products]
    return JsonResponse({'products': data})
