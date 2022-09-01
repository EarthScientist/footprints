### footprints
---

#### Purpose
this package intends to simplify the generation of 
'coverage' shapefiles of the footprint extents of raster
tiles that are adjacent or overlapping.

#### Installation:
First lets make a virtualenv (or alternatively `source`-in an existing one)
```sh
python3 -m venv ~/footprints
source ~/footprints/bin/activate
```

Install the `requirements.txt`:
```sh
pip install -r requirements.txt
```

Install the package itself:
```sh
cd ~/repos
git clone ssh://github.com/earthscientist/footprints.git
cd footprints
pip install . # or python setup.py install
```

#### Usage
A new command line keyword is now available to you when in the virtualenv where the package is installed named `footprints`.  This can be used at the CLI to generate a footprints .geojson layer from a directory of raster tiles.

```sh
(footprints) $ footprints
usage: footprints [-h] [-p PATH] [-w WILD] [-o OUTFN] [-c [DSTCRS]] [-d [DATA_ONLY]] [-n NCPUS]

Generate Raster Coverage

optional arguments:
  -h, --help      show this help message and exit
  -p PATH         path to the folder of raster files to generate bboxes for
  -w WILD         wildcard used to glob for raster files to build footprints for.
  -o OUTFN        path to the output file to be generated. (*.geojson)
  -c [DSTCRS]     destination CRS to reproject all geometries to for the outfn. default: None
  -d [DATA_ONLY]  if True: return polygons of the data extent within the raster, if False, bounding box. default:False
  -n NCPUS        number of CPU-cores to be used.
```

or we can leverage the CLI function above from within the python interpreter:
```python
from footprints import run

path = "/path/to/folder/of/rasters"
wild = "*.*"
ncpus=35
dstcrs="EPSG:4326"
data_only=False # valid data extent (True) or bounding rectangle(False).

gdf = run(path=path, wild=wild, ncpus=ncpus, dstcrs=None, data_only=False)
gdf.to_file(out_fn)
```

`run` can also be instantiated with a pre-baked list of file paths...

```python
from footprints import run

filelist = ["/path/to/raster1.tif", "/path/to/raster2.tif", "/path/to/raster3.tif"]
wild = "*.*"
ncpus=35
dstcrs="EPSG:4326"
data_only=False # valid data extent (True) or bounding rectangle(False).

gdf = run(filelist=filelist, wild=wild, ncpus=ncpus, dstcrs=None, data_only=False)
gdf.to_file(out_fn)
```
note the explicit use of the `argname=value` above. This is needed to handle these different, but similar
use-cases. 