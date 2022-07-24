"""
Model exported as python.
Name : modelo1
Group : 
With QGIS : 32209
"""
# Se importan los paquetes de QGIS necesarios 
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing

# Se define una clase para el modelo1:
class Modelo1(QgsProcessingAlgorithm):
    # Creamos función que crea un destino para los outputs creados por los algoritmos, dentro de esta apareceran cada una de las ramificaciones de lo programado en QGIS
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Autoinc_id', 'autoinc_id', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Wldsout', 'wldsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Length', 'length', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Field_calc', 'field_calc', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output_menor_a_11', 'OUTPUT_menor_a_11', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_geo', 'fix_geo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
    # Creamos función principal
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback)
        results = {}
        outputs = {}

        # #######################################
        # Feature filter
        # #######################################        

        # Procedemos a realizar el filtro de la información, quedandonos con la información que cumpla que length<11
        # el resultado de este proceso se guardará en nuevo archivo o diccionario denominado OUTPUT_menor_a_11
        alg_params = {
            'INPUT': 'Calculado_5c4a16ba_30f2_4b13_89fd_8a1f5924d336',
            'OUTPUT_menor_a_11': parameters['Output_menor_a_11']
        }
        # Procesamos el INPUT a traves del método 'native:filter', esto se almacena en diccionario outputs con la key "FeatureFilter"
        outputs['FeatureFilter'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        # Guardamos el output en el diccionario results
        results['Output_menor_a_11'] = outputs['FeatureFilter']['OUTPUT_menor_a_11']
        
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Drop field(s): Eliminamos las columnas tomando como referencia los nombres de las mismas: 
        alg_params = {
            'COLUMN': ['ID_ISO_A3','ID_ISO_A2','ID_FIPS','NAM_LABEL','NAME_PROP','NAME2','NAM_ANSI','CNT','C1','POP','LMP_POP1','G','LMP_CLASS','FAMILYPROP','FAMILY','langpc_km2','length'],
            'INPUT': 'Calculado_79570d2b_7538_49d3_b7cb_7383eeb2a42e',
            'OUTPUT': parameters['Wldsout']
        }
        # Procesamos el INPUT a traves del método 'native:deletecolumn', esto se almacena en diccionario outputs con la key "DropFields"
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Wldsout'] = outputs['DropFields']['OUTPUT']
        
        # Esto es igual que el caso anterior: se menciona que paso del algoritmo se encuentra y si algo sale mal, devuelve nada.
        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Calculadora de campos
        # #######################################        
        
        # Creamos diccionario con parametros a utilizar en Field calculator, lo que estamis haciendo es básicamente generar una nueva variable
        # llamada length en base a aplicar la función length a la variables NAME_PROP
        alg_params = {
            'FIELD_LENGTH': 2,
            'FIELD_NAME': 'length',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Entero
            'FORMULA': 'length(NAME_PROP)',
            'INPUT': 'Incrementado_05e2246b_6fc3_4ebb_bc97_f8cb2216f4d7',
            'OUTPUT': parameters['Length']
        }
        
        # El resultado de generar esta variable se realiza a través del método native:fieldcalculator y se guarda en Length
        outputs['CalculadoraDeCampos'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Length'] = outputs['CalculadoraDeCampos']['OUTPUT']
        
        # Esto es igual que el caso anterior: se menciona que paso del algoritmo se encuentra y si algo sale mal, devuelve nada.
        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
        
        # #######################################
        # Field calculator clone
        # #######################################        
        
        # Creamos diccionario con parametros a utilizar en Field calculator clone, es decir estaríamos generando la nueva variable llamada lnm en base a NAME_PROP
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'lnm',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Cadena
            'FORMULA': '"NAME_PROP"',
            'INPUT': 'menor_a_11_f8a51f42_024d_4e8f_8988_a3993b00a10f',
            'OUTPUT': parameters['Field_calc']
        }
        # El resultado de clonar la variable se realiza a través del método native:fieldcalculator y se guarda en Field_calc
        outputs['FieldCalculatorClone'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Field_calc'] = outputs['FieldCalculatorClone']['OUTPUT']
        
        # Esto es igual que el caso anterior: se menciona que paso del algoritmo se encuentra y si algo sale mal, devuelve nada.
        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}
        
        # #######################################
        # Corregir geometrías
        # #######################################
        
        alg_params = {
            'INPUT': 'C:/Users/Hp Support/Videos/03 - Cursos/05 - Herramientas computacionales/Clase 4 - Python-QGIS/langa/langa.shp',
            'OUTPUT': parameters['Fix_geo']
        }
        # El resultado de clonar la variable se realiza a través del método native:fixgeometries y se guarda en Field_geo
        outputs['CorregirGeometras'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo'] = outputs['CorregirGeometras']['OUTPUT']

        # Esto es igual que el caso anterior: se menciona que paso del algoritmo se encuentra y si algo sale mal, devuelve nada.     
        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Agregar campo que auto-incrementa
        # #######################################      
        # Creamos diccionario con parametros a utilizar en Field calculator clone, es decir estaríamos generando la nueva variable GID que enumera los idiomas     
        alg_params = {
            'FIELD_NAME': 'GID',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['CorregirGeometras']['OUTPUT'],
            'MODULUS': 0,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Autoinc_id']
        }
        outputs['AgregarCampoQueAutoincrementa'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Autoinc_id'] = outputs['AgregarCampoQueAutoincrementa']['OUTPUT']
        return results

    def name(self):
        return 'modelo1'

    def displayName(self):
        return 'modelo1'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo1()
