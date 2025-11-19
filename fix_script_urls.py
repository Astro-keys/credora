import os
import re

templates_dir = r'C:\Users\EMINS\Desktop\work\credora\credora_bank\templates'

def fix_script_urls(file_path):
    """Remove query parameters from static script URLs"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix script.js?v=1.0.1
    content = re.sub(r"src/js/script\.js\?v=\d+\.\d+\.\d+", "src/js/script.js", content)
    
    # Fix transfer.js?v=1.0.1
    content = re.sub(r"src/js/transfer\.js\?v=\d+\.\d+\.\d+", "src/js/transfer.js", content)
    
    # Fix datetime.js if it has query params
    content = re.sub(r"src/js/datetime\.js\?v=\d+\.\d+\.\d+", "src/js/datetime.js", content)
    
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
                if fix_script_urls(file_path):
                    fixed_count += 1
                    print(f'Fixed: {file}')
            except Exception as e:
                print(f'Error fixing {file}: {e}')

print(f'\nTotal files fixed: {fixed_count}')
