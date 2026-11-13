import pkgutil
modules = [m.name for m in pkgutil.iter_modules()]
print("Modules disponibles:", modules[:30])