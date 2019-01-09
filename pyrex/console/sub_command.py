from .command import Command


_HELP = """\

The <info>sub</> command does this <comment>and</comment> that and then some more while forces you
to write a really long text to <comment>check</comment> check this out and now some more gibberish
just to make my point I hope this is enough text.

"""


class SubCommand(Command):
    """
    The sub command

    sub
        {arg1 : The first argument}
    """

    help = " ".join(_HELP.splitlines()).strip()

    def handle(self):
        pass

        name = self.argument("regex")

        if name:
            text = "Hello {}".format(name)
        else:
            text = "Hello"

        if self.option("yell"):
            text = text.upper()

        self.line(text)

        self.line("<info>foo</info>")

        # yellow text
        self.line("<comment>foo</comment>")

        # black text on a cyan background
        self.line("<question>foo</question>")

        # white text on a red background
        self.line("<error>foo</error>")
