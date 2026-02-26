import copy

from synthetipy.parser import parse
from synthetipy.script_merger import utils
from synthetipy.ast_loadder import ASTLoader
from synthetipy.ast_nodes import *
from pathlib import Path
from synthetipy.compiler import compile_to_file


CONFIG = {
    'common': {
        "buildings",
        "districts",
        "zones"
    },
}

GAME_ROOT = Path("D:\SteamLibrary\steamapps\common\Stellaris")

ast = ASTLoader(GAME_ROOT, CONFIG).load()

out_file = DocumentNode([])


for name, obj in ast['common/buildings'].items():
    base_buildtime = None
    for stat in obj.body.statements:
        if not isinstance(stat, PropertyNode): continue
        if str(stat.key) == 'base_buildtime':
            base_buildtime = stat.value

    if base_buildtime:
        name = f'@bca_buildtime_{name}'
        val = base_buildtime
        const_node = ConstantDefinitionNode(name,val)
        out_file.statements.append(const_node)

compile_to_file(out_file, "../common/scripted_variables/bca_gen_constants.txt")
