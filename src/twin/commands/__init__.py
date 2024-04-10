import importlib

modules = {_: importlib.import_module(f'twin.commands.{_}') for _ in ['show', 'capture']}
