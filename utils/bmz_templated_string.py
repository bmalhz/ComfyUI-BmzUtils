"""BmzJinja2String."""
from typing import Dict, Any
from jinja2 import Environment

from ..utils import parse_kv_string


class BmzJinja2String:
    """BmzJinja2String node implementation."""

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        """Provide ComfyUI with node inputs."""
        from comfy.comfy_types.node_typing import IO

        return {
            "required": {
                "templated_text": ("STRING", {"multiline": True}),
                "variables": (IO.ANY,),
            }
        }

    RETURN_TYPES = (
        "STRING",
    )
    RETURN_NAMES = (
        "rendered_text",
    )
    FUNCTION = "process"
    CATEGORY = "BMZ"

    def process(
        self,
        templated_text: str,
        variables: Any
    ):
        """Execute the node."""
        if isinstance(variables, str):
            vars_dict = parse_kv_string(variables)
        elif isinstance(variables, dict):
            vars_dict = variables
        else:
            raise ValueError("'variables' must be either a str or a Dict[str, str]")

        env = Environment()
        template = env.from_string(templated_text)

        return {
            "result": (template.render(vars_dict), )
        }
