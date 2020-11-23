PRIVATE_PREFIX = "_"


class Descriptor:
    """Only to test if a child class is a descriptor."""
    pass


class Positive(Descriptor):
    def __init__(self, name):
        self.display_name = name

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = PRIVATE_PREFIX + name

    def __get__(self, instance, owner=None):
        if instance is None:
            # https://stackoverflow.com/a/21629855/11477374
            print(
                "Descriptor accessed as class attribute, returning descriptor instance"
            )
            return self
        value = getattr(instance, self.private_name)
        print(f"Schaue '{self.display_name}' nach...")
        return value

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"Negativer Wert für {self.display_name}.")
        setattr(instance, self.private_name, value)
        print(f"{self.display_name} von {instance.name} wurde zu {value} gesetzt.")


class Card:
    power = Positive("Leistung")
    displacement = Positive("Hubraum")
    speed = Positive("Geschwindigkeit")
    n_cylinders = Positive("Anzahl Zylinder")
    weight = Positive("Gewicht")
    acceleration = Positive("Beschleunigung")

    def __init__(
        self, name, power, displacement, speed, n_cylinders, weight, acceleration
    ):
        self.name = name
        self.power = power
        self.displacement = displacement
        self.speed = speed
        self.n_cylinders = n_cylinders
        self.weight = weight
        self.acceleration = acceleration

    def __repr__(self):
        cls = self.__class__.__name__
        normal_attrs = ["name"]
        private_attrs = [
            "power",
            "displacement",
            "speed",
            "n_cylinders",
            "weight",
            "acceleration",
        ]
        key_value_repr = (
            lambda name, prefix="": f"{name}={getattr(self, prefix + name)}"
        )
        private_reprs = [key_value_repr(name, PRIVATE_PREFIX) for name in private_attrs]
        normal_reprs = [key_value_repr(name) for name in normal_attrs]
        return f"{cls}({', '.join(normal_reprs + private_reprs)})"


mercedes_280 = Card("Mercedes 280 SE", 2746, 200, 185, 6, 1665, 11)
ford_capri = Card("Ford Capri 2300 GT", 2293, 180, 108, 6, 1060, 11)
citroen_gs = Card("Citroen GS", 1015, 145, 54, 4, 890, 19)
fiat_850 = Card("Fiat 850 Sport", 903, 145, 52, 4, 745, 19)


def query_numbered_list_item(iterable, item_category, n_picks):
    iterable = list(iterable)  # Create reusable copy
    print_numbered_list(iterable)

    picked = set()
    while len(picked) < n_picks:
        try:
            if not picked:
                first = "\b" if n_picks <= 1 else "first"  # ASCII backspace
                n = int(input(f"Pick your {first} {item_category}: "))
            else:
                n = int(input(f"Pick {item_category} number {len(picked) + 1}: "))
        except ValueError:
            print("Input was not a valid number, try again...")
        else:
            if 1 <= n <= len(iterable):
                orig_len = len(picked)
                picked.add(iterable[n - 1])
                if len(picked) == orig_len:
                    print(f"{item_category.title()} already chosen, try a different one...")
            else:
                print("Input not within the valid range, try again...")
    return picked



def print_numbered_list(iterable):
    for i, item in enumerate(iterable, start=1):
        print(f"{i})", item)


def battle():
    # Only pick unique cards via set comprehension. Pretty ugly.
    cards = list({card for card in globals().values() if isinstance(card, Card)})

    picked_cards = query_numbered_list_item(cards, "card", 2)

    categories = {
        obj.display_name: obj.public_name for obj in vars(Card).values() if isinstance(obj, Descriptor)
    }
    # Unpack iterable of length 1:
    cat_display_name, = query_numbered_list_item(categories.keys(), "category", 1)
    cat_name = categories[cat_display_name]

    print(f"Comparing in the category {cat_display_name}...")

    cat_values_to_names = {
        getattr(card, cat_name): card.name for card in picked_cards
    }

    if len(cat_values_to_names) == 1:
        print("Draw!")
        return

    winner_value = max(cat_values_to_names.keys())
    winner_name = cat_values_to_names[winner_value]

    print(f"{winner_name} wins with {winner_value} in the category {cat_display_name}!")

battle()
