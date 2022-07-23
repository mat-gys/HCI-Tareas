"""
Model exported as python.
Name : model4b
Group : 
With QGIS : 32203
"""

# Importamos paquetes de QGIS necesarios
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorDestination
from qgis.core import QgsProcessingParameterFeatureSink
import processing

# Set input and output paths
# Esto requiere un directorio con el siguiente formato:
##  main-
##     \-input
##     \-output
mainpath = "C:\\Users\\Matias\\Documents\\UDESA\\Herramientas computacionales\\Clase 4"
inpath = "{}\\input".format(mainpath)
outpath = "{}\\output".format(mainpath)

countriesin = "{}\\ne_10m_admin_0_countries.shp".format(inpath)
coastin = "{}\\ne_10m_coastline.shp".format(inpath)

csvout = "{}\\csvout.csv".format(outpath)

# Definimos una clase
class Model4b(QgsProcessingAlgorithm):
    # Creamos función que crea un destino para los outputs creados por los algoritmos
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorDestination('Distout', 'distout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('Nearout', 'nearout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Country_centroids', 'country_centroids', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Coastout', 'coastout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroidsout', 'centroidsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust_dropfields', 'nearest_cat_adjust_dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroid_nearest_coast_joined_dropfields', 'centroid_nearest_coast_joined_dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_lat_lon_drop_fields', 'centroids_lat_lon_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_by_attribute', 'extract_by_attribute', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_vertices', 'extract_vertices', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust', 'nearest_cat_adjust', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lat', 'added_field_cent_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lon', 'added_field_cent_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lat', 'added_field_coast_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lon', 'added_field_coast_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_coast', 'fixgeo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroidsnearestcoastjoined', 'centroids.nearest.coast.joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_distance_joined', 'centroids_nearest_coast_distance_joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_w_coordinates', 'centroids_w_coordinates', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Add_geo_coast', 'add_geo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
    
    # Creamos función principal
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        # Esto es para poder obtener feedback sobre cada paso del modelo más adelante
        feedback = QgsProcessingMultiStepFeedback(21, model_feedback)
        # Creo los diccionarios para guardar resultados y outputs
        results = {}
        outputs = {}

        # #######################################
        # Fix geometries - countries
        # #######################################
        # Creamos diccionario con parametros a utilizar en Fix geometries (hay más opciones para agregar si queremos), en este caso solo el input y output
        alg_params = {
            'INPUT': countriesin,
            'OUTPUT': parameters['Fixgeo_countries']
        }
        # Procesamos el INPUT a traves del método 'native:fixgeometries', lo guardamos en diccionario outputs con la key "FixGeometriesCountries"
        outputs['FixGeometriesCountries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Fixgeo_countries"
        results['Fixgeo_countries'] = outputs['FixGeometriesCountries']['OUTPUT']
        
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Centroids
        # #######################################
        # Creamos diccionario con parametros a utilizar en Centroids (hay más opciones para agregar si queremos)
        alg_params = {
            'ALL_PARTS': False, # Para que no calcule centroide de cada parte de la geometria
            'INPUT': outputs['FixGeometriesCountries']['OUTPUT'], # Uso el output del anterior algoritmo
            'OUTPUT': parameters['Country_centroids']
        }
        # Procesamos el INPUT a traves del método 'native:centroids', lo guardamos en diccionario outputs con la key "Centroids"
        outputs['Centroids'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Fixgeo_countries"
        results['Country_centroids'] = outputs['Centroids']['OUTPUT']
        
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Fix geometries - coast
        # #######################################
        # Creamos diccionario con parametros a utilizar en Fix geometries (hay más opciones para agregar si queremos), en este caso solo el input y output
        alg_params = {
            'INPUT': coastin,
            'OUTPUT': parameters['Fixgeo_coast']
        }
        # Procesamos el INPUT a traves del método 'native:fixgeometries', lo guardamos en diccionario outputs con la key "FixGeometriesCoast"
        outputs['FixGeometriesCoast'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Fixgeo_coast"
        results['Fixgeo_coast'] = outputs['FixGeometriesCoast']['OUTPUT']
        
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Field calculator - nearest cat
        # #######################################
        # Creamos diccionario con parametros a utilizar en Field calculator (hay más opciones para agregar si queremos)
        alg_params = {
            'FIELD_LENGTH': 4,
            'FIELD_NAME': 'cat',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': "attribute($currentfeature, 'cat')-1\r\n", # Estamos sobreescribiendo cat bajandole el valor en 1
            'INPUT': parameters["Nearout"], # Usamos output de v.distance
            'OUTPUT': parameters['Nearest_cat_adjust']
        }
        # Procesamos el INPUT a traves del método 'native:fieldcalculator', lo guardamos en diccionario outputs con la key "FieldCalculatorNearestCat"
        outputs['FieldCalculatorNearestCat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Nearest_cat_adjust"
        results['Nearest_cat_adjust'] = outputs['FieldCalculatorNearestCat']['OUTPUT']
        
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Add geometry attributes
        # #######################################
        # Creamos diccionario con parametros a utilizar en Add geometry attributes (hay más opciones para agregar si queremos)
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': outputs['Centroids']['OUTPUT'], # Usamos output de Centroids como input
            'OUTPUT': parameters['Centroids_w_coordinates']
        }
        # Procesamos el INPUT a traves del método 'qgis:exportaddgeometrycolumns', lo guardamos en diccionario outputs con la key "AddGeometryAttributes"
        outputs['AddGeometryAttributes'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Centroids_w_coordinates"
        results['Centroids_w_coordinates'] = outputs['AddGeometryAttributes']['OUTPUT']
        
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}
        
        # #######################################
        # Drop field(s) - centroids_w_coordinates
        # #######################################
        # Creamos diccionario con parametros a utilizar en Drop field(s) (hay más opciones para agregar si queremos)
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'], # Columnas a borrar
            'INPUT': outputs['AddGeometryAttributes']['OUTPUT'],
            'OUTPUT': parameters['Centroidsout']
        }
        # Procesamos el INPUT a traves del método 'native:deletecolumn', lo guardamos en diccionario outputs con la key "DropFieldsCentroids_w_coordinates"
        outputs['DropFieldsCentroids_w_coordinates'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Centroidsout"
        results['Centroidsout'] = outputs['DropFieldsCentroids_w_coordinates']['OUTPUT']
        
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Drop field(s) - nearest_cat_adjust
        # #######################################
        # Creamos diccionario con parametros a utilizar en Drop field(s) (hay más opciones para agregar si queremos)
        alg_params = {
            'COLUMN': ['xcoord','ycoord'], # Columnas a dropear
            'INPUT': outputs['FieldCalculatorNearestCat']['OUTPUT'], # Usamos output de FieldCalculatorNearestCat como input
            'OUTPUT': parameters['Nearest_cat_adjust_dropfields']
        }
        # Procesamos el INPUT a traves del método 'native:deletecolumn', lo guardamos en diccionario outputs con la key "DropFieldsNearest_cat_adjust"
        outputs['DropFieldsNearest_cat_adjust'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Nearest_cat_adjust_dropfields"
        results['Nearest_cat_adjust_dropfields'] = outputs['DropFieldsNearest_cat_adjust']['OUTPUT']
        
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Drop field(s) - fixgeo_coast
        # #######################################
        # Creamos diccionario con parametros a utilizar en Drop field(s) (hay más opciones para agregar si queremos)
        alg_params = {
            'COLUMN': ['scalerank'], # Columnas a dropear
            'INPUT': outputs['FixGeometriesCoast']['OUTPUT'], # Usamos output de FixGeometriesCoast
            'OUTPUT': parameters['Coastout']
        }
        # Procesamos el INPUT a traves del método 'native:deletecolumn', lo guardamos en diccionario outputs con la key "DropFieldsFixgeo_coast"
        outputs['DropFieldsFixgeo_coast'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Coastout"
        results['Coastout'] = outputs['DropFieldsFixgeo_coast']['OUTPUT']
        
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Join attributes by field value - centroids_coast_joined
        # #######################################
        # Creamos diccionario con parametros a utilizar en Join attributes by field value (hay más opciones para agregar si queremos)
        alg_params = {
            'DISCARD_NONMATCHING': False, # Si descartar las que no coinciden
            'FIELD': 'ISO_A3', # Field a utilizar para el join en primer input
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'ISO_A3', # Field a utilizar para el join en segundo input
            'INPUT': outputs['DropFieldsCentroids_w_coordinates']['OUTPUT'], # Usamos output de DropFieldsCentroids_w_coordinates como primer input
            'INPUT_2': outputs['DropFieldsNearest_cat_adjust']['OUTPUT'], # Usamos output de DropFieldsNearest_cat_adjust como segundo input
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '', # Prefijo a utilizar
            'OUTPUT': parameters['Centroidsnearestcoastjoined']
        }
        # Procesamos el INPUT a traves del método 'native:joinattributestable', lo guardamos en diccionario outputs con la key "JoinAttributesByFieldValueCentroids_coast_joined"
        outputs['JoinAttributesByFieldValueCentroids_coast_joined'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Centroidsnearestcoastjoined"
        results['Centroidsnearestcoastjoined'] = outputs['JoinAttributesByFieldValueCentroids_coast_joined']['OUTPUT']
        
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # #######################################
        # v.distance
        # #######################################
        # Creamos diccionario con parametros a utilizar en v.distance (hay más opciones para agregar si queremos)
        alg_params = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,  # auto
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'column': ['xcoord'],
            'dmax': -1,
            'dmin': -1,
            'from': outputs['DropFieldsCentroids_w_coordinates']['OUTPUT'], # Usamos output de DropFieldsCentroids_w_coordinates como input
            'from_type': [0,1,3],  # point,line,area
            'to': outputs['DropFieldsFixgeo_coast']['OUTPUT'], # Usamos output de DropFieldsFixgeo_coast como input
            'to_column': '',
            'to_type': [0,1,3],  # point,line,area
            'upload': [0],  # cat
            'from_output': parameters['Nearout'],
            'output': parameters['Distout']
        }
        # Procesamos el INPUT a traves del método 'grass7:v.distance', lo guardamos en diccionario outputs con la key "Vdistance"
        outputs['Vdistance'] = processing.run('grass7:v.distance', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Distout"
        results['Distout'] = outputs['Vdistance']['output']
        # Guardamos el output en el diccionario results con la key "Nearout"
        results['Nearout'] = outputs['Vdistance']['from_output']
        
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Drop field(s) - centroid_coast_joined
        # #######################################
        # Creamos diccionario con parametros a utilizar en Drop field(s) (hay más opciones para agregar si queremos)
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA','ADMIN_2','ISO_A3_2'], # Columnas a droppear
            'INPUT': outputs['JoinAttributesByFieldValueCentroids_coast_joined']['OUTPUT'], # Usamos output de JoinAttributesByFieldValueCentroids_coast_joined como input
            'OUTPUT': parameters['Centroid_nearest_coast_joined_dropfields']
        }
        # Procesamos el INPUT a traves del método 'native:deletecolumn', lo guardamos en diccionario outputs con la key "DropFieldsCentroid_coast_joined"
        outputs['DropFieldsCentroid_coast_joined'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Centroid_nearest_coast_joined_dropfields"
        results['Centroid_nearest_coast_joined_dropfields'] = outputs['DropFieldsCentroid_coast_joined']['OUTPUT']

        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Join attributes by field value - distance joined
        # #######################################
        # Creamos diccionario con parametros a utilizar en Join attributes by field value (hay más opciones para agregar si queremos)
        alg_params = {
            'DISCARD_NONMATCHING': False, # Si descartar las que no coinciden
            'FIELD': 'cat', # Field a utilizar para el join en primer input
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cat', # Field a utilizar para el join en segundo input
            'INPUT': outputs['Vdistance']['output'], # Usamos output de Vdistance como primer input (el Distout)
            'INPUT_2': outputs['DropFieldsCentroid_coast_joined']['OUTPUT'], # Usamos output de DropFieldsCentroid_coast_joined como segundo input (el Distout)
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '', # Prefijo a utilizar
            'OUTPUT': parameters['Centroids_nearest_coast_distance_joined']
        }
        # Procesamos el INPUT a traves del método 'native:joinattributestable', lo guardamos en diccionario outputs con la key "JoinAttributesByFieldValueDistanceJoined"
        outputs['JoinAttributesByFieldValueDistanceJoined'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Centroids_nearest_coast_distance_joined"
        results['Centroids_nearest_coast_distance_joined'] = outputs['JoinAttributesByFieldValueDistanceJoined']['OUTPUT']

        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Extract vertices
        # #######################################
        # Creamos diccionario con parametros a utilizar en Extract vertices (hay más opciones para agregar si queremos)
        alg_params = {
            'INPUT': outputs['JoinAttributesByFieldValueDistanceJoined']['OUTPUT'],  # Usamos output de JoinAttributesByFieldValueDistanceJoined como input
            'OUTPUT': parameters['Extract_vertices']
        }
        # Procesamos el INPUT a traves del método 'native:extractvertices', lo guardamos en diccionario outputs con la key "ExtractVertices"
        outputs['ExtractVertices'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Centroids_nearest_coast_distance_joined"
        results['Extract_vertices'] = outputs['ExtractVertices']['OUTPUT']

        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Extract by attribute
        # #######################################
        # Creamos diccionario con parametros a utilizar en Extract by attribute (hay más opciones para agregar si queremos)
        alg_params = {
            'FIELD': 'distance', # Usamos distance como criterio
            'INPUT': outputs['ExtractVertices']['OUTPUT'], # Usamos output de ExtractVertices como input
            'OPERATOR': 2,  # >
            'VALUE': '0', # Entonces, crea un nuevo vector con aquellos fields con distance > 0
            'OUTPUT': parameters['Extract_by_attribute']
        }
        # Procesamos el INPUT a traves del método 'native:extractbyattribute', lo guardamos en diccionario outputs con la key "ExtractByAttribute"
        outputs['ExtractByAttribute'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Extract_by_attribute"
        results['Extract_by_attribute'] = outputs['ExtractByAttribute']['OUTPUT']

        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Field calculator - cent_lat
        # #######################################
        # Creamos diccionario con parametros a utilizar en Field calculator (hay más opciones para agregar si queremos)
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lat', # Nombre de nuevo attribute
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature, 'ycoord')", # es una copia de ycoord pero con 10 caracteres
            'INPUT': outputs['ExtractByAttribute']['OUTPUT'], # Usamos output de ExtractByAttribute como input
            'OUTPUT': parameters['Added_field_cent_lat']
        }
        # Procesamos el INPUT a traves del método 'native:fieldcalculator', lo guardamos en diccionario outputs con la key "FieldCalculatorCent_lat"
        outputs['FieldCalculatorCent_lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Added_field_cent_lat"
        results['Added_field_cent_lat'] = outputs['FieldCalculatorCent_lat']['OUTPUT']

        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Field calculator - cent_lon
        # #######################################
        # Creamos diccionario con parametros a utilizar en Field calculator (hay más opciones para agregar si queremos)
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lon', # Nombre de nuevo attribute
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature, 'xcoord')", # es una copia de ycoord pero con 10 caracteres
            'INPUT': outputs['FieldCalculatorCent_lat']['OUTPUT'], # Usamos output de FieldCalculatorCent_lat como input
            'OUTPUT': parameters['Added_field_cent_lon']
        }
        # Procesamos el INPUT a traves del método 'native:fieldcalculator', lo guardamos en diccionario outputs con la key "FieldCalculatorCent_lon"
        outputs['FieldCalculatorCent_lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Added_field_cent_lon"
        results['Added_field_cent_lon'] = outputs['FieldCalculatorCent_lon']['OUTPUT']

        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Drop field(s) - cent_lat_lon
        # #######################################
        # Creamos diccionario con parametros a utilizar en Drop field(s) (hay más opciones para agregar si queremos)
        alg_params = {
            'COLUMN': ['fid','cat','xcoord','ycoord','fid_2','cat_2','vertex_index','vertex_part','vertex_part','_index','angle'], # Columnas a droppear
            'INPUT': outputs['FieldCalculatorCent_lon']['OUTPUT'], # Usamos output de FieldCalculatorCent_lon como input
            'OUTPUT': parameters['Centroids_lat_lon_drop_fields']
        }
        # Procesamos el INPUT a traves del método 'native:deletecolumn', lo guardamos en diccionario outputs con la key "DropFieldsCent_lat_lon"
        outputs['DropFieldsCent_lat_lon'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Centroids_lat_lon_drop_fields"
        results['Centroids_lat_lon_drop_fields'] = outputs['DropFieldsCent_lat_lon']['OUTPUT']

        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Add geometry attributes - geo_coast
        # #######################################
        # Creamos diccionario con parametros a utilizar en Add geometry attributes (hay más opciones para agregar si queremos)
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': outputs['DropFieldsCent_lat_lon']['OUTPUT'], # Usamos output de DropFieldsCent_lat_lon como input
            'OUTPUT': parameters['Add_geo_coast']
        }
        # Procesamos el INPUT a traves del método 'qgis:exportaddgeometrycolumns', lo guardamos en diccionario outputs con la key "AddGeometryAttributesGeo_coast"
        outputs['AddGeometryAttributesGeo_coast'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Add_geo_coast"
        results['Add_geo_coast'] = outputs['AddGeometryAttributesGeo_coast']['OUTPUT']

        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Field calculator - coast_lat
        # #######################################
        # Creamos diccionario con parametros a utilizar en Field calculator (hay más opciones para agregar si queremos)
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lat', # Nombre de nuevo attribute
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature, 'ycoord')", # Es una copia de ycoord pero con 10 caracteres
            'INPUT': outputs['AddGeometryAttributesGeo_coast']['OUTPUT'], # Usamos output de AddGeometryAttributesGeo_coast como input
            'OUTPUT': parameters['Added_field_coast_lat']
        }
        # Procesamos el INPUT a traves del método 'native:fieldcalculator', lo guardamos en diccionario outputs con la key "FieldCalculatorCoast_lat"
        outputs['FieldCalculatorCoast_lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Added_field_coast_lat"
        results['Added_field_coast_lat'] = outputs['FieldCalculatorCoast_lat']['OUTPUT']

        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Field calculator - coast_lon
        # #######################################
        # Creamos diccionario con parametros a utilizar en Field calculator (hay más opciones para agregar si queremos)
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lon', # Nombre de nuevo attribute
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature, 'xcoord')", # Es una copia de xcoord pero con 10 caracteres
            'INPUT': outputs['FieldCalculatorCoast_lat']['OUTPUT'], # Usamos output de FieldCalculatorCoast_lat como input
            'OUTPUT': parameters['Added_field_coast_lon']
        }
        # Procesamos el INPUT a traves del método 'native:fieldcalculator', lo guardamos en diccionario outputs con la key "FieldCalculatorCoast_lon"
        outputs['FieldCalculatorCoast_lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Added_field_coast_lon"
        results['Added_field_coast_lon'] = outputs['FieldCalculatorCoast_lon']['OUTPUT']

        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Drop field(s) - coast_lon
        # #######################################
        # Creamos diccionario con parametros a utilizar en Drop field(s) (hay más opciones para agregar si queremos)
        alg_params = {
            'COLUMN': ['xcoord','ycoord'], # Columnas a droppear
            'INPUT': outputs['FieldCalculatorCoast_lon']['OUTPUT'], # Usamos output de FieldCalculatorCoast_lon como input
            'OUTPUT': csvout, # Lo guardamos como csv en la carpeta output con el nombre csvout
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        # Procesamos el INPUT a traves del método 'native:deletecolumn', lo guardamos en diccionario outputs con la key "DropFieldsCoast_lon"
        outputs['DropFieldsCoast_lon'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Devuelve diccionario results
        return results

    def name(self):
        return 'model4b'

    def displayName(self):
        return 'model4b'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4b()
