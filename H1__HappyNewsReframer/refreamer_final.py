import requests
from bs4 import BeautifulSoup
import ollama

def reframer_news(url: str, model_name: str = "llama3.1"):
    # 1. Disable proxy usage for requests session
    session = requests.Session()
    session.trust_env = False  # Bypasses system-level proxy settings
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching article: {e}")
        return

    # 2. Extract clean text from HTML
    soup = BeautifulSoup(response.text, "html.parser")
    for script in soup(["script", "style", "header", "footer", "nav"]):
        script.extract()
        
    article_text = soup.get_text(separator=" ", strip=True)

    # 3. Construct the prompt
    prompt = f"""
    You are an expert editor specializing in solutions journalism. 
    Read the following news text and rewrite it so that it highlights constructive progress, 
    human resilience, solution-oriented aspects, and hope—while keeping the core factual events intact.

    [ARTICLE TEXT START]
    {article_text[:8000]}
    [ARTICLE TEXT END]
    """

    # 4. Stream response from Ollama
    stream = ollama.chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    print("\n--- UPLIFTING VERSION ---\n")
    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)

if __name__ == "__main__":
    target_url = input("Enter the news article URL: ").strip()
    if not target_url:
        print("No URL entered. Exiting.")
    else:
        reframer_news(target_url, model_name="llama3.1")
    ### Replace with a real news URL to test
    ##target_url = "https://bbc.com/news" 
    ##reframer_news(target_url, model_name="llama3.1")
