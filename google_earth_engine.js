// Define the list of models
var models = ["CNRM-ESM2-1"]; 

// Define point for quarter-degree (0.25) spacing
var points = ee.FeatureCollection([
 ee.Feature(ee.Geometry.Point([-73.875, 40.875]), {name: 'P5'}),
]);

// Loop through each model and process
models.forEach(function(model) {
  var dataset = ee.ImageCollection('NASA/GDDP-CMIP6')
                  .filter(ee.Filter.date('1950-01-01', '2100-12-31'))
                  .filter(ee.Filter.eq('model', model))
                  .select(['tasmin', 'tasmax', 'tas', 'hurs', 'sfcWind', 'pr', 'rlds', 'rsds']);

  var sampled = dataset.map(function(image) {
    return image.sampleRegions({
      collection: points,
    }).map(function(feature) {
      return feature.set('time', image.date().format())
                    .set('model', model);  // Add model name to each feature
    });
  }).flatten();  // Convert list of feature collections into one

  // Export the sampled data for the current model
  Export.table.toDrive({
    collection: sampled,
    description: 'GDDP_CMIP6_PointSamples_' + model,
    fileNamePrefix: 'GDDP_CMIP6_' + model,
    fileFormat: 'CSV'
  });
});
