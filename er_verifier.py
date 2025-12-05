"""
ER Diagram to PlantUML Verifier
Analyzes an incomplete ER diagram image and generates complete PlantUML code.
"""

import base64
import sys
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()


# Configuration
IMAGES_DIR = Path("data/images")
DESCRIPTIONS_DIR = Path("data/system_descriptions")
PROMPT_FILE = Path("prompt.md")
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg"}


def get_mime_type(image_path: Path) -> str:
    """Get the MIME type for an image file."""
    extension = image_path.suffix.lower()
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".svg": "image/svg+xml",
    }
    return mime_types.get(extension, "image/jpeg")


def encode_image(image_path: Path) -> str:
    """Read and base64 encode an image file."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def load_prompt(system_description: str) -> str:
    """Load the prompt template and inject the system description."""
    if not PROMPT_FILE.exists():
        print(f"Error: Prompt file not found: {PROMPT_FILE}")
        print("Create prompt.txt with your prompt template.")
        print("Use {system_description} as a placeholder for the system description.")
        sys.exit(1)
    
    template = PROMPT_FILE.read_text()
    return template.format(system_description=system_description)


def find_image(name: str) -> Path | None:
    """Find an image file by name (without extension) in the images directory."""
    for ext in IMAGE_EXTENSIONS:
        candidate = IMAGES_DIR / f"{name}{ext}"
        if candidate.exists():
            return candidate
        candidate = IMAGES_DIR / f"{name}{ext.upper()}"
        if candidate.exists():
            return candidate
    return None


def find_description(name: str) -> Path | None:
    """Find a description file by name in the descriptions directory."""
    candidate = DESCRIPTIONS_DIR / f"{name}.txt"
    return candidate if candidate.exists() else None


def list_available_diagrams() -> list[dict]:
    """List all diagrams that have both an image and description file."""
    available = []
    
    if not DESCRIPTIONS_DIR.exists():
        return available
    
    for desc_file in DESCRIPTIONS_DIR.glob("*.txt"):
        name = desc_file.stem
        image_path = find_image(name)
        if image_path:
            available.append({
                "name": name,
                "image": image_path,
                "description": desc_file,
            })
    
    return available


def list_models(api_key: str) -> None:
    """List available Gemini models."""
    genai.configure(api_key=api_key)
    print("Available models:\n")
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            print(f"  {model.name}")


def analyze_er_diagram(image_path: Path, description: str, api_key: str) -> str:
    """
    Analyze an ER diagram image and generate PlantUML code.
    
    Args:
        image_path: Path to the image of the ER diagram
        description: Textual description of the system being modeled
        api_key: Google Gemini API key
    
    Returns:
        Full response from the model
    """
    genai.configure(api_key=api_key)
    
    # Use gemini-1.5-flash with the full path, or try gemini-2.0-flash
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    image_data = encode_image(image_path)
    prompt = load_prompt(description)

    image_part = {
        "mime_type": get_mime_type(image_path),
        "data": image_data
    }
    
    response = model.generate_content([prompt, image_part])
    return response.text


def extract_plantuml(response: str) -> str:
    """Extract just the PlantUML code block from the response."""
    lines = response.split("\n")
    in_code_block = False
    plantuml_lines = []
    
    for line in lines:
        if line.strip().startswith("```plantuml") or (line.strip() == "```" and in_code_block):
            if in_code_block:
                break
            in_code_block = True
            continue
        if in_code_block:
            plantuml_lines.append(line)
    
    return "\n".join(plantuml_lines) if plantuml_lines else response


def main():
    import argparse
    import os
    
    parser = argparse.ArgumentParser(
        description="Convert ER diagram image to PlantUML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python er_verifier.py mydiagram
  python er_verifier.py --list
  python er_verifier.py --all
  python er_verifier.py --list-models
  python er_verifier.py mydiagram --output result.puml
        """
    )
    parser.add_argument("name", nargs="?", help="Diagram name (without extension)")
    parser.add_argument("--list", "-l", action="store_true", help="List available diagrams")
    parser.add_argument("--list-models", action="store_true", help="List available Gemini models")
    parser.add_argument("--all", "-a", action="store_true", help="Process all available diagrams")
    parser.add_argument("--output", "-o", help="Output file for PlantUML code")
    parser.add_argument("--output-dir", help="Output directory for batch processing")
    parser.add_argument("--full-response", "-f", action="store_true", 
                        help="Show full analysis, not just PlantUML code")
    
    args = parser.parse_args()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment or .env file")
        sys.exit(1)
    
    if args.list_models:
        list_models(api_key)
        return
    
    if not IMAGES_DIR.exists():
        print(f"Error: Images directory not found: {IMAGES_DIR}")
        sys.exit(1)
    
    if not DESCRIPTIONS_DIR.exists():
        print(f"Error: Descriptions directory not found: {DESCRIPTIONS_DIR}")
        sys.exit(1)
    
    if args.list:
        diagrams = list_available_diagrams()
        if not diagrams:
            print("No diagrams found with matching image and description files.")
        else:
            print(f"Available diagrams ({len(diagrams)}):\n")
            for d in diagrams:
                print(f"  {d['name']}")
                print(f"    Image: {d['image']}")
                print(f"    Description: {d['description']}")
                print()
        return
    
    if args.all:
        diagrams = list_available_diagrams()
        if not diagrams:
            print("No diagrams found to process.")
            return
        
        output_dir = Path(args.output_dir) if args.output_dir else Path("output")
        output_dir.mkdir(exist_ok=True)
        
        print(f"Processing {len(diagrams)} diagrams...\n")
        
        for d in diagrams:
            print(f"Processing: {d['name']}")
            description = d["description"].read_text()
            
            try:
                response = analyze_er_diagram(d["image"], description, api_key)
                output = response if args.full_response else extract_plantuml(response)
                
                output_file = output_dir / f"{d['name']}.puml"
                output_file.write_text(output)
                print(f"  -> {output_file}")
            except Exception as e:
                print(f"  Error: {e}")
        
        print(f"\nDone! Output files in: {output_dir.absolute()}")
        return
    
    if not args.name:
        parser.print_help()
        print("\nError: Provide a diagram name, use --list, or use --all")
        sys.exit(1)
    
    image_path = find_image(args.name)
    if not image_path:
        print(f"Error: No image found for '{args.name}'")
        sys.exit(1)
    
    desc_path = find_description(args.name)
    if not desc_path:
        print(f"Error: No description found for '{args.name}'")
        sys.exit(1)
    
    description = desc_path.read_text()
    
    print(f"Image: {image_path}")
    print(f"Description: {desc_path}")
    print("-" * 40)
    
    response = analyze_er_diagram(image_path, description, api_key)
    output = response if args.full_response else extract_plantuml(response)
    
    if args.output:
        Path(args.output).write_text(output)
        print(f"PlantUML code written to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()