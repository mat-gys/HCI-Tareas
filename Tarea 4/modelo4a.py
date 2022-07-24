"""
Model exported as python.
Name : modelo4a
Group : 
With QGIS : 32209
"""
# Se importan los paquetes de QGIS necesarios 
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing

# Se define una clase para el modelo4a:
class Modelo4a(QgsProcessingAlgorithm):
    # Creamos función que crea un destino para los outputs creados por los algoritmos, dentro de esta apareceran cada una de las ramificaciones de lo programado en QGIS
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_wlds', 'fixgeo_wlds', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Intersection', 'intersection', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
    # Creamos función principal
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        # #######################################
        # Fix geometries - wlds
        # #######################################          
        # Procedemos a fijar las geometrías del archivo shapefile clean. 
        alg_params = {
            'INPUT': 'C:/Users/Hp Support/Videos/03 - Cursos/05 - Herramientas computacionales/Clase 4 - Python-QGIS/Tarea/output/clean.shp',
            'OUTPUT': parameters['Fixgeo_wlds']
        }
        # Procesamos el INPUT a traves del método 'native:fixgeometries', esto se almacena en diccionario outputs con la key "Fixgeo_wlds"
        outputs['FixGeometriesWlds'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results
        results['Fixgeo_wlds'] = outputs['FixGeometriesWlds']['OUTPUT']
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada        
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}


        
        # #######################################
        # Fix geometries - countries
        # #######################################          
        # Al igual que en el caso anterior fijamos las geometrías del shapefile de countries
        alg_params = {
            'INPUT': 'C:/Users/Hp Support/Videos/03 - Cursos/05 - Herramientas computacionales/Clase 4 - Python-QGIS/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixgeo_countries']
        }
        # Procesamos el INPUT a traves del método 'native:fixgeometries', esto se almacena en diccionario outputs con la key "Fixgeo_countries"       
        outputs['FixGeometriesCountries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results
        results['Fixgeo_countries'] = outputs['FixGeometriesCountries']['OUTPUT']
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}


        # #######################################
        # Intersection
        # #######################################  
        # Realizamos la intersección de las dos bases de tal manera de quedarnos con la variable GID del input 'FixGeometriesWlds' y con la variable 
        # ADMIN del input FixGeometriesCountries
        alg_params = {
            'INPUT': outputs['FixGeometriesWlds']['OUTPUT'],
            'INPUT_FIELDS': ['GID'],
            'OVERLAY': outputs['FixGeometriesCountries']['OUTPUT'],
            'OVERLAY_FIELDS': ['ADMIN'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': parameters['Intersection']
        }
        # Procesamos el INPUT a traves del método 'native:intersection', esto se almacena en diccionario outputs con la key "Intersection"         
        outputs['Intersection'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results
        results['Intersection'] = outputs['Intersection']['OUTPUT']        
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
        
        
        # #######################################
        # Statistics by categories
        # #######################################            
        #  Básicamente estamos solicitando que nos cuente por ADMIN el número de idiomas por país y que el resultado se 
        # almacene en un archivo en formato csv llamado languages_by_country. 
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['ADMIN'],
            'INPUT': 'Intersection_bfc5d3fa_3f80_4490_9f30_609a9ef0dd08',
            'OUTPUT': 'C:/Users/Hp Support/Videos/03 - Cursos/05 - Herramientas computacionales/Clase 4 - Python-QGIS/Tarea/output/languages_by_country.csv',
            'VALUES_FIELD_NAME': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        # Procesamos el INPUT a traves del método 'qgis:statisticsbycategories'.         
        outputs['StatisticsByCategories'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'modelo4a'

    def displayName(self):
        return 'modelo4a'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo4a()
