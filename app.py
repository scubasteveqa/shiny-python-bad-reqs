import platform
import subprocess
import sys

from shiny import App, reactive, render, ui

app_ui = ui.page_fluid(
    ui.h2("Tool versions:"),
    ui.span("Python"),
    ui.output_text_verbatim("python"),
    ui.input_text_area("cmd", "Command to run", placeholder="Enter text"),
    ui.output_text_verbatim("cmd_output"),
    ui.input_text_area("logme", "Text to log", placeholder="Enter text"),
    ui.input_checkbox("stderr", "log to stderr", False),
    ui.input_action_button("log_button", "Log"),
    ui.output_text_verbatim("logged"),
)


def server(input, output, session):
    @output
    @render.text
    def python():
        return platform.python_version()

    @output
    @render.text
    def cmd_output():
        cmd=input.cmd()
        try:
            return subprocess.check_output(cmd, shell=True).decode()
        except Exception as e:
            return f"Error: {e}"

    @render.text()
    @reactive.event(input.log_button)
    def logged():
        l = input.logme()
        if input.stderr():
            print(l, file=sys.stderr)
        else:
            print(l)
        return l

app = App(app_ui, server)
