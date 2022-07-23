"""
Model exported as python.
Name : modelo4c
Group : 
With QGIS : 32203
"""

# Importamos paquetes de QGIS necesarios
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsCoordinateReferenceSystem
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

areas_out = "{}\\areas_out.csv".format(outpath)

# Definimos una clase
class Modelo4c(QgsProcessingAlgorithm):
    # Creamos función que crea un destino para los outputs creados por los algoritmos
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_drop_fields', 'countries_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Areas_out', 'areas_out', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_fixgeo', 'countries_fixgeo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_reprojected', 'countries_reprojected', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
    
    # Creamos función principal
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        # Esto es para poder obtener feedback sobre cada paso del modelo más adelante
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        # Creo los diccionarios para guardar resultados y outputs
        results = {}
        outputs = {}

        # #######################################
        # Drop field(s)
        # #######################################
        # Creamos diccionario con parametros a utilizar en Drop field(s) (hay más opciones para agregar si queremos)
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'], # Columnas a droppear
            'INPUT': countriesin, # Usamos countriesin como input
            'OUTPUT': parameters['Countries_drop_fields']
        }
        # Procesamos el INPUT a traves del método 'native:deletecolumn', lo guardamos en diccionario outputs con la key "DropFields"
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Countries_drop_fields"
        results['Countries_drop_fields'] = outputs['DropFields']['OUTPUT']

        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Reproject layer
        # #######################################
        # Creamos diccionario con parametros a utilizar en Reproject layer (hay más opciones para agregar si queremos)
        alg_params = {
            'INPUT': outputs['DropFields']['OUTPUT'], # Usamos ouput de DropFields como input
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('ESRI:54034'), # Tipo de proyeccion a utilizar
            'OUTPUT': parameters['Countries_reprojected']
        }
        # Procesamos el INPUT a traves del método 'native:reprojectlayer', lo guardamos en diccionario outputs con la key "ReprojectLayer"
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Countries_reprojected"
        results['Countries_reprojected'] = outputs['ReprojectLayer']['OUTPUT']

        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Fix geometries
        # #######################################
        # Creamos diccionario con parametros a utilizar en Fix geometries (hay más opciones para agregar si queremos)
        alg_params = {
            'INPUT': outputs['ReprojectLayer']['OUTPUT'], # Usamos ouput de ReprojectLayer como input
            'OUTPUT': parameters['Countries_fixgeo']
        }
        # Procesamos el INPUT a traves del método 'native:fixgeometries', lo guardamos en diccionario outputs con la key "FixGeometries"
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Countries_fixgeo"
        results['Countries_fixgeo'] = outputs['FixGeometries']['OUTPUT']

        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Field calculator
        # #######################################
        # Creamos diccionario con parametros a utilizar en Field calculator (hay más opciones para agregar si queremos)
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'km2area', # Nombre de nuevo attribute
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'area($geometry)/1000000', # Calculo a realizar
            'INPUT': outputs['FixGeometries']['OUTPUT'], # Usamos ouput de FixGeometries como input
            'OUTPUT': parameters['Areas_out']
        }
        # Procesamos el INPUT a traves del método 'native:fieldcalculator', lo guardamos en diccionario outputs con la key "FieldCalculator"
        outputs['FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results con la key "Areas_out"
        results['Areas_out'] = outputs['FieldCalculator']['OUTPUT']

        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Save vector features to file
        # #######################################
        # Creamos diccionario con parametros a utilizar en Save vector features to file (hay más opciones para agregar si queremos)
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': outputs['FieldCalculator']['OUTPUT'], # Usamos ouput de FieldCalculator como input
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': areas_out, # Lo guardo como csv con nombre areas_out
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        # Procesamos el INPUT a traves del método 'native:savefeatures', lo guardamos en diccionario outputs con la key "SaveVectorFeaturesToFile"
        outputs['SaveVectorFeaturesToFile'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Devuelve diccionario results
        return results

    def name(self):
        return 'modelo4c'

    def displayName(self):
        return 'modelo4c'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo4c()
