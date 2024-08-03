from typing import Any
from click import command, option
from inflection import camelize


import mountaineer.client_builder.builder
from mountaineer.client_builder.build_schemas import (
    TSLiteral,
    python_payload_to_typescript,
)


def patched_convert_enum_to_interface(self, model):
    fields: dict[str, Any] = {}

    if not model.enum:
        raise ValueError(f"Model {model} is not an enum")

    for enum_value in model.enum:
        # If the enum is an integer, we need to escape it
        enum_key: str
        print(model.__dict__)
        if isinstance(enum_value, (int, float)):
            enum_key = f"Value__{enum_value}"
        elif isinstance(enum_value, str):
            enum_key = camelize(enum_value, uppercase_first_letter=True)
        else:
            raise ValueError(f"Invalid enum value: {enum_value}")

        fields[TSLiteral(enum_key)] = enum_value

    # Enums use an equal assignment syntax
    interface_body = python_payload_to_typescript(fields).replace(":", " =")
    interface_full = (
        f"enum {self.get_typescript_interface_name(model)} {interface_body}"
    )

    if self.export_interface:
        interface_full = f"export {interface_full}"

    return interface_full


# Define your custom converter class
class CustomClientBuilder(mountaineer.client_builder.builder.ClientBuilder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openapi_schema_converter._convert_enum_to_interface = (
            patched_convert_enum_to_interface.__get__(
                self.openapi_schema_converter, type(self.openapi_schema_converter)
            )
        )


mountaineer.client_builder.builder.ClientBuilder = CustomClientBuilder

from mountaineer.cli import handle_runserver, handle_watch, handle_build


from django_mountaineer.controllers import (
    patch_enable_hotreload_controllers_in_views_folder,
)

patch_enable_hotreload_controllers_in_views_folder()


@command()
@option("--port", default=5006, help="Port to run the server on")
def runserver(port: int):
    handle_runserver(
        package="example",
        webservice="example.main:app",
        webcontroller="example.app:app_controller",
        port=port,
    )


@command()
def watch():
    handle_watch(
        package="example",
        webcontroller="example.app:app_controller",
    )


@command()
def build():
    handle_build(
        webcontroller="example.app:app_controller",
    )


@command()
def generate():
    import django
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")
    django.setup()
    from django.apps import apps
    from django.db import models
    import importlib.util
    import os

    enums = {}

    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            model_file = model.__module__.replace(".", "/") + ".py"
            if os.path.exists(model_file):
                spec = importlib.util.spec_from_file_location(
                    model.__module__, model_file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for name, obj in vars(module).items():
                    if isinstance(obj, type) and issubclass(obj, models.TextChoices):
                        enums[name] = obj
    print(enums)

    def enum_choice_to_interface(choice):
        label = getattr(choice, "label", choice.value.replace("_", " ").capitalize())
        return ',\n'.join('    ' + line for line in [
            f"label: \"{label}\"",
            f"value: \"{choice.value}\"",
        ])

    def enum_to_interface(name, enum):
        return (
            "export const Enum"
            + name
            + ": EnumTextChoices = "
            + " {\n"
            + ",\n".join(
                "  " + "'" + item.value + "'"
                + ": {\n"
                + enum_choice_to_interface(item)
                + "\n  }"
                for item in enum
            )
            + "\n}"
        )

    definitions = [enum_to_interface(name, enum) for name, enum in enums.items()]

    definitions = [
        "export type EnumTextChoice = {label: string, value: string}",
        "export type EnumTextChoices = Record<string, EnumTextChoice>",
    ] + definitions

    with open("example/views/src/enums.ts", "w") as f:
        f.write("\n\n".join(definitions))
