import os
import re

templates_dir = r'C:\Users\EMINS\Desktop\work\credora\credora_bank\templates'

def fix_inline_bg_images(file_path):
    """Convert inline Tailwind bg-[url(...)] to style attribute with Django static tag"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern to match bg-[url('/src/images/...')] 
    pattern = r"bg-\[url\('(/src/images/[^']+)'\)\]"
    
    def replace_bg_url(match):
        full_match = match.group(0)
        image_path = match.group(1)
        # Remove the leading slash and 'src/' to get relative path from static root
        relative_path = image_path.lstrip('/')
        return f"bg-[url('{{% static '{relative_path}' %}}')]"
    
    # Replace all occurrences
    content = re.sub(pattern, replace_bg_url, content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Process all HTML files
fixed_count = 0
for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            try:
                if fix_inline_bg_images(file_path):
                    fixed_count += 1
                    print(f'Fixed: {file}')
            except Exception as e:
                print(f'Error fixing {file}: {e}')

print(f'\nTotal files fixed: {fixed_count}')
