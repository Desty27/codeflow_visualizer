import os
import sys
from dotenv import load_dotenv
from src.utils import clone_repository, get_code_structure
from src.analyzer import generate_artifacts, parse_ai_response, save_artifacts
from src.mermaid_renderer import find_mmdc

def check_environment():
    """Verify all required tools are available"""
    print("🔍 Checking environment...")
    
    # Check Node.js/mmdc
    mmdc_path = find_mmdc()
    if mmdc_path:
        print(f"✅ Found mmdc at: {mmdc_path}")
    else:
        print("❌ mmdc not found - diagrams will be limited")
        print("Please install with: npm install -g @mermaid-js/mermaid-cli")
    
    # Check Python dependencies
    try:
        import openai
        import git
        print("✅ Python dependencies OK")
    except ImportError as e:
        print(f"❌ Missing Python package: {str(e)}")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)

def main():
    load_dotenv()
    check_environment()
    
    try:
        repo_url = "https://github.com/megadose/holehe.git"
        
        print("\n🔍 Analyzing repository...")
        repo_path = clone_repository(repo_url)
        code_structure = get_code_structure(repo_path)
        
        print("\n🤖 Generating documentation artifacts...")
        ai_response = generate_artifacts(code_structure)
        artifacts = parse_ai_response(ai_response)
        
        print("\n💾 Saving outputs...")
        output_paths = save_artifacts(artifacts)
        
        print("\n✅ Analysis complete!")
        print("\n📄 Output files:")
        print(f"- Project report: {output_paths['report']}")
        print(f"- High-level diagram: {output_paths['high_level_svg']}")
        print(f"- Code-level diagram: {output_paths['code_level_svg']}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()