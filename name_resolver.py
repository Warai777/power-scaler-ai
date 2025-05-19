import requests

def resolve_character_name(nickname):
    """
    Resolves a character nickname or shorthand (e.g., 'Luffy') into the full canonical name
    using the AniList GraphQL API. Falls back to the original input if not found.
    """
    query = '''
    query ($search: String) {
      Character(search: $search) {
        name {
          full
        }
      }
    }
    '''
    variables = {"search": nickname}

    try:
        response = requests.post(
            "https://graphql.anilist.co",
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"}
        )

        result = response.json()
        return result["data"]["Character"]["name"]["full"]
    except Exception as e:
        print(f"[Alias Resolver] Failed to resolve '{nickname}': {e}")
        return nickname  # fallback to user input
