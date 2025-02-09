from custom_command import LinkCountingCommand
from openwpm.command_sequence import CommandSequence
from openwpm.commands.browser_commands import GetCommand
from openwpm.config import BrowserParams, ManagerParams
from openwpm.task_manager import TaskManager

#Code gotten from OPENWPM Project with slight modifications

# The list of sites that we wish to crawl
NUM_BROWSERS = 1
sites = []

file = open("SubPagesLess.txt", "r")
for page in file:
    page = page.strip('\n')
    sites.append(page)
# Loads the default ManagerParams
# and NUM_BROWSERS copies of the default BrowserParams
manager_params = ManagerParams(
    num_browsers=NUM_BROWSERS
)  # num_browsers is necessary to let TaskManager know how many browsers to spawn

browser_params = [BrowserParams(display_mode="native") for _ in range(NUM_BROWSERS)]

# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
    browser_params[i].http_instrument = True
    # Record cookie changes
    browser_params[i].cookie_instrument = True
    # Record Navigations
    browser_params[i].navigation_instrument = True
    # Record JS Web API calls
    browser_params[i].js_instrument = True
    # Record the callstack of all WebRequests made
    browser_params[i].callstack_instrument = True
    # Record DNS resolution
    browser_params[i].dns_instrument = True

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params.data_directory = "~/Desktop/"
manager_params.log_directory = "~/Desktop/"

# memory_watchdog and process_watchdog are useful for large scale cloud crawls.
# Please refer to docs/Configuration.md#platform-configuration-options for more information
# manager_params.memory_watchdog = True
# manager_params.process_watchdog = True

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager(manager_params, browser_params)

# Visits the sites
for site in sites:

    # Parallelize sites over all number of browsers set above.
    command_sequence = CommandSequence(
        site,
        reset=True,
        callback=lambda success, val=site: print("CommandSequence {} done".format(val)),
    )

    # Start by visiting the page
    command_sequence.append_command(GetCommand(url=site, sleep=10), timeout=60)
    # Have a look at custom_command.py to see how to implement your own command
    command_sequence.append_command(LinkCountingCommand())

    # Run commands across the three browsers (simple parallelization)
    manager.execute_command_sequence(command_sequence)

# Shuts down the browsers and waits for the data to finish logging
manager.close()
