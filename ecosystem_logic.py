EMPTY, TREE, LAKE, DINO, BIRD = "empty", "tree", "lake", "dino", "bird"

TREE_O2, LAKE_O2, DINO_O2, BIRD_O2 = 0.8, 0.5, -1.0, -0.4
DINO_CO2, BIRD_CO2, TREE_CO2, LAKE_CO2 = 1.2, 0.4, -0.8, -0.5

MAX_BOTTOM_PATCHES = 12
MAX_BIRD_PATCHES = 12

def update_ecosystem(state):

    trees = state["bottom"].count(TREE)
    lakes = state["bottom"].count(LAKE)
    dinos = state["bottom"].count(DINO)
    birds = state["birds"].count(BIRD)

    state["oxygen"] += (
        trees * TREE_O2
        + lakes * LAKE_O2
        + dinos * DINO_O2
        + birds * BIRD_O2
    )

    state["co2"] += (
        dinos * DINO_CO2
        + birds * BIRD_CO2
        + trees * TREE_CO2
        + lakes * LAKE_CO2
    )

    state["oxygen"] = max(0, min(100, state["oxygen"]))
    state["co2"] = max(0, min(100, state["co2"]))

    state["biodiversity"] = (
        birds + dinos
    ) / (MAX_BOTTOM_PATCHES + MAX_BIRD_PATCHES)

    return state