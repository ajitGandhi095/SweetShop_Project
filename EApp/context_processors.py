from .models import *

def cart_count_processor(request):
    cart_count = 0
    try:
        user_id = request.session.get('user_id')
        if user_id:
            user = SignupModel.objects.get(id=user_id)
            cart_items = CartItemModel.objects.filter(user=user)
            cart_count = sum(item.quantity for item in cart_items)
    except:
        pass  # You can log errors here if needed

    return {'cart_count': cart_count}