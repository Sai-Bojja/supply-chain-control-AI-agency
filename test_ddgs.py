from duckduckgo_search import DDGS

def test_search():
    query = "Sony Headphones news"
    print(f"Searching for: {query}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                print(f"Found {len(results)} results:")
                for r in results:
                    print(f"- {r['title']}")
            else:
                print("No results found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_search()
