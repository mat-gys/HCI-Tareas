"""
Model exported as python.
Name : modelo2
Group : 
With QGIS : 32209
"""
# Se importan los paquetes de QGIS necesarios 
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsCoordinateReferenceSystem
import processing

# Se define una clase para el modelo1:
class Modelo2(QgsProcessingAlgorithm):
    # Creamos función que crea un destino para los outputs creados por los algoritmos, dentro de esta apareceran cada una de las ramificaciones de lo programado en QGIS
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterDestination('Suitout', 'suitout', createByDefault=True, defaultValue=None))
    # Creamos función principal
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # #######################################
        # Warp (reproject)
        # #######################################           
        # Procedemos a proyectar el raster hdr.adf que se guarde en un archivo tipo diccionario suitout.
        alg_params = {
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': '',
            'INPUT': 'C:/Users/Hp Support/Videos/03 - Cursos/05 - Herramientas computacionales/Clase 4 - Python-QGIS/SUIT/suit/hdr.adf',
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,  # Nearest Neighbour
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['Suitout']
        }
        # Procesamos el INPUT a traves del método 'gdal:warpreproject', esto se almacena en un diccionario outputs con la key "Suitout"
        outputs['WarpReproject'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Suitout'] = outputs['WarpReproject']['OUTPUT']
        
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Extract projection
        # Esto también nos permitió crear el archivo en formato prj. 
        alg_params = {
            'INPUT': outputs['WarpReproject']['OUTPUT'],
            'PRJ_FILE_CREATE': True
        }
        # Procesamos el INPUT a traves del método 'gdal:extractprojection'.
        outputs['ExtractProjection'] = processing.run('gdal:extractprojection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'modelo2'

    def displayName(self):
        return 'modelo2'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo2()
