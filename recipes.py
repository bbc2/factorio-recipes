#!/usr/bin/env python3

import argparse
from collections import namedtuple
import json
import os


class Item(namedtuple('ItemBase', 'id')):
    @property
    def name(self):
        return ' '.join(self.id.split('-')).capitalize()

    @property
    def short_name(self):
        return ''.join(word[0] for word in self.id.split('-')).capitalize()


class Multiple(namedtuple('MultipleBase', 'item quantity')):
    pass


class Recipe(namedtuple('RecipeBase', 'inputs outputs')):
    def has_input(self, id):
        return any(input.item.id == id for input in self.inputs)

    def has_output(self, id):
        return any(output.item.id == id for output in self.outputs)


def parse_ingredient(ingredient):
    try:
        (id, quantity) = ingredient
    except ValueError:
        id = ingredient['name']
        quantity = ingredient['amount']
    item = Item(id=id)
    return Multiple(item=item, quantity=quantity)


def parse_result(result):
    try:
        id = result['name']
        quantity = result['amount']
    except TypeError:
        id = result
        quantity = 1
    item = Item(id=id)
    return Multiple(item=item, quantity=quantity)


def parse_recipe(id, recipe):
    try:
        recipe = recipe['normal']
    except KeyError:
        pass
    inputs = tuple(parse_ingredient(ingredient) for ingredient in recipe['ingredients'])
    try:
        outputs = (parse_result(recipe['result']),)
    except KeyError:
        outputs = tuple(parse_result(result) for result in recipe['results'])
    return Recipe(inputs=inputs, outputs=outputs)


def obsolete(recipe):
    ids_obsolete = frozenset((
        'electric-energy-interface',
        'express-loader',
        'fast-loader',
        'loader',
        'player-port',
        'railgun',
        'railgun-dart',
        'small-plane',
    ))
    inputs = frozenset(multiple.item.id for multiple in recipe.inputs)
    outputs = frozenset(multiple.item.id for multiple in recipe.outputs)
    return bool(ids_obsolete.intersection(inputs.union(outputs)))


def parse_recipes(data):
    recipes_raw = (
        parse_recipe(id, recipe)
        for (id, recipe) in data['recipe'].items()
    )
    return tuple(recipe for recipe in recipes_raw if not obsolete(recipe))


def get_dot_recipe(recipe):
    return tuple(
        '    "{}" -> "{}"'.format(input.item.id, output.item.id)
        for input in recipe.inputs
        for output in recipe.outputs
    )


def image_path(factorio_path, id):
    prefix = ()
    fluids = (
            'crude-oil',
            'heavy-oil',
            'light-oil',
            'lubricant',
            'petroleum-gas',
            'steam',
            'sulfuric-acid',
            'water',
    )
    if id in fluids:
        prefix = ('fluid',)
    elif id == 'empty-barrel':
        prefix = ('fluid', 'barreling')
    if id == 'discharge-defense-remote':
        id = 'discharge-defense-equipment'
    elif id == 'heat-exchanger':
        id = 'heat-boiler'
    elif id == 'locomotive':
        id = 'diesel-locomotive'
    elif id == 'locomotive':
        id = 'diesel-locomotive'
    elif id == 'low-density-structure':
        id = 'rocket-structure'
    return os.path.join(
        factorio_path,
        'data/base/graphics/icons',
        *prefix,
        '{}.png'.format(id),
    )


def get_dot_graph(factorio_path, recipes):
    dot = (
        'digraph all {',
    )
    nodes = frozenset(
        '    "{}" [label="",image="{}"]'
        .format(multiple.item.id, image_path(factorio_path, multiple.item.id))
        for recipe in recipes
        for multiple in recipe.inputs + recipe.outputs
    )
    dot += tuple(sorted(nodes))
    links = frozenset(link for recipe in recipes for link in get_dot_recipe(recipe))
    dot += tuple(sorted(links))
    dot += ('}',)
    return '\n'.join(dot)


def missing_recipes():
    stone = Item(id='stone')
    iron_ore = Item(id='iron-ore')
    copper_ore = Item(id='copper-ore')
    stone_brick = Item(id='stone-brick')
    iron_plate = Item(id='iron-plate')
    iron_gear_wheel = Item(id='iron-gear-wheel')
    pipe = Item(id='pipe')
    copper_plate = Item(id='copper-plate')
    copper_cable = Item(id='copper-cable')
    transport_belt = Item(id='transport-belt')
    electronic_circuit = Item(id='electronic-circuit')
    electric_mining_drill = Item(id='electric-mining-drill')
    assembing_machine_1 = Item(id='assembling-machine-1')
    inserter = Item(id='inserter')
    radar = Item(id='radar')
    return (
        Recipe(
            inputs=(
                Multiple(item=iron_ore, quantity=1),
            ),
            outputs=(
                Multiple(item=iron_plate, quantity=1),
            ),
        ),
        Recipe(
            inputs=(
                Multiple(item=copper_ore, quantity=1),
            ),
            outputs=(
                Multiple(item=copper_plate, quantity=1),
            ),
        ),
        Recipe(
            inputs=(
                Multiple(item=iron_plate, quantity=2),
            ),
            outputs=(
                Multiple(item=iron_gear_wheel, quantity=1),
            ),
        ),
        Recipe(
            inputs=(
                Multiple(item=copper_plate, quantity=1),
            ),
            outputs=(
                Multiple(item=copper_cable, quantity=2),
            ),
        ),
        Recipe(
            inputs=(
                Multiple(item=iron_plate, quantity=1),
            ),
            outputs=(
                Multiple(item=pipe, quantity=1),
            ),
        ),
        Recipe(
            inputs=(
                Multiple(item=iron_gear_wheel, quantity=1),
                Multiple(item=iron_plate, quantity=1),
            ),
            outputs=(
                Multiple(item=transport_belt, quantity=2),
            ),
        ),
        Recipe(
            inputs=(
                Multiple(item=iron_plate, quantity=1),
                Multiple(item=copper_cable, quantity=3),
            ),
            outputs=(
                Multiple(item=electronic_circuit, quantity=1),
            ),
        ),
        Recipe(
            inputs=(
                Multiple(item=iron_plate, quantity=10),
                Multiple(item=iron_gear_wheel, quantity=5),
                Multiple(item=electronic_circuit, quantity=3),
            ),
            outputs=(
                Multiple(item=electric_mining_drill, quantity=1),
            ),
        ),
        Recipe(
            inputs=(
                Multiple(item=electronic_circuit, quantity=3),
                Multiple(item=iron_gear_wheel, quantity=5),
                Multiple(item=iron_plate, quantity=9),
            ),
            outputs=(
                Multiple(item=assembing_machine_1, quantity=1),
            ),
        ),
        Recipe(
            inputs=(
                Multiple(item=stone, quantity=2),
            ),
            outputs=(
                Multiple(item=stone_brick, quantity=1),
            ),
        ),
        Recipe(
            inputs=(
                Multiple(item=iron_plate, quantity=1),
                Multiple(item=iron_gear_wheel, quantity=1),
                Multiple(item=electronic_circuit, quantity=1),
            ),
            outputs=(
                Multiple(item=inserter, quantity=1),
            ),
        ),
        Recipe(
            inputs=(
                Multiple(item=iron_plate, quantity=10),
                Multiple(item=iron_gear_wheel, quantity=5),
                Multiple(item=electronic_circuit, quantity=5),
            ),
            outputs=(
                Multiple(item=radar, quantity=1),
            ),
        ),
    )


def filter_sources(recipes, id):
    recipes_direct = frozenset(recipe for recipe in recipes if recipe.has_input(id))
    recipes_indirect = frozenset(
        indirect
        for direct in recipes_direct
        for output in direct.outputs
        for indirect in filter_sources(recipes - recipes_direct, output.item.id)
    )
    return recipes_direct.union(recipes_indirect)


def filter_target(recipes, id):
    recipes_direct = frozenset(recipe for recipe in recipes if recipe.has_output(id))
    recipes_indirect = frozenset(
        indirect
        for direct in recipes_direct
        for input in direct.inputs
        for indirect in filter_target(recipes - recipes_direct, input.item.id)
    )
    return recipes_direct.union(recipes_indirect)


def main(factorio_path, target):
    data = json.load(open('data.json'))
    recipes = frozenset(parse_recipes(data) + missing_recipes())
    recipes = filter_target(recipes, target)
    print(get_dot_graph(factorio_path, recipes))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('factorio_path', type=str)
    parser.add_argument('target', type=str)
    args = parser.parse_args()
    main(factorio_path=args.factorio_path, target=args.target)
