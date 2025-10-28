#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from Category.models import Category, Product

def create_superuser():
    """Создание суперпользователя"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✅ Суперпользователь 'admin' создан (пароль: admin123)")
    else:
        print("ℹ️ Суперпользователь 'admin' уже существует")

def create_categories():
    """Создание категорий"""
    categories_data = [
        {'name': 'Краски', 'slug': 'kraski', 'description': 'Краски для внутренних и наружных работ'},
        {'name': 'Растворители', 'slug': 'rastvoriteli', 'description': 'Растворители и разбавители'},
        {'name': 'Товары для дома', 'slug': 'tovary-dlya-doma', 'description': 'Товары для дома и быта'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description']
            }
        )
        if created:
            print(f"✅ Категория '{category.name}' создана")
        else:
            print(f"ℹ️ Категория '{category.name}' уже существует")
    
    return Category.objects.all()

def create_products():
    """Создание товаров"""
    categories = Category.objects.all()
    
    if not categories.exists():
        print("❌ Сначала создайте категории!")
        return
    
    products_data = [
        # Краски
        {
            'name': 'Краска акриловая белая',
            'description': 'Высококачественная акриловая краска для внутренних работ',
            'price': 1250.00,
            'stock': 50,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Краска фасадная',
            'description': 'Устойчивая к погодным условиям фасадная краска',
            'price': 1850.00,
            'stock': 30,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Краска латексная влагостойкая',
            'description': 'Влагостойкая латексная краска для ванных комнат',
            'price': 2100.00,
            'stock': 25,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Краска масляная МА-15',
            'description': 'Масляная краска для металлических поверхностей',
            'price': 950.00,
            'stock': 40,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Краска металлик',
            'description': 'Краска с металлическим эффектом',
            'price': 1650.00,
            'stock': 20,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Краска моющаяся',
            'description': 'Моющаяся краска для детских комнат',
            'price': 1950.00,
            'stock': 35,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Краска для пола',
            'description': 'Износостойкая краска для деревянных полов',
            'price': 2200.00,
            'stock': 15,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Краска для радиаторов',
            'description': 'Термостойкая краска для отопительных приборов',
            'price': 1400.00,
            'stock': 28,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Краска резиновая',
            'description': 'Эластичная резиновая краска для крыш',
            'price': 2750.00,
            'stock': 12,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Краска супербелая',
            'description': 'Ослепительно белая краска с высокой укрывистостью',
            'price': 1550.00,
            'stock': 45,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Эмаль аэрозоль черная',
            'description': 'Аэрозольная эмаль для мелких работ',
            'price': 350.00,
            'stock': 60,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Эмаль НЦ-132',
            'description': 'Нитроцеллюлозная эмаль для внутренних работ',
            'price': 850.00,
            'stock': 30,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Эмаль ПФ-115 синяя',
            'description': 'Пентафталевая эмаль для наружных работ',
            'price': 1200.00,
            'stock': 25,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Эмаль ПФ-266 пол',
            'description': 'Эмаль для окраски полов',
            'price': 1800.00,
            'stock': 18,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Грунт-эмаль 3в1',
            'description': 'Универсальная грунт-эмаль',
            'price': 1450.00,
            'stock': 22,
            'category_slug': 'kraski',
            'image': 'product-image.jpg'
        },
        {
            'name': 'Краска без изображения',
            'description': 'Пример товара без картинки для демонстрации',
            'price': 999.00,
            'stock': 10,
            'category_slug': 'kraski',
            'image': None
        },
        
        # Растворители
        {
            'name': 'Растворитель 646',
            'description': 'Универсальный растворитель для красок',
            'price': 450.00,
            'stock': 80,
            'category_slug': 'rastvoriteli',
            'image': 'product-image2.jpg'
        },
        {
            'name': 'Растворитель 650',
            'description': 'Растворитель для эмалей и лаков',
            'price': 520.00,
            'stock': 65,
            'category_slug': 'rastvoriteli',
            'image': 'product-image2.jpg'
        },
        {
            'name': 'Растворитель Р-4',
            'description': 'Растворитель для перхлорвиниловых красок',
            'price': 480.00,
            'stock': 70,
            'category_slug': 'rastvoriteli',
            'image': 'product-image2.jpg'
        },
        {
            'name': 'Ацетон',
            'description': 'Чистый ацетон для обезжиривания',
            'price': 380.00,
            'stock': 90,
            'category_slug': 'rastvoriteli',
            'image': 'product-image2.jpg'
        },
        {
            'name': 'Уайт-спирит',
            'description': 'Уайт-спирит для разбавления масляных красок',
            'price': 420.00,
            'stock': 75,
            'category_slug': 'rastvoriteli',
            'image': 'product-image2.jpg'
        },
        {
            'name': 'Сольвент',
            'description': 'Сольвент для разбавления красок',
            'price': 400.00,
            'stock': 85,
            'category_slug': 'rastvoriteli',
            'image': 'product-image2.jpg'
        },
        {
            'name': 'Растворитель без изображения',
            'description': 'Пример товара без картинки для демонстрации',
            'price': 299.00,
            'stock': 15,
            'category_slug': 'rastvoriteli',
            'image': None
        },
        
        # Товары для дома
        {
            'name': 'Наждачная бумага',
            'description': 'Наждачная бумага разной зернистости',
            'price': 150.00,
            'stock': 100,
            'category_slug': 'tovary-dlya-doma',
            'image': 'product-image1.jpg'
        },
        {
            'name': 'Перчатки рабочие',
            'description': 'Защитные перчатки для малярных работ',
            'price': 200.00,
            'stock': 120,
            'category_slug': 'tovary-dlya-doma',
            'image': 'product-image1.jpg'
        },
        {
            'name': 'Пленка защитная',
            'description': 'Полиэтиленовая пленка для защиты поверхностей',
            'price': 300.00,
            'stock': 80,
            'category_slug': 'tovary-dlya-doma',
            'image': 'product-image1.jpg'
        },
        {
            'name': 'Респиратор',
            'description': 'Защитный респиратор от паров краски',
            'price': 800.00,
            'stock': 50,
            'category_slug': 'tovary-dlya-doma',
            'image': 'product-image1.jpg'
        },
        {
            'name': 'Шпатель',
            'description': 'Металлический шпатель для шпаклевки',
            'price': 250.00,
            'stock': 60,
            'category_slug': 'tovary-dlya-doma',
            'image': 'product-image1.jpg'
        },
        {
            'name': 'Ведро пластиковое',
            'description': 'Ведро для разведения красок',
            'price': 180.00,
            'stock': 90,
            'category_slug': 'tovary-dlya-doma',
            'image': 'product-image1.jpg'
        },
        {
            'name': 'Товар без изображения',
            'description': 'Пример товара без картинки для демонстрации',
            'price': 199.00,
            'stock': 25,
            'category_slug': 'tovary-dlya-doma',
            'image': None
        },
    ]
    
    for prod_data in products_data:
        try:
            category = Category.objects.get(slug=prod_data['category_slug'])
            
            # Подготовка данных для создания товара
            product_data = {
                'description': prod_data['description'],
                'price': prod_data['price'],
                'stock': prod_data['stock'],
                'category': category,
            }
            
            # Добавляем изображение только если оно указано
            if prod_data['image'] is not None:
                product_data['image'] = f'products/{prod_data["image"]}'
            
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults=product_data
            )
            if created:
                print(f"✅ Товар '{product.name}' создан")
            else:
                print(f"ℹ️ Товар '{product.name}' уже существует")
        except Category.DoesNotExist:
            print(f"❌ Категория с slug '{prod_data['category_slug']}' не найдена")

def main():
    print("🚀 Начинаем настройку данных...")
    print()
    
    create_superuser()
    print()
    
    create_categories()
    print()
    
    create_products()
    print()
    
    print("✅ Настройка данных завершена!")
    print()
    print("📊 Статистика:")
    print(f"   👤 Пользователей: {User.objects.count()}")
    print(f"   📂 Категорий: {Category.objects.count()}")
    print(f"   📦 Товаров: {Product.objects.count()}")

if __name__ == '__main__':
    main()
