"""
Baza filmova za CineBot.
15 filmova s metapodacima koji odgovaraju entitetima u Wit.ai.
"""

MOVIES = [
    {
        "title": "Inception",
        "year": 2010,
        "decade": 2010,
        "director": "Christopher Nolan",
        "genres": ["sci-fi", "thriller", "action"],
        "actors": ["Leonardo DiCaprio", "Tom Hardy"],
        "rating": 8.8,
        "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO."
    },
    {
        "title": "The Matrix",
        "year": 1999,
        "decade": 1990,
        "director": "Lana Wachowski",
        "genres": ["sci-fi", "action"],
        "actors": ["Keanu Reeves", "Morgan Freeman"],
        "rating": 8.7,
        "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."
    },
    {
        "title": "Interstellar",
        "year": 2014,
        "decade": 2010,
        "director": "Christopher Nolan",
        "genres": ["sci-fi", "drama"],
        "actors": ["Matthew McConaughey", "Anne Hathaway"],
        "rating": 8.7,
        "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."
    },
    {
        "title": "The Dark Knight",
        "year": 2008,
        "decade": 2000,
        "director": "Christopher Nolan",
        "genres": ["action", "crime", "drama"],
        "actors": ["Christian Bale", "Heath Ledger"],
        "rating": 9.0,
        "description": "Batman faces the Joker, a criminal mastermind who wants to plunge Gotham City into anarchy."
    },
    {
        "title": "Pulp Fiction",
        "year": 1994,
        "decade": 1990,
        "director": "Quentin Tarantino",
        "genres": ["crime", "drama"],
        "actors": ["Samuel L. Jackson", "John Travolta"],
        "rating": 8.9,
        "description": "The lives of two mob hitmen, a boxer, and others intertwine in four tales of violence and redemption."
    },
    {
        "title": "Forrest Gump",
        "year": 1994,
        "decade": 1990,
        "director": "Robert Zemeckis",
        "genres": ["drama", "romance", "comedy"],
        "actors": ["Tom Hanks", "Robin Wright"],
        "rating": 8.8,
        "description": "The history of the United States from the 1950s to the '70s unfolds from the perspective of an Alabama man with an IQ of 75."
    },
    {
        "title": "The Shawshank Redemption",
        "year": 1994,
        "decade": 1990,
        "director": "Frank Darabont",
        "genres": ["drama"],
        "actors": ["Morgan Freeman", "Tim Robbins"],
        "rating": 9.3,
        "description": "Two imprisoned men bond over years, finding solace and eventual redemption through acts of common decency."
    },
    {
        "title": "The Godfather",
        "year": 1972,
        "decade": 1970,
        "director": "Francis Ford Coppola",
        "genres": ["crime", "drama"],
        "actors": ["Al Pacino", "Robert De Niro"],
        "rating": 9.2,
        "description": "An organized crime dynasty's aging patriarch transfers control to his reluctant son."
    },
    {
        "title": "Fight Club",
        "year": 1999,
        "decade": 1990,
        "director": "David Fincher",
        "genres": ["drama", "thriller"],
        "actors": ["Brad Pitt", "Edward Norton"],
        "rating": 8.8,
        "description": "An insomniac office worker forms an underground fight club that evolves into something much more."
    },
    {
        "title": "Goodfellas",
        "year": 1990,
        "decade": 1990,
        "director": "Martin Scorsese",
        "genres": ["crime", "drama"],
        "actors": ["Robert De Niro", "Joe Pesci"],
        "rating": 8.7,
        "description": "The story of Henry Hill and his life in the mob, covering his relationship with his wife and partners."
    },
    {
        "title": "The Lord of the Rings",
        "year": 2001,
        "decade": 2000,
        "director": "Peter Jackson",
        "genres": ["fantasy", "action"],
        "actors": ["Elijah Wood", "Ian McKellen"],
        "rating": 8.8,
        "description": "A meek hobbit and his companions set out on a journey to destroy a powerful ring and save Middle-earth."
    },
    {
        "title": "Star Wars",
        "year": 1977,
        "decade": 1970,
        "director": "George Lucas",
        "genres": ["sci-fi", "action", "fantasy"],
        "actors": ["Mark Hamill", "Harrison Ford"],
        "rating": 8.6,
        "description": "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, and droids to save the galaxy."
    },
    {
        "title": "Jurassic Park",
        "year": 1993,
        "decade": 1990,
        "director": "Steven Spielberg",
        "genres": ["sci-fi", "action"],
        "actors": ["Sam Neill", "Laura Dern"],
        "rating": 8.2,
        "description": "A pragmatic paleontologist visits an almost complete theme park with cloned dinosaurs."
    },
    {
        "title": "Titanic",
        "year": 1997,
        "decade": 1990,
        "director": "James Cameron",
        "genres": ["romance", "drama"],
        "actors": ["Leonardo DiCaprio", "Kate Winslet"],
        "rating": 7.9,
        "description": "A young aristocrat falls in love with a poor artist aboard the ill-fated R.M.S. Titanic."
    },
    {
        "title": "Avatar",
        "year": 2009,
        "decade": 2000,
        "director": "James Cameron",
        "genres": ["sci-fi", "action", "fantasy"],
        "actors": ["Sam Worthington", "Zoe Saldana"],
        "rating": 7.9,
        "description": "A paraplegic Marine on the alien world of Pandora is torn between following orders and protecting the natives."
    },
    {
        "title": "The Shining",
        "year": 1980,
        "decade": 1980,
        "director": "Stanley Kubrick",
        "genres": ["horror", "drama"],
        "actors": ["Jack Nicholson", "Shelley Duvall"],
        "rating": 8.4,
        "description": "A family heads to an isolated hotel for the winter where a sinister presence influences the father into violence."
    },
    {
        "title": "The Exorcist",
        "year": 1973,
        "decade": 1970,
        "director": "William Friedkin",
        "genres": ["horror"],
        "actors": ["Ellen Burstyn", "Max von Sydow"],
        "rating": 8.1,
        "description": "When a young girl is possessed by a mysterious entity, her mother seeks the help of two priests to save her."
    },
    {
        "title": "Get Out",
        "year": 2017,
        "decade": 2010,
        "director": "Jordan Peele",
        "genres": ["horror", "thriller"],
        "actors": ["Daniel Kaluuya", "Allison Williams"],
        "rating": 7.7,
        "description": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness eventually reaches a boiling point."
    },
    {
        "title": "Hereditary",
        "year": 2018,
        "decade": 2010,
        "director": "Ari Aster",
        "genres": ["horror", "drama"],
        "actors": ["Toni Collette", "Alex Wolff"],
        "rating": 7.3,
        "description": "A grieving family is haunted by tragic and disturbing occurrences after the death of their secretive grandmother."
    }
]


def get_all_movies():
    return MOVIES


def find_by_title(title):
    """Pronadi film po naslovu (case-insensitive)."""
    title_lower = title.lower().strip()
    for movie in MOVIES:
        if movie["title"].lower() == title_lower:
            return movie
    return None


def find_by_genre(genre):
    """Vrati listu filmova u zadanom zanru."""
    genre_lower = genre.lower().strip()
    return [m for m in MOVIES if genre_lower in [g.lower() for g in m["genres"]]]


def find_by_actor(actor):
    """Vrati listu filmova u kojima glumi zadani glumac."""
    actor_lower = actor.lower().strip()
    return [m for m in MOVIES if any(actor_lower == a.lower() for a in m["actors"])]


def find_by_director(director):
    """Vrati listu filmova zadanog redatelja."""
    director_lower = director.lower().strip()
    return [m for m in MOVIES if m["director"].lower() == director_lower]


def find_by_decade(decade):
    """Vrati listu filmova iz zadanog desetljeca."""
    try:
        decade_int = int(decade)
        return [m for m in MOVIES if m["decade"] == decade_int]
    except (ValueError, TypeError):
        return []
