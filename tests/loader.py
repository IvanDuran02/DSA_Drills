import importlib.util
import os
import sys
from typing import Any

def load_exercise(rel_path: str, symbol_name: str | None = None) -> Any:
    """
    Dynamically loads the target module based on DRILLS_TARGET or DRILLS_IMPL_PATH.
    If DRILLS_TARGET == 'reference', loads from reference/<rel_path>.
    Otherwise loads from drills/<rel_path> (student implementation).
    """
    custom_path = os.environ.get("DRILLS_IMPL_PATH")
    if custom_path and os.path.exists(custom_path):
        path = os.path.abspath(custom_path)
    else:
        target = os.environ.get("DRILLS_TARGET", "student")
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        base_dir = os.path.join(root_dir, "reference" if target == "reference" else "drills")
        path = os.path.join(base_dir, rel_path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Exercise file not found at: {path}")

    module_name = f"drill_{os.path.splitext(os.path.basename(rel_path))[0]}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to create module spec for {path}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    if symbol_name:
        if not hasattr(module, symbol_name):
            raise AttributeError(f"Module '{rel_path}' does not define '{symbol_name}'")
        return getattr(module, symbol_name)
    return module
