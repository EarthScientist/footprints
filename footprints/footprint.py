import rasterio
from rasterio.features import shapes
from shapely.geometry import MultiPolygon, box, shape
from pathlib import Path

class Footprint:
    def __init__(self, fn):
        '''
        raster extent footprint

        fn = [str] path to the rasterio readable raster file

        to return the extent footprint use method: `extent()` or `record()`
        
        '''
        self.fn = fn
        self.rst = rasterio.open(self.fn)
        self.crs = self.rst.crs.to_string()

    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.rst:
            self.rst.close()

    def open_raster(self):
        try:
            return rasterio.open(self.fn)
        except Exception as e:
            TypeError(f'{self.fn} is not a valid rasterio\nreadable raster file.')

    def extent(self):
        '''return an extent polygon of the raster extent(footprint)'''
        return box(*self.rst.bounds)

    @property
    def record(self):
        ''' return a dataframe record which passes nicely into GeoPandas '''
        return {'fn':str(self.fn), 'geometry':self.extent(), 'crs':self.crs}


"""
Valid (non-nodata) Extent instead of bounding rectangle.  

This can be a slow process if the data are high resolution. 
Rasters must have a valid nodata value for this to operate as it is 
built currently.

"""
class DataFootprint(Footprint):
    def extent(self):
        '''
        return polygon(s) of the valid raster data extent
        (all non-nodata pixels patches.)
        '''
        band = 1
        arr = self.rst.read_masks(band)
        t = self.rst.transform
        pols = [shape(i) 
                    for i,j in 
                        shapes(
                            arr,
                            transform=t,
                            ) 
                        if j != 0]
        n = len(pols)
        if n == 0: 
            pols = GeometryCollection()
        elif n == 1:
            pols, = pols
        else:
            pols = MultiPolygon(pols)
        return pols 
