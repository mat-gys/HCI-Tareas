"""
Model exported as python.
Name : modelo3
Group : 
With QGIS : 32209
"""
# Se importan los paquetes de QGIS necesarios 
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing

# Se define una clase para el modelo3:
class Modelo3(QgsProcessingAlgorithm):
    # Creamos función que crea un destino para los outputs creados por los algoritmos, dentro de esta apareceran cada una de las ramificaciones de lo programado en QGIS
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Drop_fields_3', 'drop_fields_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_3', 'fixgeo_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Landq', 'landq', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1800', 'pop1800', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1900', 'pop1900', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop2000', 'pop2000', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
    # Creamos función principal
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(7, model_feedback)
        results = {}
        outputs = {}


        # #######################################
        # Fix geometries
        # #######################################          
        # Fijamos el shapefile de countries con el que se trabaja
        alg_params = {
            'INPUT': 'C:/Users/Hp Support/Videos/03 - Cursos/05 - Herramientas computacionales/Clase 4 - Python-QGIS/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixgeo_3']
        }
        # Procesamos el INPUT a traves del método 'native:fixgeometries', esto se almacena en diccionario outputs con la key "Fixgeo_3"
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_3'] = outputs['FixGeometries']['OUTPUT']
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
                        
        # #######################################
        # Drop files
        # #######################################  
        # Procedemos a borrar las variables que consideramos innecesarias
        
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'],
            'INPUT': 'Fixed_geometries_275d5cb4_7652_4174_9aa9_f48fd74bce04',
            'OUTPUT': parameters['Drop_fields_3']
        }
        # Procesamos el INPUT a traves del método 'native:deletecolumn', esto se almacena en diccionario outputs con la key "Drop_fields_3"
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Drop_fields_3'] = outputs['DropFields']['OUTPUT']
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Zonal statistics
        # #######################################  
        # Procedemos a calcular un promedio a nivel de los países tomando el raster de Landquality, esto lo hicimos para el resto de rasters. 
        # se podría crear un loop para realizar el proceso iterativamente y no parte por parte como lo realiza QGIS. 
        alg_params = {
            'COLUMN_PREFIX': '_',
            'INPUT': 'Remaining_fields_062d8752_4ed2_4324_b8e4_8e01eb899bd2',
            'INPUT_RASTER': 'landquality_cf8c6f74_656e_4c31_879b_13fa2214ea98',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Landq']
        }
        # Procesamos el INPUT a traves del método 'native:zonalstatisticsfb', esto se almacena en diccionario outputs con la key "Landq"
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Landq'] = outputs['ZonalStatistics']['OUTPUT']
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}        
        
        
        # #######################################
        # Zonal statistics
        # #######################################  
        # Procedemos a calcular un promedio a nivel de los países tomando el raster de pop1800, esto lo hicimos para el resto de rasters. 
        # se podría crear un loop para realizar el proceso iterativamente y no parte por parte como lo realiza QGIS. 
        alg_params = {
            'COLUMN_PREFIX': 'pop1800',
            'INPUT': 'Zonal_Statistics_535a126b_e830_4e8d_81a8_f6476601e7e2',
            'INPUT_RASTER': 'popd_1800AD_8251ddf8_4134_48d5_bbc4_4cfcaff92ac9',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Pop1800']
        }
        # Procesamos el INPUT a traves del método 'native:zonalstatisticsfb', esto se almacena en diccionario outputs con la key "Pop1800"        
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1800'] = outputs['ZonalStatistics']['OUTPUT']
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}        
        
        # #######################################
        # Zonal statistics
        # #######################################  
        # Procedemos a calcular un promedio a nivel de los países tomando el raster de pop1900, esto lo hicimos para el resto de rasters. 
        # se podría crear un loop para realizar el proceso iterativamente y no parte por parte como lo realiza QGIS. 
        alg_params = {
            'COLUMN_PREFIX': 'pop1900',
            'INPUT': 'Zonal_Statistics_42648998_8c7c_4398_98b8_89af6cf1c85d',
            'INPUT_RASTER': 'popd_1900AD_6a5d57e5_74db_4f69_83f6_301ba0e47f9b',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Pop1900']
        }
        # Procesamos el INPUT a traves del método 'native:zonalstatisticsfb', esto se almacena en diccionario outputs con la key "Pop1900"        
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1900'] = outputs['ZonalStatistics']['OUTPUT']
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Zonal statistics
        # #######################################        
        # Procedemos a calcular un promedio a nivel de los países tomando el raster de pop2000, esto lo hicimos para el resto de rasters. 
        # se podría crear un loop para realizar el proceso iterativamente y no parte por parte como lo realiza QGIS.         
        alg_params = {
            'COLUMN_PREFIX': 'pop2000',
            'INPUT': 'Zonal_Statistics_8a562c86_5f34_4bc7_8cca_7f1814da9923',
            'INPUT_RASTER': 'popd_2000AD_62a7897f_d2f9_4a72_8596_e6ba70405cb4',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Pop2000']
        }
        # Procesamos el INPUT a traves del método 'native:zonalstatisticsfb', esto se almacena en diccionario outputs con la key "Pop2000"          
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop2000'] = outputs['ZonalStatistics']['OUTPUT']
        # Le digo en que paso del algoritmo estoy para dividirlo en distintos child steps, si algo salió mal, devuelve nada
        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # #######################################
        # Save vector features to file
        # #######################################          
        # Esto nos permite guardar toda la información en forma de archivo csv. 
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': 'Zonal_Statistics_ea3702fd_07b6_4f0d_913e_5711d6e62fc2',
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': 'C:/Users/Hp Support/Videos/03 - Cursos/05 - Herramientas computacionales/Clase 4 - Python-QGIS/Tarea/output/raster_stats.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SaveVectorFeaturesToFile'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)        
        return results

    def name(self):
        return 'modelo3'

    def displayName(self):
        return 'modelo3'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo3()
