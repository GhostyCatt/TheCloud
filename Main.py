# Library Imports
import nextcord, json, os, random
from nextcord.ext import commands
from dotenv import load_dotenv
from colorama import Fore, init

# Custom Imports
from Modules.HelpCommand import Help
from Functions.WebServer import Start
from Tools.Verify import Counter
from Tools.Support import SupportView, StaffAppView
from Tools.Roles import RoleView
from Tools.Ranks import RankView

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
            self.add_view(Counter(self))
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

    # Commands #
    "Commands.Verify",
    "Commands.Developer",
    "Commands.Support",
    "Commands.Application",
    "Commands.Roles",
    "Commands.Admin",

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

    print(Fore.LIGHTCYAN_EX + "[ ■ ] Finished loading extensions")

# Starting the web server
Start(port = random.randint(2000, 9000))

# Logging into discord with token from secure file
load_dotenv()
Bot.run(os.getenv('DiscordToken'))