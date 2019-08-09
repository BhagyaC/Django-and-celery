import spacy
import logging

logger = logging.getLogger(__name__)


class SpacySingleton(object):
    __instance = None
    __create_key = object()

    def __init__(self, create_key):
        """ Virtually private constructor. """

        # Model to load
        SPACY_MODEL = "en_core_web_md"

        # Ensure singleton can only be instantiated though get_instance() method
        assert (create_key == SpacySingleton.__create_key), \
            "SpacySingleton object must be created using SpacySingleton.get_instance() method"

        if SpacySingleton.__instance is not None:
            raise Exception("SpacySingleton can only be initialized once!")
        else:
            logger.info('Loading spacy model {}'.format(SPACY_MODEL))
            self.spacy_nlp = spacy.load(SPACY_MODEL)
            logger.info('Loading spacy model complete!')
            SpacySingleton.__instance = self

    @classmethod
    def get_instance(cls):
        """ Static access method. """
        if SpacySingleton.__instance is None:
            SpacySingleton(cls.__create_key)
        return SpacySingleton.__instance


def get_spacy_nlp() -> spacy:
    nlp = SpacySingleton.get_instance().spacy_nlp
    return nlp
