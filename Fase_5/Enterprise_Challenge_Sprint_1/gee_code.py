import ee
import geemap
import os

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize()

# Define region of interest (ROI) - Mato Grosso
roi = ee.Geometry.Rectangle([-60, -18, -52, -10])  # Adjust coordinates

# Load Sentinel-2 dataset
sentinel2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
    .filterBounds(roi) \
    .filterDate('2023-01-01', '2024-12-31') \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5))  # Only low cloud cover images

# Compute NDVI
def compute_ndvi(image):
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    return image.addBands(ndvi)

ndvi_collection = sentinel2.map(compute_ndvi)

# Get median NDVI for the selected time period
ndvi_median = ndvi_collection.select('NDVI').median()

# Visualize
Map = geemap.Map()
Map.addLayer(ndvi_median, {'min': 0, 'max': 1, 'palette': ['red', 'yellow', 'green']}, 'Median NDVI')
Map.centerObject(roi, 6)
output_path = os.path.join(os.path.dirname(__file__), "gee_code.html")
Map.to_html(output_path)

# Define field boundaries (replace with your actual shapefile)
fields = ee.FeatureCollection([ee.Feature(roi)])

# Calculate zonal stats (mean NDVI per field)
stats = ndvi_median.reduceRegions(
    collection=fields,
    reducer=ee.Reducer.mean(),
    scale=30
)

# Export to CSV or GeoJSON
task = ee.batch.Export.table.toDrive(
    collection=stats,
    description='NDVI_Stats',
    fileFormat='CSV'
)
task.start()
