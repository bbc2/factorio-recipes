local pretty = require('pl.pretty')
local json = require('dkjson')

require('dataloader')

require('ammo')
require('capsule')
require('equipment')
require('fluid-recipe')
require('furnace-recipe')
require('inserter')
require('module')
require('recipe')
require('turret')

print(json.encode(data.raw))
