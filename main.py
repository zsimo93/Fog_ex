from core.API import mainAPI
from core.database import initSetup

initSetup.setup()
mainAPI.run()
