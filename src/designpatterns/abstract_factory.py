from abc import ABC, abstractmethod

"""
Use the Abstract Factory when:
    * a system should be independent of how its products are created, composed, and represented

    * a system should be configured with one of multiple families of products

    * a family of related product ojbects is designed to be used together, and you need to enforce this constraint

    * you want to provide a class library of products, and you want to reveal just their interfaces, not their implementations
"""

class AbstractMovie(ABC):

    @abstractmethod
    def play(self) -> str: ...


class TropicThunder(AbstractMovie):

    def play(self) -> str:
        return """
        I know who I am. I'm the dude playin' the dude, disguised as another dude!
        """


class AmericanPsycho(AbstractMovie):

    def play(self) -> str:
        return  """
        Now let's see Paul Allen's card. Look at that subtle off-white coloring. The tasteful thickness of it. 
        Oh, my God. It even has a watermark.
        """

class AbstractSnacks(ABC):

    @abstractmethod
    def stuff_face(self) -> str: ...


class JellyBeans(AbstractSnacks):

    def stuff_face(self) -> str:
        return """
        Washing a pack of \"Jelly Beans\" down with some delicious Booty Sweat\u2122...
        """


class DorsiaTakeaway(AbstractSnacks):

    def stuff_face(self) -> str:
        return """
        Gulping down the duck canette while you ponder why you couldn't get a reservation...
        """


class AbstractMovieNightFactory(ABC):

    @abstractmethod
    def create_movie(self) -> AbstractMovie: ...

    @abstractmethod
    def create_snacks(self) -> AbstractSnacks: ...


class ComedyMovieNightFactory(AbstractMovieNightFactory):

    def create_movie(self) -> AbstractMovie:
        return TropicThunder()
    
    def create_snacks(self) -> AbstractSnacks:
        return JellyBeans()


class ThrillerMovieNightFactory(AbstractMovieNightFactory):

    def create_movie(self) -> AbstractMovie:
        return AmericanPsycho()
    
    def create_snacks(self) -> AbstractSnacks:
        return DorsiaTakeaway()


def client(factory: AbstractMovieNightFactory):
    movie = factory.create_movie()
    snacks = factory.create_snacks()
    print(movie.play())
    print(snacks.stuff_face())


if __name__ == "__main__":
    comedy_movie_night_factory = ComedyMovieNightFactory()
    thriller_movie_night_factory = ThrillerMovieNightFactory()
    client(comedy_movie_night_factory)
    client(thriller_movie_night_factory)
