from pathlib import Path
import multiprocessing as mp
from shapely.geometry import GeometryCollection
from .footprint import Footprint, DataFootprint

class GetFootprints:
	def __init__(self, path='', filelist=None, wildcard='*', data_only=False):
		self.path = Path(path)
		self.wildcard = wildcard
		self.filelist = filelist
		if self.filelist is None:
			self.filelist = self._getfiles()
		self.data_only = data_only

	def _getfiles(self):
		if self.path:
			return list(self.path.rglob(self.wildcard))

	def footprints(self, ncpus=1):
		files= [str(fn) for fn in self.filelist]
		if len(self.filelist) == 0:
			raise ValueError('No files found with wildcard')
		if ncpus == 1:
			out = [self._openfootprint(fn) for fn in files]
		else:
			pool = mp.Pool(ncpus)
			out = pool.map(self._openfootprint, files)
			pool.close()
			pool.join()
			self._footprints = out
		return out

	@staticmethod
	def _footprints(data_only):
		return {
			True:DataFootprint,
			False:Footprint,
			}[bool(data_only)]

	def _openfootprint(self, fn):
		try:
			with self._footprints(self.data_only)(fn) as footprint:
				rec = footprint.record
		except:
			rec = {'fn':str(fn), 'geometry':GeometryCollection(), 'crs':None}
		return rec

