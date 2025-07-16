import os
import subprocess
import tempfile
import shutil
from pathlib import Path

def find_mmdc():
    """Locate mmdc executable with multiple fallback options"""
    # Check standard global install location
    mmdc_path = shutil.which('mmdc')
    if mmdc_path:
        return mmdc_path
    
    # Check common Node.js global install locations
    common_paths = [
        os.path.expanduser('~/.npm-global/bin/mmdc'),
        os.path.expanduser('~/.nvm/versions/node/*/bin/mmdc'),
        os.path.expanduser('~/AppData/Roaming/npm/mmdc.cmd'),  # Windows
        '/usr/local/bin/mmdc',  # Linux/Mac
        '/opt/homebrew/bin/mmdc'  # Mac ARM
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

def render_local_mermaid(mermaid_code, output_path):
    """Render Mermaid using local mmdc with improved path handling"""
    try:
        mmdc_path = find_mmdc()
        if not mmdc_path:
            print("❌ mmdc not found in PATH or common locations")
            print("💡 Try these solutions:")
            print("1. Restart your terminal/IDE after npm install")
            print("2. Add Node.js to system PATH")
            print("3. Reinstall with: npm install -g @mermaid-js/mermaid-cli")
            return False
        
        # Create temporary .mmd file
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".mmd", delete=False) as temp:
            temp.write(mermaid_code)
            temp_path = temp.name
        
        # Run mmdc command with full path
        cmd = [
            mmdc_path,
            "-i", temp_path,
            "-o", output_path,
            "-b", "transparent",
            "-t", "forest",
            "-w", "1200",
            "-H", "800"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True if os.name == 'nt' else False
        )
        
        # Clean up
        os.unlink(temp_path)
        
        if result.returncode == 0:
            print(f"✅ Diagram rendered to {output_path}")
            return True
        else:
            print(f"❌ mmdc failed with error:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"⚠️ Local rendering error: {str(e)}")
        return False

def render_diagram(mermaid_code, output_path):
    """Main rendering function with fallback to basic SVG"""
    if not mermaid_code.strip():
        print("⚠️ Empty Mermaid code - skipping diagram")
        return False
    
    print(f"\n🔄 Rendering {os.path.basename(output_path)}...")
    
    # First try local rendering
    if render_local_mermaid(mermaid_code, output_path):
        return True
    
    # Fallback: Create basic SVG with error message
    print("⚠️ Creating placeholder SVG with Mermaid code")
    svg_content = f"""<svg width="1200" height="800" xmlns="http://www.w3.org/2000/svg">
        <style>
            .error {{ font-family: Arial; font-size: 14px; fill: red; }}
            .code {{ font-family: Consolas; font-size: 12px; fill: #333; }}
        </style>
        <rect width="100%" height="100%" fill="#f9f9f9" rx="5" ry="5"/>
        <text x="20" y="30" class="error">⚠️ Diagram Rendering Failed</text>
        <text x="20" y="60" class="error">Please install mmdc: npm install -g @mermaid-js/mermaid-cli</text>
        <foreignObject x="20" y="80" width="1160" height="700">
            <div xmlns="http://www.w3.org/1999/xhtml" style="
                font-family: Consolas;
                font-size: 12px;
                white-space: pre;
                background: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                overflow: auto;
                height: 100%;
            ">
                {mermaid_code.replace('<', '&lt;').replace('>', '&gt;')}
            </div>
        </foreignObject>
    </svg>"""
    
    with open(output_path, "w") as f:
        f.write(svg_content)
    
    return True