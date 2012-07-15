"""The rite factory."""

from Balance.BalanceRite     import BalanceRite
from Database.DatabaseRite   import DatabaseRite
from Graph.GraphRite         import GraphRite
from Heartbeat.HeartbeatRite import HeartbeatRite
from Poke.PokeRite           import PokeRite
from Registry.RegistryRite   import RegistryRite
from Scheduler.SchedulerRite import SchedulerRite

def createRite(aCritter, aName):
    """Creates a rite.

    Arguments:
        aCritter: The name of the critter holding the rite.
        aName:    The name of the rite.

    Returns:
        The rite that is daemonized, None if the rite of such a name is not available.

    """

    rites = \
    {
        'Balance':   BalanceRite,
        'Database':  DatabaseRite,
        'Graph':     GraphRite,
        'Heartbeat': HeartbeatRite,
        'Poke':      PokeRite,
        'Registry':  RegistryRite,
        'Scheduler': SchedulerRite
    }

    if aName in rites:
        def newInstance(type_, critter):
            return type_(critter,
                         critter.getCritterData(),
                         critter.getSettings(),
                         critter.getPostOffice())

        rite = newInstance(rites[aName], aCritter)

        rite.setDaemon(True)

        return rite
    else:
        return None
