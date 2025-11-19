import os
import re

templates_dir = r'C:\Users\EMINS\Desktop\work\credora\credora_bank\templates'

fallback_script = """
<script>
// Fallback to hide preloader if jQuery doesn't load
window.addEventListener('load', function() {
    var preloader = document.getElementById('preloader-container');
    if (preloader) {
        setTimeout(function() {
            preloader.style.display = 'none';
        }, 500);
    }
});
</script>
"""

def add_preloader_fallback(file_path):
    """Add fallback script to hide preloader after the preloader div"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if fallback already exists
    if "var preloader = document.getElementById('preloader-container')" in content:
        return False
    
    # Check if preloader exists
    if 'id="preloader-container"' not in content:
        return False
    
    # Find the closing </div> of preloader-container
    pattern = r'(<div id="preloader-container">.*?</div>\s*</div>)'
    
    def replacement(match):
        return match.group(1) + fallback_script
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL, count=1)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

# Process all HTML files
fixed_count = 0
for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            try:
                if add_preloader_fallback(file_path):
                    fixed_count += 1
                    print(f'Fixed: {file}')
            except Exception as e:
                print(f'Error fixing {file}: {e}')

print(f'\nTotal files fixed: {fixed_count}')
