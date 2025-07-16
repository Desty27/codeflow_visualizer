import os
import re
from openai import AzureOpenAI
from .mermaid_renderer import render_diagram

def generate_artifacts(code_structure):
    """Send code structure to Azure OpenAI"""
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2023-12-01-preview"
    )
    
    # Create a code summary that fits within token limits
    code_summary = "\n".join(
        f"### {path}\n```python\n{content[:1000]}\n...\n```" 
        for path, content in list(code_structure.items())[:5]  # Only first 5 files
    )
    
    prompt = f"""
    Analyze the codebase and generate exactly three artifacts:
    
    1. PROJECT REPORT in markdown format
    2. HIGH-LEVEL FLOWCHART in Mermaid syntax
    3. CODE-LEVEL FLOWCHART in Mermaid syntax for the main module
    
    Important: 
    - Mermaid diagrams MUST start with 'graph TD' or 'graph TB'
    - Diagrams MUST be complete and valid
    - Do NOT include markdown code fences (```) in diagrams
    
    Code Structure Summary:
    {str(list(code_structure.keys()))}
    
    Selected Code Contents:
    {code_summary}
    
    Format your response EXACTLY as:
    [PROJECT REPORT]
    ... (markdown content here) ...
    [HIGH-LEVEL FLOWCHART]
    graph TD
    ... (mermaid diagram here) ...
    [CODE-LEVEL FLOWCHART]
    graph TB
    ... (mermaid diagram here) ...
    """
    
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[
            {
                "role": "system", 
                "content": "You are a senior software architect. Generate complete, valid technical documentation."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=4000
    )
    
    return response.choices[0].message.content

def parse_ai_response(response):
    """Extract components from AI response with robust patterns"""
    components = {
        "report": "",
        "high_level_chart": "",
        "code_level_chart": "",
        "raw_response": response  # Keep for debugging
    }
    
    # Improved extraction patterns
    patterns = {
        "report": r"\[PROJECT REPORT\](.*?)(?=\[HIGH-LEVEL FLOWCHART\]|\Z)",
        "high_level_chart": r"\[HIGH-LEVEL FLOWCHART\][\s]*(graph\s+TD[\s\S]*?)(?=\[CODE-LEVEL FLOWCHART\]|\Z)",
        "code_level_chart": r"\[CODE-LEVEL FLOWCHART\][\s]*(graph\s+TB[\s\S]*?)(?=\Z)"
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
        if match:
            content = match.group(1).strip()
            # Clean up any markdown code blocks
            content = re.sub(r"```mermaid\s*", "", content)
            content = re.sub(r"```\s*$", "", content)
            components[key] = content
    
    return components

def save_artifacts(components, output_dir="outputs"):
    """Save generated artifacts to files"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save raw response for debugging
    with open(os.path.join(output_dir, "raw_ai_response.txt"), "w") as f:
        f.write(components["raw_response"])
    
    # Save markdown report
    report_path = os.path.join(output_dir, "project_report.md")
    with open(report_path, "w") as f:
        f.write(components["report"] or "# Error: Report not generated")
    
    # Process and render diagrams
    output_paths = {}
    for diagram_type in ["high_level", "code_level"]:
        key = f"{diagram_type}_chart"
        mmd_path = os.path.join(output_dir, f"{diagram_type}_flowchart.mmd")
        svg_path = os.path.join(output_dir, f"{diagram_type}_flowchart.svg")
        
        content = components[key]
        output_paths[key] = svg_path
        
        # Save Mermaid source
        with open(mmd_path, "w") as f:
            f.write(content or f"# Error: {diagram_type} diagram not generated")
        
        # Render SVG if we have valid content
        if content and content.startswith("graph"):
            render_diagram(content, svg_path)
        else:
            print(f"⚠️ Invalid Mermaid content for {diagram_type}")
    
    # Embed SVGs in markdown report
    if os.path.exists(output_paths["high_level_chart"]):
        with open(report_path, "a") as f:
            f.write("\n\n## Architecture Diagrams\n")
            f.write(f"### High-Level Flow\n![]({output_paths['high_level_chart']})\n\n")
            
            if os.path.exists(output_paths["code_level_chart"]):
                f.write(f"### Code-Level Flow\n![]({output_paths['code_level_chart']})")
    
    print(f"📁 Artifacts saved to {output_dir}/")
    return {
        "report": report_path,
        "high_level_svg": output_paths["high_level_chart"],
        "code_level_svg": output_paths["code_level_chart"]
    }