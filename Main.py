# Library Imports
import nextcord, json, os
from nextcord.ext import commands
from dotenv import load_dotenv
from colorama import Fore, init

# Custom Imports
from Modules.Help import Help
from Server.WebServer import Start
from Views.Verify import VerifyView
from Views.Support import SupportView, StaffAppView
from Views.Roles import RoleView
from Views.Ranks import RankView

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Initialise Bot Variable / Class
intents = nextcord.Intents.all()
intents.members = True
intents.guilds = True

class TheCloud(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = commands.when_mentioned_or(Options['Prefix']),
            case_insensitive = True,
            help_command = Help(),
            activity = nextcord.Activity(type = nextcord.ActivityType.listening, name = f"{Options['Prefix']}help"),
            status = nextcord.Status.idle,
            intents = intents
        )
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(VerifyView(self))
            self.add_view(SupportView(self))
            self.add_view(StaffAppView(self))
            self.add_view(RoleView(self))
            self.add_view(RankView(self))
            self.persistent_views_added = True


Bot = TheCloud()

# Load extentions
init(autoreset = True)

extensions = [
    # Events #
    "Events.Greetings",
    "Events.Announcements",
    "Events.Starboard",
    "Events.Rep",

    # Commands #
    "Commands.Verify",
    "Commands.Developer",
    "Commands.Support",
    "Commands.Application",
    "Commands.Roles",
    "Commands.Admin",
    "Commands.Rep",
    "Commands.Economy",
    "Commands.Essentials",

    # Modules #
    "Modules.ErrorHandler",
]

if __name__ == '__main__':
    print(Fore.LIGHTBLUE_EX + "——■————■——[ Bot Starting ]——■————■——")

    print(Fore.LIGHTCYAN_EX + "[ ■ ] Starting to load extensions...")

    for extension in extensions:
        try:
            Bot.load_extension(extension)
            print(Fore.LIGHTGREEN_EX + f"  [+] {extension}")
        except Exception as error:
            print(Fore.LIGHTRED_EX + f"  [-] {extension}")
            print(error)

    print(Fore.LIGHTCYAN_EX + "[ ■ ] Finished loading extensions")

# Starting the web server
Start()

# Logging into discord with token from secure file
load_dotenv()
Bot.run(os.getenv('DiscordToken'))