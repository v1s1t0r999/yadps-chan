import disnake
from handler.logging.log import Log
from handler.config.data import Data
from handler.database.sql import Sql
from handler.commands.controller import CommandController
from disnake.ext import commands


class Yadps(commands.Bot):
    data = Data().read()
    bot_log = Log().create(__name__, data.bot_log)
    sql = Sql()
    cmd_controller = CommandController

    def init(self):
        self.bot_log.info("Initing yadps-chan")
        self.cmd_controller(self).init()
        self.sql.init()
        if self.data.token == "":
            self.bot_log.error("Token not found!")
            exit(1)
        if self.data.prefix == "":
            self.bot_log.warn("Prefix not found!")
        self.bot_log.info("Valid .env configuration detected")

    async def on_ready(self):
        self.bot_log.info("yadps-chan is connected")

    async def on_message(self, message: disnake.Message):
        if message.author == self.user:
            return

    async def on_slash_command(self, inter):
        self.bot_log.info(f"Slash command: {inter.data.name} invoked by {inter.author}")

    async def on_slash_command_completion(self, inter):
        self.bot_log.info(f"Slash command: {inter.data.name} invoked by {inter.author} successful")

    async def on_slash_command_error(self, inter, error):
        self.bot_log.error(inter, error)
        if isinstance(error, commands.MissingAnyRole):
            if self.data.command_warnings:
                self.bot_log.warning(f"{inter.author} is missing roles for slash command: {inter.data.name}")
            if self.data.command_debug or self.data.mode == "development":
                self.bot_log.debug(f"Command -> {inter.data.name} | Invoked from -> {inter.channel_id} | By user"
                                     f"-> {inter.author} | Error -> {inter.author} missing roles")
            await inter.send(f"{inter.author.mention}, you don't have the required permissions for this command.")
