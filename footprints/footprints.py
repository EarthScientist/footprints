from pathlib import Path
from .getfootprints import GetFootprints
import rasterio
from shapely.geometry import mapping, shape
import geopandas as gpd
import argparse
import sys
import fiona
from fiona.transform import transform_geom

def update_geom(row, geom):
   row['geometry']=geom
   return row

def reproject_geoms(shp, dstcrs='EPSG:4326', antimeridian_cutting=False):
    out = [update_geom(row, shape(
                                transform_geom(
                                    row['crs'], 
                                    dstcrs, 
                                    mapping(
                                            row['geometry']
                                            ),
                                     antimeridian_cutting=antimeridian_cutting)
                                )
                            )
                                            for idx,row in shp.iterrows()]
    return gpd.GeoDataFrame(out, crs=dstcrs)

def run(path='', filelist=None, wild="DEM/*.tif", ncpus=1, dstcrs=None, data_only=False):
    """
    run footprints across a path (using a wildcard for discovery) or (pre-baked) filelist 
    and output a geopandas.GeoDataFrame object containing the results.

    Arguments:
    ---------
    path: (PathLike, str, optional) path to parent directory to search using a recursive glob
            with `wild`.  default: ''
    filelist: (list) of (PathLike, str, optional) pre-baked path list to rasterio-readable raster
            objects to build footprints from. default: None.  If argument is used, this overrides
            `path` and `wild`
    wild: (str, optional) glob-like pattern to use in a recursive search of `path` for discovery 
            of files to build footprints from. default: 'DEM/*.tif'
    ncpus: (int, optional) number of cpu cores to use in building footprints. default: 1
    dstcrs: (str, optional) Proj6 like pattern describing the coordinate reference system to 
            reproject all footprint polygon objects to. if not given, function will return the 
            polygon objects in their native crs. default: None 
    data_only: (bool, optional) if True polygons will retun only the valid data area as determined 
                by the nodata property of the input raster. If False, returns the full extent of 
                the raster object. default: False

    Returns:
    --------
    gpd.GeoDataFrame of footprint polygons and attributes of the path to the location, native crs
    of the input raster. If `dstcrs` is not given, the CRS of the output GeoDataFrame will be that
    of the raster in the first row (potentially incorrect data contain multiple CRS's)

    """
    coverage = GetFootprints(
                    path, 
                    filelist,
                    wildcard=wild, 
                    data_only=data_only
                    ).footprints(ncpus=int(ncpus))

    gdf = gpd.GeoDataFrame(coverage)
    gdf.crs = gdf['crs'].iloc[0]
    if dstcrs is not None:
        antimeridian_cutting = True
        gdf = reproject_geoms(gdf, dstcrs, antimeridian_cutting)
    return gdf

def main():
    desc = ''' Generate Raster Coverage '''
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-p', dest='path', action="store", type=str, 
                                help='path to the folder of raster files to generate bboxes for')
    parser.add_argument('-w', dest='wild', action="store", type=str, 
                                help='wildcard used to glob for raster files to build footprints for.')
    parser.add_argument('-o', dest='outfn', action="store", type=str, 
                                help='path to the output file to be generated. (*.geojson)')
    parser.add_argument('-c', dest='dstcrs', action="store", nargs='?', default=None, type=str, 
                                help='destination CRS to reproject all geometries to for the outfn. \
                                    default: None')
    parser.add_argument('-d', dest='data_only', action="store", nargs='?', default=False, type=bool, 
                                help='if True: return polygons of the data extent within the raster, \
                                      if False, bounding box. default: False')
    parser.add_argument('-n', dest='ncpus', action="store", type=int, default=2, 
                                help='number of CPU-cores to be used.')

    # parse the CLI args
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    path = args.path
    wild = args.wild
    outfn = args.outfn
    dstcrs = args.dstcrs
    data_only = args.data_only
    ncpus = args.ncpus

    DRIVER = 'GeoJSON'

    gdf = run(path=path, wild=wild, ncpus=ncpus, dstcrs=dstcrs, data_only=data_only)
    gdf.to_file(outfn, driver=DRIVER)
    return 0

if __name__ == '__main__':
    main()