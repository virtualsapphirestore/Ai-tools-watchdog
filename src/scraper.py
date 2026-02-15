
import os
import datetime
import google.generativeai as genai

# --- Configuration ---
# Get API Key from environment variable (GitHub Secrets)
API_KEY = os.environ.get("GOOGLE_API_KEY")

# --- Affiliate Configuration ---
# Add your affiliate links here. Format: "Tool Name": "Your Link"
AFFILIATE_LINKS = {
    "Gamma App": "https://gamma.app", # REPLACE THIS LATER with your affiliate link
    "Murf AI": "https://murf.ai",     # REPLACE THIS LATER with your affiliate link
    "Jasper": "https://jasper.ai",
    "Copy.ai": "https://copy.ai"
}

# --- Mock Data Source (Replace with real scraping logic) ---
# In the future, you can use requests/BeautifulSoup here to scrape sites like ProductHunt, etc.
def fetch_trending_tools():
    # Expanded list of tools to rotate through
    all_tools = [
        {"name": "Gamma App", "url": "https://gamma.app", "description": "Create beautiful presentations, documents, and webpages with AI."},
        {"name": "Perplexity AI", "url": "https://www.perplexity.ai", "description": "An AI-powered search engine that provides direct answers with citations."},
        {"name": "Murf AI", "url": "https://murf.ai", "description": "Turn text into lifelike speech for your videos."},
        {"name": "Jasper", "url": "https://jasper.ai", "description": "AI copywriter for marketing content."},
        {"name": "Copy.ai", "url": "https://copy.ai", "description": "AI writing tool for sales and marketing teams."},
        {"name": "Midjourney", "url": "https://www.midjourney.com", "description": "Generates realistic images from natural language descriptions."},
        {"name": "Runway", "url": "https://runwayml.com", "description": "AI tools for video editing and generation."},
        {"name": "ElevenLabs", "url": "https://elevenlabs.io", "description": "Text to speech and voice cloning software."},
        {"name": "Beautiful.ai", "url": "https://beautiful.ai", "description": "Presentation software that designs for you."},
        {"name": "Tome", "url": "https://tome.app", "description": "AI-powered storytelling format for presentations."}
    ]
    
    # Simple rotation logic based on the day of the year
    # Selects 2 different tools each day
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    tools_count = len(all_tools)
    
    # Pick 2 tools based on the current day to ensure rotation
    idx1 = (day_of_year * 2) % tools_count
    idx2 = (day_of_year * 2 + 1) % tools_count
    
    selected_tools = [all_tools[idx1], all_tools[idx2]]
    
    # Inject Affiliate Links if available
    for tool in selected_tools:
        if tool["name"] in AFFILIATE_LINKS:
            tool["url"] = AFFILIATE_LINKS[tool["name"]]
            
    return selected_tools

# --- Gemini Generation ---
def generate_review(tool):
    if not API_KEY:
        print(f"WARNING: GOOGLE_API_KEY not found. Skipping review generation for {tool['name']}.")
        return f"### {tool['name']}\n\n*Review pending (API Key missing)*\n\n[Visit Tool]({tool['url']})\n"

    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Write a short but engaging review for an AI tool called "{tool['name']}".
        Description: {tool['description']}
        
        IMPORTANT: Write the review in ENGLISH.
        
        Format:
        ### [Tool Name]
        **Verdict:** [One sentence summary]
        
        [2-3 sentences about what it does]
        
        *   **Pros:** [List 2 pros]
        *   **Cons:** [List 1 con]
        
        [Link to tool]({tool['url']})
        """
        
        response = model.generate_content(prompt)
        return response.text + "\n---\n"
    except Exception as e:
        print(f"Error generating review for {tool['name']}: {e}")
        return f"### {tool['name']}\n\n*Error generating review.*\n\n[Visit Tool]({tool['url']})\n"

# --- Main Execution ---
def main():
    tools = fetch_trending_tools()
    new_content = f"\n## Daily Update: {datetime.date.today()}\n\n"
    
    for tool in tools:
        print(f"Reviewing {tool['name']}...")
        review = generate_review(tool)
        new_content += review
    
    # Append to index.md
    file_path = "index.md"
    # Ensure file exists
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("---\nlayout: default\ntitle: AI Tools Watchdog\n---\n\n# AI Tools Watchdog\n\nAutomated daily reviews of trending AI tools.\n\n")
            
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(new_content)
    
    print("Updates written to index.md")

if __name__ == "__main__":
    main()
