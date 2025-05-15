import time
# import pandas as pd
import fsspec
from fsspec.implementations.local import LocalFileSystem


def logs(x):
	out_dir = "/var/lib/odoo/"
	with open(f"{out_dir}/log", "a") as f:
		# f.write(str(picking)+" "+picking.partner_geo)
		f.write("\n")
		f.write(f"{time.time()} "+str(x))
