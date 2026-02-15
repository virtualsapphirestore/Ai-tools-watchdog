import os
import json
import random
import datetime
import google.generativeai as genai

# --- Configuration ---
# Get API Key from environment variable (GitHub Secrets)
API_KEY = os.environ.get("GOOGLE_API_KEY")
HISTORY_FILE = "history.json"

# --- Affiliate Configuration ---
# Add your affiliate links here. Format: "Tool Name": "Your Link"
AFFILIATE_LINKS = {
    "Gamma App": "https://try.gamma.app/dmd9lziexhnu", 
    "Murf AI": "https://murf.ai",     
    "Jasper": "https://jasper.ai",
    "Copy.ai": "https://copy.ai",
    "Descript": "https://www.descript.com",
    "ElevenLabs": "https://elevenlabs.io"
}

# --- Tool Database (Expanded) ---
ALL_TOOLS = [
    # Presentation & Productivity
    {"name": "Gamma App", "url": "https://gamma.app", "description": "Create beautiful presentations, documents, and webpages with AI."},
    {"name": "Beautiful.ai", "url": "https://beautiful.ai", "description": "Presentation software that designs for you."},
    {"name": "Tome", "url": "https://tome.app", "description": "AI-powered storytelling format for presentations."},
    {"name": "Notion AI", "url": "https://www.notion.so/product/ai", "description": "Integrated AI assistant for notes, docs, and tasks."},
    {"name": "Otter.ai", "url": "https://otter.ai", "description": "AI meeting assistant that records audio, writes notes, and captures slides."},
    
    # Text & Writing
    {"name": "Jasper", "url": "https://jasper.ai", "description": "AI copywriter for marketing content."},
    {"name": "Copy.ai", "url": "https://copy.ai", "description": "AI writing tool for sales and marketing teams."},
    {"name": "Writesonic", "url": "https://writesonic.com", "description": "AI writer for SEO-friendly content."},
    {"name": "Rytr", "url": "https://rytr.me", "description": "AI writing assistant that helps you create high-quality content."},
    {"name": "Sudowrite", "url": "https://www.sudowrite.com", "description": "AI writing partner for creative writers."},

    # Chat & Search
    {"name": "Perplexity AI", "url": "https://www.perplexity.ai", "description": "An AI-powered search engine that provides direct answers with citations."},
    {"name": "ChatGPT", "url": "https://chat.openai.com", "description": "Conversational AI model by OpenAI."},
    {"name": "Claude", "url": "https://claude.ai", "description": "Next-generation AI assistant by Anthropic."},
    {"name": "Gemini", "url": "https://gemini.google.com", "description": "Google's most capable AI model."},
    {"name": "Bing Chat", "url": "https://www.bing.com/chat", "description": "AI-powered search and chat by Microsoft."},

    # Image Generation
    {"name": "Midjourney", "url": "https://www.midjourney.com", "description": "Generates realistic images from natural language descriptions."},
    {"name": "DALL-E 3", "url": "https://openai.com/dall-e-3", "description": "OpenAI's advanced image generation model."},
    {"name": "Stable Diffusion", "url": "https://stability.ai", "description": "Latent text-to-image diffusion model."},
    {"name": "Leonardo.ai", "url": "https://leonardo.ai", "description": "Create production-quality visual assets for your projects with AI."},
    {"name": "Adobe Firefly", "url": "https://firefly.adobe.com", "description": "Generative AI for creators, integrated into Adobe apps."},

    # Video & Audio
    {"name": "Murf AI", "url": "https://murf.ai", "description": "Turn text into lifelike speech for your videos."},
    {"name": "Runway", "url": "https://runwayml.com", "description": "AI tools for video editing and generation."},
    {"name": "ElevenLabs", "url": "https://elevenlabs.io", "description": "Text to speech and voice cloning software."},
    {"name": "Descript", "url": "https://www.descript.com", "description": "All-in-one video and podcast editing with AI transcription."},
    {"name": "Synthesia", "url": "https://www.synthesia.io", "description": "Create AI videos from text with avatars."},
    {"name": "HeyGen", "url": "https://www.heygen.com", "description": "AI video generator for business videos."},
    {"name": "Suno AI", "url": "https://suno.ai", "description": "Make songs, radio, and audio with AI."},

    # Coding & Development
    {"name": "GitHub Copilot", "url": "https://github.com/features/copilot", "description": "AI pair programmer."},
    {"name": "Replit Ghostwriter", "url": "https://replit.com", "description": "AI-powered coding assistant in the IDE."},
    {"name": "Tabnine", "url": "https://www.tabnine.com", "description": "AI code completion tool."},
    {"name": "Cursor", "url": "https://cursor.sh", "description": "The AI-first code editor."},

    # Business & Marketing
    {"name": "AdCreative.ai", "url": "https://www.adcreative.ai", "description": "Generate conversion-focused ad creatives and social media post creatives."},
    {"name": "Predis.ai", "url": "https://predis.ai", "description": "AI social media post generator."},
    {"name": "Reply.io", "url": "https://reply.io", "description": "AI-powered sales engagement platform."},
    {"name": "Lavender", "url": "https://www.lavender.ai", "description": "AI email coach for sales teams."},

    # Design & UI
    {"name": "Canva Magic Studio", "url": "https://www.canva.com", "description": "A suite of AI tools within Canva for design."},
    {"name": "Uizard", "url": "https://uizard.io", "description": "Design wireframes, mockups, and prototypes in minutes."},
    {"name": "Looka", "url": "https://looka.com", "description": "Design your own beautiful brand/logo with AI."},

    # Miscellaneous
    {"name": "ChatPDF", "url": "https://www.chatpdf.com", "description": "Chat with any PDF file using AI."},
    {"name": "Humata AI", "url": "https://www.humata.ai", "description": "Analyze complex documents 100X faster."},
    {"name": "Consensus", "url": "https://consensus.app", "description": "AI search engine for research."},
    {"name": "Scispace", "url": "https://typeset.io", "description": "AI research assistant to decode papers."},
    {"name": "Rewind", "url": "https://www.rewind.ai", "description": "Search anything you’ve seen, said, or heard on your Mac."}
]

# --- History Management ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def fetch_trending_tools():
    history = load_history()
    today = datetime.date.today().isoformat()
    
    # Filter tools: Don't show if reviewed in the last 30 days
    available_tools = []
    for tool in ALL_TOOLS:
        last_review = history.get(tool["name"])
        if last_review:
            date_obj = datetime.date.fromisoformat(last_review)
            days_since = (datetime.date.today() - date_obj).days
            if days_since > 30:
                available_tools.append(tool)
        else:
            # Never reviewed
            available_tools.append(tool)
            
    # If we ran out of new tools (unlikely with 50+), reset availability slightly
    if len(available_tools) < 2:
        available_tools = ALL_TOOLS
    
    # Randomly select 2 unique tools
    if len(available_tools) >= 2:
        selected_tools = random.sample(available_tools, 2)
    else:
        selected_tools = available_tools

    # Update history for selected tools (in memory, saved later)
    # We return the tool objects, main() will handle the review generation.
    # We should update history AFTER successful generation, but for simplicity we prepare it here.
    
    # Inject Affiliate Links
    for tool in selected_tools:
        if tool["name"] in AFFILIATE_LINKS:
            tool["url"] = AFFILIATE_LINKS[tool["name"]]
            
    return selected_tools, history

# --- Gemini Generation ---
def generate_review(tool):
    if not API_KEY:
        print(f"WARNING: GOOGLE_API_KEY not found. Skipping review generation for {tool['name']}.")
        return f"### {tool['name']}\n\n*Review pending (API Key missing)*\n\n[Visit Tool]({tool['url']})\n"

    try:
        genai.configure(api_key=API_KEY)
        
        # DEBUG: List available models
        try:
            print("Listing available models...")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"Found model: {m.name}")
        except Exception as e:
            print(f"Error listing models: {e}")

        # Try using the full model path if simple name fails
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        prompt = f"""
        Write a short but engaging review for an AI tool called "{tool['name']}".
        Description: {tool['description']}
        
        IMPORTANT: Write the review in ENGLISH.
        
        Format:
        ### <img src="https://logo.clearbit.com/{tool['url'].split('://')[-1].split('/')[0]}" width="24" height="24" style="vertical-align: middle; margin-right: 8px;"> [Tool Name]
        **Verdict:** [One sentence summary]
        
        [2-3 sentences about what it does]
        
        *   **Pros:** [List 2 pros]
        *   **Cons:** [List 1 con]
        
        [Link to tool]({tool['url']})
        """
        
        response = model.generate_content(prompt)
        # Fallback if model doesn't output the image tag exactly as requested, 
        # we can forcefully inject it in the python return string, but let's try prompting first.
        # Actually, it's safer to inject it in Python.
        
        logo_url = f"https://logo.clearbit.com/{tool['url'].split('://')[-1].split('/')[0]}"
        review_text = response.text.replace("### ", f"### <img src='{logo_url}' width='32' style='vertical-align: middle; border-radius: 4px; margin-right: 8px;'> ")
        
        return review_text + "\n---\n"
    except Exception as e:
        print(f"Error generating review for {tool['name']}: {e}")
        
        available_models = []
        try:
             for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
        except:
            available_models = ["Could not list models"]
            
        return f"### {tool['name']}\n\n*Error: {str(e)}*\n\n*Available Models: {', '.join(available_models)}*\n\n[Visit Tool]({tool['url']})\n"

# --- Main Execution ---
def main():
    tools, history = fetch_trending_tools()
    
    if not tools:
        print("No tools to review today.")
        return

    new_content = f"\n## Daily Update: {datetime.date.today()}\n\n"
    
    tools_reviewed_count = 0
    for tool in tools:
        print(f"Reviewing {tool['name']}...")
        review = generate_review(tool)
        if "Error generating review" not in review and "Review pending" not in review:
             # Only update history if review was successful (or at least attempted with API key)
             history[tool["name"]] = datetime.date.today().isoformat()
        
        new_content += review
        tools_reviewed_count += 1
    
    # Save updated history
    save_history(history)
    
    # Append to index.md
    file_path = "index.md"
    # Ensure file exists
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("---\nlayout: default\ntitle: AI Tools Watchdog\n---\n\n# AI Tools Watchdog\n\nAutomated daily reviews of trending AI tools.\n\n")
            
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"Updates written to index.md. {tools_reviewed_count} tools reviewed.")

if __name__ == "__main__":
    main()
