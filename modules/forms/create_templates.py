from .models import FormTemplate

def create_templates():
    template1 = FormTemplate(name="Order Form", email="email", phone="phone", order_date="date")
    template1.save()

    template2 = FormTemplate(name="User Registration", email="email", user_name="text", birth_date="date")
    template2.save()

    print("Templates created successfully!")
