import rasterio
from pathlib import Path
from lxml.builder import E

class Map:
    def __init__(self, fn):
        self.rst = rasterio.open(fn)
        self.arr = self.rst.read()
        self.filename = fn
        self.desc = Path(fn).name
        self.bounds = ','.join([str(int(round(i))) for i in self.rst.bounds])
        self.prj_name = self.get_prj_name()
        self.has_vector = 0
        self.has_raster = 1
        self.has_elevation = 1
        self.required_mem = '' # this is an odd one...
        self.disabled = 0
        self.min_elev = self.get_min_elev()
        self.max_elev = self.get_max_elev()
        self.spatial_res_x = self.get_resolution()[0]
        self.spatial_res_y = self.get_resolution()[1]
        self.pix_width = self.rst.shape[1]
        self.pix_height = self.rst.shape[0]
        self.band_count = self.rst.count
    
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.rst:
            self.rst.close()

    def get_prj_name(self):
        name = self.rst.crs.wkt.split(',')[0]
        return name.split("[")[-1].replace('"', "").replace(",", '')

    def get_min_elev(self):
        return self.arr[ self.arr != self.rst.nodata ].min()

    def get_max_elev(self):
        return self.arr[ self.arr != self.rst.nodata ].max()

    def get_resolution(self):
        return self.rst.res

    def xml(self):
        return E.map(
                    E.filename(str(self.filename)),
                    E.desc(str(self.desc)),
                    E.bounds(str(self.bounds)),
                    E.prj_name(str(self.prj_name)),
                    E.has_vector(str(self.has_vector)),
                    E.has_raster(str(self.has_raster)),
                    E.has_elevation(str(self.has_elevation)),
                    E.required_mem(str(self.required_mem)),
                    E.disabled(str(self.disabled)),
                    E.min_elev(str(self.min_elev)),
                    E.max_elev(str(self.max_elev)),
                    E.spatial_res_x(str(self.spatial_res_x)),
                    E.spatial_res_y(str(self.spatial_res_y)),
                    E.pix_width(str(self.pix_width)),
                    E.pix_height(str(self.pix_height)),
                    E.band_count(str(self.band_count), ) 
                    )
