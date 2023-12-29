from typing import List, TypeVar

TAuthor = TypeVar("Author")
TGenre = TypeVar("Genre")


class Book:
    def __init__(self, title: str, description: str, language: str, authors: List[TAuthor], genres: List[TGenre], publication_year: int, isbn: str ) -> None:
        self.title = title
        self.description = description
        self.language = language
        self.authors = authors
        self.genres = genres
        self.publication_year = publication_year
        self.isbn = isbn

    def __str__(self) -> str:
        author_names = ", ".join(str(author) for author in self.authors)
        genre_names = ", ".join(genre.name for genre in self.genres)
        return (
            f"Title: {self.title}\n"
            f"Description: {self.description}\n"
            f"Language: {self.language}\n"
            f"Authors: {author_names}\n"
            f"Genres: {genre_names}\n"
            f"Publication Year: {self.publication_year}\n"
            f"ISBN: {self.isbn}"
        )

    def __repr__(self) -> str:
        return (
            f"Book({self.title}, {self.description}, {self.language}, "
            f"{self.authors}, {self.genres}, {self.publication_year}, {self.isbn})"
        )

    def __eq__(self, other: "Book") -> bool:
        return (
            self.title == other.title
            and self.authors == other.authors
            and self.genres == other.genres
        )


class Author:
    def __init__(self, f_name: str, l_name: str, year: int) -> None:
        self.f_name = f_name
        self.l_name = l_name
        self.year = year

    def __str__(self) -> str:
        return f"{self.f_name} {self.l_name} ({self.year})"

    def __repr__(self) -> str:
        return f"Author({self.f_name}, {self.l_name}, {self.year})"

    def __eq__(self, other: "Author") -> bool:
        return (
            self.f_name == other.f_name
            and self.l_name == other.l_name
            and self.year == other.year
        )


class Genre:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"

    def __repr__(self) -> str:
        return f"Genre({self.name}, {self.description})"

    def __eq__(self, other: "Genre") -> bool:
        return self.name == other.name and self.description == other.description


