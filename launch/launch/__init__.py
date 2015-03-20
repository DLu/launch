from launch.output_handler import CompositeOutputHandler
from launch.output_handler import ConsoleOutput
from launch.exit_handler import DefaultExitHandler


class LaunchDescriptor(object):

    def __init__(self):
        self.process_descriptors = []

    def add_process(self, cmd, name=None, env=None, output_handlers=None, exit_handler=None):
        if name is not None and name in [p.name for p in self.process_descriptors]:
            raise RuntimeError("Process name '%s' already used" % name)
        if output_handlers is None:
            output_handlers = [ConsoleOutput()]
        output_handlers = CompositeOutputHandler(output_handlers)
        if exit_handler is None:
            exit_handler = DefaultExitHandler()
        self.process_descriptors.append(ProcessDescriptor(
            cmd, name, output_handlers, exit_handler, env=env))


class ProcessDescriptor(object):

    def __init__(self, cmd, name, output_handler, exit_handler, env=None):
        self.cmd = cmd
        self.name = name
        self.output_handler = output_handler
        self.exit_handler = exit_handler
        self.env = env
        self.transport = None
        self.protocol = None
        self.returncode = None
