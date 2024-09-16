from genai_stack.genai_server.settings.config import read_configurations
from genai_stack.genai_server.utils import get_current_stack
import pathlib

path = f"{str(pathlib.Path().resolve())}/setup"
stack_configurations = read_configurations(path)[1]
stack = get_current_stack(config=stack_configurations)
