################################################################################
#
# This program is part of the WBEMDataSource Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""WBEMPlugin

wrapper for PythonPlugin

$Id: WBEMPlugin.py,v 1.2 2010/02/22 11:14:43 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]


from Products.DataCollector.plugins.CollectorPlugin import CollectorPlugin
from WBEMClient import WBEMClient, CError

class WBEMPlugin(CollectorPlugin):
    """
    A WBEMPlugin defines a native Python collection routine and a parsing
    method to turn the returned data structure into a datamap. A valid
    WBEMPlugin must implement the process method.
    """
    transport = "python"
    deviceProperties = CollectorPlugin.deviceProperties + (
        'zWinUser',
        'zWinPassword',
        'zWbemPort',
        'zWbemProxy',
        'zWbemUseSSL',
    )

    tables = {}

    def queries(self, device):
        return self.tables

    def collect(self, device, log):
        return WBEMClient(device).query(self.queries(device),
                                                    includeQualifiers = True)

    def preprocess(self, results, log):
        newres = {}
        for table, value in results.iteritems():
            if isinstance(value[0], CError):
                log.error(value[0].getErrorMessage())
                continue
            newres[table] = value
        return newres




