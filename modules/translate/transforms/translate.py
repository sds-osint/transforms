from extensions import translate_registry
from maltego_trx.entities import *
from maltego_trx.maltego import UIM_TYPES, MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
from settings import deepl_auth_key
import deepl
import csv
import random

@translate_registry.register_transform(
    display_name="Translate Phrase", 
    input_entity="maltego.Unknown",
    description='Uses DeepL to translate the text and updates the entity with translation details.',
    output_entities=["maltego.Unknown"]
)

class translate(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # api_key = request.getTransformSetting(deepl_auth_key.id)
        og_text = request.Value
        og_type = str(request.Type)

        with open ('modules/translate/assets/deepl_keys.csv', 'r') as file:
            reader = csv.reader(file)
            keys = [row[0] for row in reader] 

        api_key = random.choice(keys)

        # Attempt translation and handle potential exceptions
        try:
            translator = deepl.Translator(api_key)
            translated_text = translator.translate_text(og_text, target_lang='EN-US')
            input_lang = translated_text.detected_source_lang

            # Since updating the original is not directly supported, create a mirrored entity with added properties
            og_entity = response.addEntity(request.Type, og_text)
            og_entity.addProperty(fieldName='translated_text', displayName='Translated Text', value=translated_text.text)
            og_entity.addProperty(fieldName='source_lang', displayName='Source Language', value=input_lang)

            # Optionally, add UI messages for user feedback
            response.addUIMessage(f"Translated from {input_lang} to EN-US.")

            translated_entity = response.addEntity(request.Type, translated_text)
            translated_entity.addProperty(fieldName='text', displayName='Text', value=translated_text.text)
            translated_entity.setLinkLabel(f'Translated: {input_lang} to EN')
        
        except Exception as e:
            response.addUIMessage(f"Error during translation: {str(e)}")