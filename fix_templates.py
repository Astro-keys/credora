import os
import re

# Directory containing templates
templates_dir = r'C:\Users\EMINS\Desktop\work\credora\credora_bank\templates'

def fix_template(file_path):
    """Fix escaped quotes in Django template tags"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix {% static \'...\' %} to {% static '...' %}
    content = re.sub(r"{% static \\'(.+?)\\' %}", r"{% static '\1' %}", content)
    
    # Fix {% url \'...\' %} to {% url '...' %}
    content = re.sub(r"{% url \\'(.+?)\\' %}", r"{% url '\1' %}", content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

# Process all HTML files recursively
fixed_count = 0
for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            try:
                if fix_template(file_path):
                    fixed_count += 1
                    print(f'Fixed: {file}')
            except Exception as e:
                print(f'Error fixing {file}: {e}')

print(f'\nTotal files fixed: {fixed_count}')
