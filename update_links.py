import os
import re

base_path = r'C:\Users\DELL\.accio\accounts\7084465040\agents\DID-F456DA-2B0D4C\project/winningstar-repo'

# 1. Update index.html Product Categories
index_path = os.path.join(base_path, 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

index_replacements = {
    'href="products.html#kitchen"': 'href="air-fryer.html"',
    'href="products.html#home"': 'href="vacuum.html"',
    'href="products.html#personal"': 'href="hair-clipper.html"',
    'href="products.html#kitchenware"': 'href="pan.html"',
    'href="products.html#others"': 'href="stabilizer.html"'
}

for old, new in index_replacements.items():
    index_content = index_content.replace(old, new)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_content)

# 2. Update products.html category cards
products_path = os.path.join(base_path, 'products.html')
with open(products_path, 'r', encoding='utf-8') as f:
    products_content = f.read()

# Define category mapping for products.html
# We'll use a regex to find each card and wrap the image and title.
category_links = {
    "Air Fryer": "air-fryer.html",
    "Blender & Juicer": "blender.html",
    "Electric Kettle": "kettle.html",
    "Rice Cooker": "rice-cooker.html",
    "Vacuum Cleaner": "vacuum.html",
    "Electric Fan": "fan.html",
    "Electric Iron": "iron.html",
    "Refrigerator": "refrigerator.html",
    "Hair Clipper": "hair-clipper.html",
    "Hair Dryer": "hair-dryer.html",
    "Nonstick Pan": "pan.html",
    "Voltage Stabilizer": "stabilizer.html"
}

for name, link in category_links.items():
    # Wrap image
    # Original: <img src="placeholder-product.jpg" alt="" class="w-full h-full object-cover group-hover:scale-110 transition duration-700">
    # New: <a href="link"><img ...></a>
    
    # Since all cards look the same, we need to be careful.
    # We find the block containing the name first.
    
    pattern = rf'(<div class="bg-white rounded-3xl.*?<img src="placeholder-product\.jpg" alt="" class="w-full h-full object-cover group-hover:scale-110 transition duration-700">.*?<h3 class="font-bold text-lg mb-4 text-gray-800">{name}</h3>)'
    
    def wrap_card(match):
        block = match.group(1)
        # Wrap image
        block = block.replace('<img src="placeholder-product.jpg"', f'<a href="{link}"><img src="placeholder-product.jpg"')
        block = block.replace('duration-700">', f'duration-700"></a>')
        # Wrap title
        block = block.replace(f'<h3 class="font-bold text-lg mb-4 text-gray-800">{name}</h3>', f'<a href="{link}"><h3 class="font-bold text-lg mb-4 text-gray-800 hover:text-teal-600 transition">{name}</h3></a>')
        # Update button
        # Original: <a href="..." class="...">Inquiry Now</a>
        # New: <a href="link" class="...">View All</a>
        
        # Use regex to find the inquiry/view all button
        block = re.sub(r'<a href="[^"]+" class="inline-block w-full py-3 rounded-xl bg-gray-900 text-white text-sm font-bold hover:bg-teal-600 transition-colors uppercase tracking-wider">.*?</a>', 
                       f'<a href="{link}" class="inline-block w-full py-3 rounded-xl bg-gray-900 text-white text-sm font-bold hover:bg-teal-600 transition-colors uppercase tracking-wider">View All</a>', 
                       block)
        return block

    products_content = re.sub(pattern, wrap_card, products_content, flags=re.DOTALL)

with open(products_path, 'w', encoding='utf-8') as f:
    f.write(products_content)

print("index.html and products.html links updated successfully.")
