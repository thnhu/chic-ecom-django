# from django.views.generic import ListView
# from .models import Product, ProductVariant, Image

# class ProductListView(ListView):
#     model = Product
#     template_name = 'products/product_list.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
#         top_selling = Product.objects.filter(is_active=True).order_by('-total_quantity')[:4]

#         def prepare_product_data(products):
#             items = []
#             for product in products:
#                 variant = ProductVariant.objects.filter(product=product).first()
#                 image = Image.objects.filter(product=product, is_primary=True).first()
#                 if variant and image:
#                     discount = round((product.base_price - variant.price) / product.base_price * 100, 0) if product.base_price > variant.price else None
#                     items.append({
#                         'image': image.image.url,
#                         'name': product.name,
#                         'stars': '★★★★★',
#                         'score': '4.5/5', 
#                         'current_price': variant.price,
#                         'original_price': product.base_price if discount else None,
#                         'discount': f'-{discount}%' if discount else None,
#                     })
#             return items

#         context['new_arrivals_items'] = prepare_product_data(new_arrivals)
#         context['top_selling_items'] = prepare_product_data(top_selling)
#         return context