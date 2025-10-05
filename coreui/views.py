from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'index.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Hardcode data tĩnh cho New Arrivals (4 items, dạng dict như atomic components)
        context['new_arrivals_items'] = [
            {
                'image': 'images/T-shirt-with-Tape-Details.png',  
                'name': 'T-shirt with Tape Details',
                'stars': '★★★★★',
                'score': '4.5/5',
                'current_price': 120,
                'original_price': None,
                'discount': None,
            },
            {
                'image': 'images/Skinny-Fit-Jeans.png',
                'name': 'Skinny Fit Jeans',
                'stars': '★★★',
                'score': '3.5/5',
                'current_price': 240,
                'original_price': 260,
                'discount': '-20%',
            },
            {
                'image': 'images/Checkered-Shirt.png',
                'name': 'Checkered Shirt',
                'stars': '★★★★',
                'score': '4.5/5',
                'current_price': 180,
                'original_price': None,
                'discount': None,
            },
            {
                'image': 'images/Sleeve-Striped-T-shirt.png',
                'name': 'Sleeve Striped T-shirt',
                'stars': '★★★★',
                'score': '4.5/5',
                'current_price': 130,
                'original_price': 160,
                'discount': '-30%',
            },
        ]
        context['top_selling_items'] = [
            {
                'image': 'images/Vertical-striped-shirt.png',
                'name': 'Vertical Striped Shirt',
                'stars': '★★★★★',
                'score': '5.0/5',
                'current_price': 212,
                'original_price': 232,
                'discount': '-20%',
            },
            {
                'image': 'images/Courage-graphic-t-shirt.png',
                'name': 'Courage Graphic T-shirt',
                'stars': '★★★★',
                'score': '4.0/5',
                'current_price': 145,
                'original_price': None,
                'discount': None,
            },
            {
                'image': 'images/Loose-fit-bermuda-shorts.png',
                'name': 'Loose Fit Bermuda Shorts',
                'stars': '★★★',
                'score': '3.0/5',
                'current_price': 80,
                'original_price': None,
                'discount': None,
            },
            {
                'image': 'images/Faded-skinny-jeans.png',
                'name': 'Faded Skinny Jeans',
                'stars': '★★★★★',
                'score': '4.5/5',
                'current_price': 210,
                'original_price': None,
                'discount': None,
            },
        ]
        return context