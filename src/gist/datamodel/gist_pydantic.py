from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.11.0"
version = "14.1.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'gist_linkml',
     'default_range': 'string',
     'description': 'gist  is a minimalist upper ontology created by Semantic Arts '
                    'for enterprise knowledge graph applications. This LinkML '
                    'schema (version 14.1.0) aggregates the gist modules: Core '
                    '(classes and properties), MediaTypes (IANA media type '
                    'instances), and PrefixDeclarations (SHACL namespace '
                    'bindings). Supplementary schemas gist_rdfs_annotations and '
                    'gist_sub_class_assertions are available for annotation '
                    'enrichment and OWL RL reasoner support.',
     'id': 'https://w3id.org/lmodel/gist',
     'imports': ['linkml:types',
                 './gist_core',
                 './gist_media_types',
                 './gist_prefix_declarations'],
     'license': 'CC-BY-4.0',
     'name': 'gist',
     'prefixes': {'gist': {'prefix_prefix': 'gist',
                           'prefix_reference': 'https://w3id.org/semanticarts/ns/ontology/gist/'},
                  'gist_linkml': {'prefix_prefix': 'gist_linkml',
                                  'prefix_reference': 'https://w3id.org/lmodel/gist/'},
                  'gistd': {'prefix_prefix': 'gistd',
                            'prefix_reference': 'https://w3id.org/semanticarts/ns/data/gist/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'media_app': {'prefix_prefix': 'media_app',
                                'prefix_reference': 'https://www.iana.org/assignments/media-types/application/'},
                  'media_img': {'prefix_prefix': 'media_img',
                                'prefix_reference': 'https://www.iana.org/assignments/media-types/image/'},
                  'media_txt': {'prefix_prefix': 'media_txt',
                                'prefix_reference': 'https://www.iana.org/assignments/media-types/text/'}},
     'see_also': ['https://www.semanticarts.com/gist/',
                  'https://w3id.org/semanticarts/ontology/gistCore',
                  'https://lmodel.github.io/gist'],
     'source': 'https://w3id.org/semanticarts/ontology/gistCore',
     'source_file': 'src/gist/schema/gist.yaml',
     'title': 'gist (LinkML rendering)'} )

class AspectInstance(str, Enum):
    """
    Named instances of gist:Aspect from gist reference data.
    """
    altitude = "ASPECT_ALTITUDE"
    """
    The aspect altitude.
    """
    area = "ASPECT_AREA"
    """
    The aspect area.
    """
    duration = "ASPECT_DURATION"
    """
    The aspect duration.
    """
    balance = "ASPECT_FINANCIAL_BALANCE"
    """
    The aspect financial balance.
    """
    mass = "ASPECT_MASS"
    """
    The aspect mass.
    """
    monetary_value = "ASPECT_MONETARY_VALUE"
    """
    The aspect monetary value.
    """
    probability = "ASPECT_PROBABILITY"
    """
    The aspect probability.
    """
    volume = "ASPECT_VOLUME"
    """
    The aspect volume.
    """


class MediaTypeInstance(str, Enum):
    """
    Named instances of gist:MediaType from gist reference data.
    """
    JSON = "JSON"
    JSON_LD = "LD_PLUS_JSON"
    N_Quads = "N_QUADS"
    N_Triples = "N_TRIPLES"
    RDFSOLIDUSXML = "RDF_PLUS_XML"
    SPARQL_1FULL_STOP1_Query_Results_JSON = "SPARQL_RESULTS_PLUS_JSON"
    SPARQL_1FULL_STOP1_Query_Results_XML = "SPARQL_RESULTS_PLUS_XML"
    TriG = "TRIG"
    JPG = "JPG"
    PNG = "PNG"
    CSV = "CSV"
    HTML = "HTML"
    Plain_Text = "PLAIN"
    Turtle = "TURTLE"


class PrefixDeclarationInstance(str, Enum):
    """
    Named SHACL prefix declarations from the gist ontology.
    """
    gist = "PREFIXDECLARATION_GIST"
    """
    Prefix 'gist' for namespace <https://w3id.org/semanticarts/ns/ontology/gist/>.
    """
    owl = "PREFIXDECLARATION_OWL"
    """
    Prefix 'owl' for namespace <http://www.w3.org/2002/07/owl#>.
    """
    rdf = "PREFIXDECLARATION_RDF"
    """
    Prefix 'rdf' for namespace <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
    """
    rdfs = "PREFIXDECLARATION_RDFS"
    """
    Prefix 'rdfs' for namespace <http://www.w3.org/2000/01/rdf-schema#>.
    """
    sh = "PREFIXDECLARATION_SH"
    """
    Prefix 'sh' for namespace <http://www.w3.org/ns/shacl#>.
    """
    skos = "PREFIXDECLARATION_SKOS"
    """
    Prefix 'skos' for namespace <http://www.w3.org/2004/02/skos/core#>.
    """
    xsd = "PREFIXDECLARATION_XSD"
    """
    Prefix 'xsd' for namespace <http://www.w3.org/2001/XMLSchema#>.
    """



class GistThing(ConfiguredBaseModel):
    """
    Mixin providing universal slots applicable to any GIST entity. Covers OWL properties with no rdfs:domain (open-world).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixin': True})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Aspect(GistThing):
    """
    A measurable characteristic.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Aspect'],
         'class_uri': 'gist:Aspect',
         'comments': ['Depending on implementation, every aspect should be related to '
                      'a unit group either directly or through a broader aspect. For '
                      'example, angle of incidence could be related to the broader '
                      'concept of angle, which in turn is related to a unit group, or '
                      'it could be related directly to the unit group without the '
                      'hierarchical relationship.',
                      'Rule of thumb: use the least specific aspect that serves the '
                      'intended purpose, increasing specificity only when required '
                      '(e.g., to distinguish between two magnitudes attached to the '
                      'same object).'],
         'disjoint_with': ['Event'],
         'examples': [{'value': 'Length, weight, cost, cycle time, defect rate, '
                                'wheelbase, billing rate.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Category(GistThing):
    """
    A concept or label used to categorize other instances without specifying any formal semantics.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Category'],
         'class_uri': 'gist:Category',
         'comments': ['Often a type can be modeled either as an owl:Class or as a '
                      "gist:Category. Use the latter if you don't care much about the "
                      'formal structure of the different types, or if there is a whole '
                      'hierarchy of types that are going to be managed by a group '
                      'separate from the ontology developers. The formal structure may '
                      'be defined elsewhere and linked to, if necessary.'],
         'disjoint_with': ['Event'],
         'examples': [{'value': 'Tags used in folksonomies; formal definitions from '
                                'other systems.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing'],
         'notes': ['OWL subClassOf restrictions: '
                   '∃isAllocatedBy.(gist:IntellectualProperty | gist:Organization | '
                   'gist:Person)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class AddressUsageType(Category):
    """
    A category indicating the context or manner in which an address may be used.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Address Usage Type'],
         'class_uri': 'gist:AddressUsageType',
         'comments': ['If you are using temporal relations involving addresses, this '
                      'category should be used to qualify the temporal relation rather '
                      'than the address itself, since the same address may have '
                      'different uses in different contexts, by different people and '
                      'organizations, or at different times.'],
         'examples': [{'value': 'Billing, business, personal, postal, residence.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Behavior(Category):
    """
    A category indicating the nature of an activity.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Behavior'],
         'class_uri': 'gist:Behavior',
         'examples': [{'value': 'Drilling and cutting are two different kinds of '
                                'manufacturing event.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Component(GistThing):
    """
    Something that, while having an independent existence, is inherently part of or designed to be part of a larger entity, such as a system or network.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Component'],
         'class_uri': 'gist:Component',
         'comments': ['A component may be designed or intended as part of a whole '
                      'without actually being so; e.g., a car steering wheel that is '
                      'not installed in any car.',
                      'Many things are in a trivial sense a part of a larger thing, '
                      'but are not considered components because they are not '
                      'inherently part of that larger thing. For example, while a book '
                      'may be part of a library (a collection of books), it is not '
                      'inherently so, and thus is not a component. A playing card, on '
                      'the other hand, could be considered a component in (member of) '
                      'a deck of cards. This may be use case-dependent; e.g., car '
                      'parts might be modeled as components in an automobile '
                      'manufacturing context but not in a retail auto parts store.',
                      'Physical substances, such as ingredients in a cake batter, do '
                      'not meet the independent existence criterion, so are not '
                      'components.',
                      'This class is not disjoint with gist:Composite, because a '
                      'component may itself break down into smaller components.',
                      'This is an abstract class that is not directly instantiated. '
                      'Users will define subclasses that are meaningful to their '
                      'domain of interest.'],
         'disjoint_with': ['PhysicalSubstance'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Composite(GistThing):
    """
    Something which is made up of various parts or elements that are independently identifiable.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Composite'],
         'class_uri': 'gist:Composite',
         'comments': ['Some composites, like systems, networks, and ordered '
                      'collections, have internal organization, while others, such as '
                      'unordered collections, typically do not.',
                      'This class is not disjoint with gist:Component, because a '
                      'composite can itself be a component of a larger composite.',
                      'This is an abstract class that will not be directly '
                      'instantiated.'],
         'examples': [{'value': 'A library (collection of books); a network of pipes '
                                'and valves; a computer network of routers and '
                                'computers.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Collection(Composite):
    """
    A grouping of things.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Collection'],
         'class_uri': 'gist:Collection',
         'comments': ['Individuals are placed in the collection using the '
                      'gist:isMemberOf property. Collections typically are created '
                      'because the members are functionally connected in some way. '
                      'This definition allows a collection to have zero members.'],
         'examples': [{'value': 'A jury is a group of people; a financial ledger is a '
                                'collection of transaction entries; a route is an '
                                '(ordered) collection of segments.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Content(GistThing):
    """
    Information available in some medium.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Content'],
         'class_uri': 'gist:Content',
         'comments': ['Categories are not content until they are written down.',
                      'This class includes both abstract content and its expression, '
                      'but it must have at least one expression in order to be '
                      'content. For example, the idea a writer has for a book is not '
                      'content until it is expressed in some form, but a single '
                      'content object may have multiple expressions - e.g., the '
                      'particular print and audio editions.'],
         'disjoint_with': ['GeoPoint',
                           'GeoRegion',
                           'Organization',
                           'PhysicalIdentifiableItem',
                           'PhysicalSubstance',
                           'UnitOfMeasure'],
         'examples': [{'value': "The literary work 'The Adventures of Huckleberry "
                                "Finn' by Mark Twain, independent of any particular "
                                'edition.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Address(Content):
    """
    A reference to a place (real or virtual) that can be located by some routing algorithm and where messages or things can be sent or received.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Address'],
         'class_uri': 'gist:Address',
         'close_mappings': ['common_domain_model:Address'],
         'examples': [{'value': 'A PO Box, a URL to a PDF file.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ContentExpression(Content):
    """
    Content reduced to text, audio, etc.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Content Expression'],
         'class_uri': 'gist:ContentExpression',
         'comments': ['If it contains text (written or spoken), it will be expressed '
                      'in a language.',
                      "While the content expression is less abstract than a 'Work,' it "
                      'is more abstract than the specific physical items that render '
                      'the expression. For example, any physical or electronic book '
                      'with ISBN-13 978-1953649805 is associated with the same content '
                      'expression.'],
         'examples': [{'value': "A specific print or audio edition of 'The Adventures "
                                "of Huckleberry Finn,' such as the one identified by "
                                'ISBN-13 978-1953649805.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL subClassOf restrictions: '
                   '∃isCategorizedBy.gist:GeneralMediaType']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ControlledVocabulary(Collection):
    """
    A collection of terms approved and managed by some organization or person.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Controlled Vocabulary'],
         'class_uri': 'gist:ControlledVocabulary',
         'comments': ['A controlled vocabulary is similar to a skos:ConceptScheme, but '
                      'it could also be used for things that are not concepts, such as '
                      'organizations, US presidents, geographic regions, etc. '
                      'Hierarchical relationships between instances of the controlled '
                      'vocabulary are possible.'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Collection & '
                   '∃isGovernedBy.(gist:Organization | gist:Person) & '
                   '∃^isMemberOf.gist:Category)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class DegreeOfCommitment(Category):
    """
    The difficulty of reversing a commitment.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Degree Of Commitment'],
         'class_uri': 'gist:DegreeOfCommitment',
         'examples': [{'value': 'A car rental typically has a lower degree of '
                                'commitment than an airfare reservation.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Discipline(Category):
    """
    An area of study or practice.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Discipline'],
         'class_uri': 'gist:Discipline',
         'examples': [{'value': 'Finance, accounting, project management, acoustics, '
                                'ballistics.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ElectronicAddress(Address):
    """
    An address referring to a locatable virtual place that does not physically exist but is made by software or electronics to appear to do so.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Electronic Address', 'Virtual Address'],
         'class_uri': 'gist:ElectronicAddress',
         'close_mappings': ['common_domain_model:ContactInformation'],
         'disjoint_with': ['PhysicalAddress'],
         'examples': [{'value': 'A file system path, website URL, IP address, email '
                                'address, mobile or landline telephone number.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ElectronicAddressType(Category):
    """
    A category indicating a kind of electronic address. Such a category is usually based on the technology that enables routing to the address referent.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Electronic Address Type'],
         'class_uri': 'gist:ElectronicAddressType',
         'examples': [{'value': 'A URL, file system path, email address, mobile '
                                'telephone number.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class EquipmentType(Category):
    """
    A category of equipment.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Equipment Type'],
         'class_uri': 'gist:EquipmentType',
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Event(GistThing):
    """
    Something that occurs over a period of time, often characterized as an activity being carried out by some person, organization, or software application or brought about by natural forces.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Event'],
         'class_uri': 'gist:Event',
         'close_mappings': ['common_domain_model:BusinessEvent', 'iso22989:Action'],
         'comments': ['An event does not necessarily have either planned or actual '
                      'start or end datetimes. For example, a conference can be in the '
                      'planning phase without any dates selected, but is nevertheless '
                      'an (unscheduled) event. The subclasses of gist:Event state '
                      'particular restrictions on planned and actual start and end '
                      'dates.',
                      'An event occurs during a time interval, which is distinct from '
                      'the event.'],
         'disjoint_with': ['Language', 'Magnitude', 'TimeInterval', 'UnitOfMeasure'],
         'examples': [{'value': 'A transaction, conference, baseball game, '
                                'earthquake.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing'],
         'narrow_mappings': ['iso22989:AILifecycleProcess', 'iso22989:DataProcess']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ContemporaryEvent(Event):
    """
    An event that has started but has not yet ended.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Contemporary Event'],
         'class_uri': 'gist:ContemporaryEvent',
         'comments': ['When the event actually ends, it will cease being '
                      'contemporary.'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Event & =1actualStartDateTime & '
                   '≤0actualEndDateTime)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ContingentEvent(Event):
    """
    An event with a probability of happening in the future, and usually dependent upon some other event or condition.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Contingent Event'],
         'class_uri': 'gist:ContingentEvent',
         'examples': [{'value': 'A fire insurance payout is contingent on a particular '
                                'building burning down; selling 20 shares of stock in '
                                'a given company is contingent on the price dropping '
                                'below $200/share; the death benefit payout on a life '
                                'insurance policy is contingent on the death of the '
                                'insured person.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Event & '
                   '∃hasMagnitude.∃hasAspect=_Aspect_probability & '
                   '∃isTriggeredBy.gist:Event)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Determination(Event):
    """
    An event whose purpose is to establish a specific result, value, or outcome, usually by research, measuring, evaluating, or calculating.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Determination'],
         'class_uri': 'gist:Determination',
         'close_mappings': ['iso22989:Decision'],
         'examples': [{'value': 'Measuring the sulfur content of crude oil; evaluating '
                                'a loan application for approval; estimating the price '
                                'of gas for the next three months; determining whether '
                                'and by how much an interest rate should change; '
                                'classifying a purchase into a budget category.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class FormattedContent(ContentExpression):
    """
    Content encoded in a specific format, but existing as data independent of any particular physical medium.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Formatted Content'],
         'class_uri': 'gist:FormattedContent',
         'comments': ['Each instance of formatted content is a distinct formatting of '
                      'some Content. Thus, a PDF-formatted version and an '
                      'HTML-formatted version of the same content are separate '
                      'instances of formatted content.'],
         'examples': [{'value': 'A document in PDF format; an image in JPEG format.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:ContentExpression & '
                   '∃isExpressedIn.gist:MediaType)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class GeneralMediaType(Category):
    """
    The real-world media type for content.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['General Media Type'],
         'class_uri': 'gist:GeneralMediaType',
         'examples': [{'value': 'Audio, still image, video, textual, physical (e.g., a '
                                'statue), performance (e.g., a play), oil or pastel '
                                'for a painting.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class GeoLocation(GistThing):
    """
    A physical location, with the earth as a frame of reference.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Geographic Location'],
         'class_uri': 'gist:GeoLocation',
         'close_mappings': ['dpvs:StorageLocation'],
         'comments': ['A geographic location may be a point, region, or volume.'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class GeoPoint(GeoLocation):
    """
    An individual point on or above the Earth's surface, identified by latitude, longitude and altitude. Altitude is the distance measured from sea level. If altitude is missing, the point is assumed to be at the Earth's surface. These points are described using decimal latitude/longitude.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Geographic Point'],
         'class_uri': 'gist:GeoPoint',
         'disjoint_with': ['IntellectualProperty',
                           'Intention',
                           'Language',
                           'Magnitude',
                           'Organization',
                           'PhysicalIdentifiableItem',
                           'PhysicalSubstance',
                           'UnitOfMeasure'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (∃hasMagnitude.∃hasAspect=_Aspect_altitude & '
                   '∃latitude.<http://www.w3.org/2001/XMLSchema#double> & '
                   '∃longitude.<http://www.w3.org/2001/XMLSchema#double>)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class GeoRegion(GeoLocation):
    """
    A bounded region (or set of regions) on the surface of the Earth.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Geographic Region'],
         'broad_mappings': ['dpvs:PersonalSpace'],
         'class_uri': 'gist:GeoRegion',
         'comments': ['A geographic region could be non-contiguous; e.g., the region '
                      'governed by the US federal government is the contiguous area of '
                      'the lower 48 states plus Alaska, Hawaii, and overseas '
                      'territories. Child classes in lower ontologies can make this '
                      'distinction.'],
         'disjoint_with': ['IntellectualProperty',
                           'Intention',
                           'Language',
                           'Magnitude',
                           'Organization',
                           'PhysicalIdentifiableItem',
                           'PhysicalSubstance',
                           'Template',
                           'UnitOfMeasure'],
         'examples': [{'value': 'The bounded shape that defines the region occupied by '
                                'Crater Lake; the bounded area known as the contiguous '
                                'USA.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL subClassOf restrictions: (gist:GeoLocation & '
                   '∃hasMagnitude.∃hasAspect=_Aspect_area)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class GeoVolume(GeoLocation):
    """
    A three-dimensional space on or near the surface of the Earth.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Geographic Volume'],
         'class_uri': 'gist:GeoVolume',
         'examples': [{'value': 'An oil reservoir, the body of a lake, or an '
                                'airspace.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:GeoLocation & '
                   '∃hasMagnitude.∃hasAspect=_Aspect_volume & '
                   '∃^isGeoContainedIn.gist:GeoPoint)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class GovernedGeoRegion(GeoRegion):
    """
    A geographic region governed by at least one government organization.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Governed Geographic Region'],
         'class_uri': 'gist:GovernedGeoRegion',
         'comments': ['Geographic regions do not need not be physically contiguous in '
                      'order to constitute a governed geographic region; e.g., Alaska '
                      'and Hawaii are part of the region governed by the United '
                      'States.'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:GeoRegion & '
                   '∃isGovernedBy.gist:GovernmentOrganization)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class CountryGeoRegion(GovernedGeoRegion):
    """
    A geographic region governed by exactly one country government.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Country Geographic Region'],
         'class_uri': 'gist:CountryGeoRegion',
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL subClassOf restrictions: =1isGovernedBy',
                   'OWL equivalentClass: (gist:GovernedGeoRegion & '
                   '∃isGovernedBy.gist:CountryGovernment)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class HistoricalEvent(Event):
    """
    An event which occurred in time, with an actual end earlier than the present moment.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Historical Event'],
         'class_uri': 'gist:HistoricalEvent',
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL subClassOf restrictions: '
                   '∃actualStartDateTime.<http://www.w3.org/2001/XMLSchema#dateTime>',
                   'OWL equivalentClass: (gist:Event & '
                   '∃actualEndDateTime.<http://www.w3.org/2001/XMLSchema#dateTime>)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ID(Content):
    """
    Content that is used to uniquely identify something or someone.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['ID'],
         'class_uri': 'gist:ID',
         'close_mappings': ['common_domain_model:Identifier',
                            'common_domain_model:PartyIdentifier',
                            'common_domain_model:PersonIdentifier',
                            'common_domain_model:EntityIdentifier',
                            'common_domain_model:AssignedIdentifier'],
         'comments': ['Used in conjunction with gist:isIdentifiedBy.'],
         'examples': [{'value': 'SSN for a person; serial number for a product; '
                                'employee ID for a person.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Content & '
                   '∃isAllocatedBy.(gist:IntellectualProperty | gist:Organization | '
                   'gist:Person) & '
                   '∃uniqueText.<http://www.w3.org/2001/XMLSchema#string>)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class IntellectualProperty(GistThing):
    """
    An intangible work, invention, or concept, independent of its being expressed in text, audio, video, image, or live performance. IP can also be tacit knowledge, know-how, or skill.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Intellectual Property'],
         'broad_mappings': ['dpvs:IntellectualPropertyData'],
         'class_uri': 'gist:IntellectualProperty',
         'comments': ["For literature this could be called the 'Work,' except that "
                      "'work' is a highly overloaded term (expenditure of energy, "
                      'resource consumption, art). Often the first expression precedes '
                      'our recognition of the IP, but subsequent expressions are known '
                      'to be derivatives of the IP, even if they are '
                      'expression-to-expression translations (or copies).',
                      'This concept includes works that are out of copyright or were '
                      'never formally registered; the defining feature is not that it '
                      'is legally protected but that it is an intangible creation of '
                      'the human mind.'],
         'disjoint_with': ['Magnitude',
                           'Organization',
                           'PhysicalIdentifiableItem',
                           'PhysicalSubstance',
                           'UnitOfMeasure'],
         'examples': [{'value': 'The Old Man and The Sea; the Page Rank algorithm; the '
                                'brand Coca Cola.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Intention(GistThing):
    """
    A goal, desire, or aspiration.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Intention'],
         'class_uri': 'gist:Intention',
         'comments': ["The 'teleological' aspect of a system that indicates things are "
                      'done with a purpose.'],
         'disjoint_with': ['Magnitude',
                           'Organization',
                           'PhysicalIdentifiableItem',
                           'PhysicalSubstance',
                           'UnitOfMeasure'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Agreement(Intention):
    """
    A mutually understood arrangement in which two or more parties make commitments to one another.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Agreement'],
         'broad_mappings': ['common_domain_model:MasterAgreement',
                            'dpvs:DataProcessingAgreement'],
         'class_uri': 'gist:Agreement',
         'comments': ['While an agreement has two or more parties, and contains '
                      'commitments which bind those parties, it will not always be '
                      'necessary to instantiate each individual commitment.'],
         'exact_mappings': ['common_domain_model:Agreement'],
         'examples': [{'value': 'A gym membership is an agreement in which the member '
                                'commits to paying the gym a certain price and the gym '
                                'commits to allowing access to their facilities.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Intention & '
                   '∃hasParty.(gist:Organization | gist:Person) & '
                   '≥2^isDirectPartOf.gist:Commitment)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Account(Agreement):
    """
    An agreement having a balance.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Account'],
         'class_uri': 'gist:Account',
         'close_mappings': ['common_domain_model:Account'],
         'examples': [{'value': 'A bank account, a credit card account, an accounts '
                                'receivable account.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Agreement & '
                   '∃hasMagnitude.∃hasAspect=_Aspect_financial_balance)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Commitment(Intention):
    """
    A promise made by a single party to one or more parties to do or not do something or act in a particular way.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Commitment'],
         'class_uri': 'gist:Commitment',
         'comments': ['A commitment is unilateral in that it is binding on only one '
                      'party. This contrasts with gist:Agreement, which consists of '
                      'commitments that bind two or more parties.',
                      'A single commitment may be made to multiple parties at once; it '
                      'is a single commitment rather than multiple commitments if the '
                      'same action would fulfill the obligation to all the parties '
                      'simultaneously. For example, a performer makes a single '
                      'commitment to hold a performance to all ticket purchasers; by '
                      'holding the performance, the commitment to all parties is '
                      'fulfilled in a single action.',
                      'The manner in which a commitment is binding may vary. In a '
                      'business context, we are typically interested in commitments '
                      'that are legally binding.'],
         'examples': [{'value': 'Upon selling a treasury bill, the U.S. government '
                                'makes a commitment to pay the purchaser a stated '
                                'amount of money at a stated time.'},
                      {'value': 'When signing an NDA, the signatory commits to keeping '
                                'specified information confidential.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Intention & (gist:Requirement | '
                   'gist:Restriction) & ∃hasGiver.(gist:Organization | gist:Person) & '
                   '∃isCategorizedBy.gist:DegreeOfCommitment)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ContingentObligation(Commitment):
    """
    An obligation that is not yet firm. There is some contingent event whose occurrence will cause the obligation to become firm.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Contingent Obligation'],
         'class_uri': 'gist:ContingentObligation',
         'close_mappings': ['dpvs:Obligation'],
         'comments': ['A contingent obligation might have a getter counterparty (as in '
                      'the case of insurance); but it might not (as in the case of an '
                      'offer).'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Commitment & '
                   '∃hasGiver.(gist:Organization | gist:Person) & '
                   '∃isTriggeredBy.gist:Event)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Contract(Agreement):
    """
    An agreement which can be enforced by law.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Contract'],
         'class_uri': 'gist:Contract',
         'exact_mappings': ['dpvs:DpvContract'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Agreement & '
                   '∃isUnderJurisdictionOf.gist:GovernmentOrganization)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Function(Intention):
    """
    The activity that a human-made item is intended to perform.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Function'],
         'class_uri': 'gist:Function',
         'examples': [{'value': 'Transmit electricity, provide ballast, control '
                                'ambient temperature.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class KnowledgeConcept(IntellectualProperty):
    """
    An abstract concept that arises from the distillation of experience. It is similar to a category but, rather than being a simple tag, it has rich structure.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Knowledge Concept'],
         'class_uri': 'gist:KnowledgeConcept',
         'comments': ['Some knowledge is about specific instances that already exist '
                      'in the knowledge graph. We may have knowledge that Judge Jones '
                      'is more lenient on repeat offenders in the morning; we may know '
                      'that the earliest killing frost in Fort Collins is the last '
                      'week of September.\r\n'
                      '\r\n'
                      'These fit the broader definition of knowledge, the distillation '
                      'of experience. But they do not require any new instances. Judge '
                      'Jones and Fort Collins already exist and have a place in our '
                      'knowledge graph.\r\n'
                      '\r\n'
                      'But some knowledge requires that we synthesize new instances in '
                      'order to have a place to consolidate the knowledge. A disease '
                      "isn't a tangible thing, like a person or a building. A disease "
                      "is a prediction that a person's health will decline in a "
                      'predictable way (without treatment and with treatment). The '
                      'number of diseases continues to grow as we collectively learn '
                      'more and more granular distinctions. Lung cancer used to be a '
                      'single disease, but now we have dozens of fine-grained '
                      'distinctions; e.g., non-lymphoma small cell fusiform is '
                      'different from alveolar adenocarcinoma because we now know the '
                      'prognosis and treatment are different.\r\n'
                      '\r\n'
                      'This superclass is meant as a place for subclasses that will '
                      'have the instances that represent the foci of the knowledge we '
                      'have acquired. Note the distinction between a particular '
                      'portion of, say, gold, which instantiates '
                      'gist:PhysicalSubstance, and the concept of gold, which '
                      'instantiates gist:KnowledgeConcept.\r\n'
                      '\r\n'
                      'In some ontologies what we are calling knowledge concepts are '
                      'defined as classes; e.g., non-lymphoma small cell fusiform and '
                      'alveolar adenocarcinoma would be two classes rather than two '
                      'instances. But using a class makes it harder to connect the '
                      'concept to other instances in a knowledge graph, and '
                      'furthermore such classes would lack instances.'],
         'examples': [{'value': 'Most domains will define a few subclasses, such as '
                                'gene, protein, chemical, disease, subject matter, '
                                'industry, method.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'related_mappings': ['iso22989:KnowledgeGraph']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Language(GistThing):
    """
    A recognized, organized set of symbols and grammar.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Language'],
         'class_uri': 'gist:Language',
         'deprecated': 'true',
         'disjoint_with': ['Magnitude',
                           'Organization',
                           'PhysicalIdentifiableItem',
                           'PhysicalSubstance',
                           'UnitOfMeasure'],
         'examples': [{'value': 'Natural languages such as English and Spanish; '
                                'computer languages such as OWL, Python, and XML.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Magnitude(GistThing):
    """
    The amount of a measurable characteristic (aspect).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Magnitude'],
         'class_uri': 'gist:Magnitude',
         'close_mappings': ['common_domain_model:Money',
                            'common_domain_model:Cash',
                            'common_domain_model:Quantity',
                            'common_domain_model:Measure'],
         'comments': ['An accuracy can be assigned to a magnitude using the property '
                      'has accuracy.'],
         'disjoint_with': ['Organization',
                           'PhysicalIdentifiableItem',
                           'PhysicalSubstance',
                           'UnitOfMeasure'],
         'examples': [{'value': 'A model of car could have a wheelbase of 113.2 '
                                'inches. In this example, the aspect is wheelbase, the '
                                'unit of measure is inch, and the numeric value is '
                                '113.2.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing'],
         'notes': ['OWL equivalentClass: (∃hasAspect.gist:Aspect & '
                   '∃hasUnitOfMeasure.gist:UnitOfMeasure & '
                   '∃numericValue.<http://www.w3.org/2000/01/rdf-schema#Literal>)'],
         'related_mappings': ['common_domain_model:Price']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class MediaType(Category):
    """
    A digitized type that computer applications can recognize.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Media Type'],
         'class_uri': 'gist:MediaType',
         'comments': ['The unique text for an IANA media type is the concatenation of '
                      "the 'Type name', a slash '/', and the 'Subtype name' as "
                      'provided on the page displayed when you resolve the URI of the '
                      'media type.'],
         'examples': [{'value': 'application/sparql-results+xml'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL subClassOf restrictions: '
                   '∃uniqueText.<http://www.w3.org/2001/XMLSchema#string>']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Medium(Category):
    """
    A physical material on which a work can be rendered, represented, or implemented.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Medium'],
         'class_uri': 'gist:Medium',
         'examples': [{'value': 'Paper, clay, a computer monitor.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Message(ContentExpression):
    """
    A specific instance of content sent from a sender to at least one other recipient.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Message'],
         'class_uri': 'gist:Message',
         'examples': [{'value': 'An email, voice, or web service message; a phone '
                                'call.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:ContentExpression & '
                   '∃comesFromAgent.(gist:Organization | gist:Person) & '
                   '∃goesToAgent.(gist:Organization | gist:Person))']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Network(Composite):
    """
    A composite consisting of nodes connected by links.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Network'],
         'class_uri': 'gist:Network',
         'examples': [{'value': 'A physical network could include connected computers '
                                'or routers, whereas a social network would consist of '
                                'related person or organization members (or their '
                                'proxies, such as accounts).'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Composite & '
                   '∃^isMemberOf.(gist:NetworkLink | gist:NetworkNode))']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class NetworkLink(Component):
    """
    An abstract representation of the connection between two or more nodes in a network.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Network Link'],
         'class_uri': 'gist:NetworkLink',
         'comments': ['Each network link is connected to a network node via the '
                      'property gist:links or one of its subproperties.'],
         'examples': [{'value': 'A network link may be physical, such as pipes, wired '
                                'or wireless networks, but may also be a link in a '
                                'non-physical network, such as organizational '
                                'structures or social networks.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL subClassOf restrictions: ∀links.gist:NetworkNode; =2links',
                   'OWL equivalentClass: (gist:Component & ∃isMemberOf.gist:Network & '
                   '∃links.gist:NetworkNode)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class NetworkNode(Component):
    """
    A node in a network.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Network Node'],
         'class_uri': 'gist:NetworkNode',
         'examples': [{'value': "A person's account is a node in a social network; a "
                                'valve is a node in a network of pipes.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL subClassOf restrictions: ∃isMemberOf.gist:Network']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Offer(ContingentObligation):
    """
    A contingent commitment to buy, sell, swap or provide one or more described or identified goods or services in exchange for another (or others).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Offer'],
         'class_uri': 'gist:Offer',
         'comments': ['Dates on an offer represent the time period the offer is valid '
                      "for, as in '25% off through October 25, 2025.'"],
         'examples': [{'value': 'An offer to sell a book for a given price; an offer '
                                'to purchase real estate for a particular price; an '
                                'offer to swap a sea kayak for a mountain bike; '
                                'currency exchange. A donation may be modeled as an '
                                'offer to receive money typically in exchange for '
                                '$0.00, but sometimes for items of value such as '
                                'coffee mugs or T-shirts.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:ContingentObligation & '
                   '∃hasGiver.(gist:Organization | gist:Person) & '
                   '∃offersToProvide.owl:Thing & ∃offersToReceive.owl:Thing & '
                   '∃plannedEndDateTime.<http://www.w3.org/2001/XMLSchema#dateTime> & '
                   '∃plannedStartDateTime.<http://www.w3.org/2001/XMLSchema#dateTime>)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class OrderedCollection(Collection):
    """
    A collection whose members are ordered in some way.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Ordered Collection'],
         'class_uri': 'gist:OrderedCollection',
         'comments': ['Includes partially ordered collections as well as collections '
                      "in which members occupy the same position in a 'tie.' All "
                      'members of an ordered collection are ordered members.'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Collection & '
                   '(∃^isFirstMemberOf.gist:OrderedMember | =0^isMemberOf) & '
                   '∀^isMemberOf.gist:OrderedMember)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class GeoRoute(OrderedCollection):
    """
    An ordered set of geographic points that defines a path from a starting point to an ending point.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Geographic Route'],
         'class_uri': 'gist:GeoRoute',
         'comments': ['A geographic route could describe a bus route by identifying '
                      'the points where the bus stops. A geographic route could '
                      'describe the boundary of a polygonal geographic region (it does '
                      'not have to be a traveled route).'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:OrderedCollection & '
                   '∃^isMemberOf.gist:GeoPoint)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class OrderedMember(Component):
    """
    A member of an ordered collection serving as a proxy for a real world item, which can appear in different orders in different collections. The ordered member appears in exactly one ordered collection.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Ordered Member'],
         'class_uri': 'gist:OrderedMember',
         'comments': ['An ordered member points to the real world item via the '
                      'providesOrderFor property. Ordering information is represented '
                      'either as a number in a sequence, or by preceding or following '
                      'another ordered member.'],
         'examples': [{'value': 'A person may rank 12th in the Boston Marathon but '
                                '29th in the New York City Marathon.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Component & '
                   '(∃precedesDirectly.gist:OrderedMember | '
                   '∃^precedesDirectly.gist:OrderedMember | '
                   '∃sequence.<http://www.w3.org/2001/XMLSchema#integer>) & '
                   '∃providesOrderFor.owl:Thing & ∀isMemberOf.gist:OrderedCollection & '
                   '=1isMemberOf)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Organization(GistThing):
    """
    A structured entity formed to achieve specific goals, typically involving members with defined roles.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Organization'],
         'broad_mappings': ['dpvs:OrganisationalUnit', 'dpvs:ThirdParty'],
         'class_uri': 'gist:Organization',
         'close_mappings': ['common_domain_model:Party',
                            'common_domain_model:LegalEntity',
                            'common_domain_model:BusinessUnit',
                            'dpvs:LegalEntity'],
         'comments': ['Not all organizations have members, e.g. shell companies.',
                      'While typically the members of organizations are people, in '
                      'some cases they are other organizations; e.g., the members of '
                      'the United Nations are country governments.'],
         'disjoint_with': ['PhysicalIdentifiableItem',
                           'PhysicalSubstance',
                           'SchemaMetaData',
                           'UnitOfMeasure'],
         'exact_mappings': ['iso22989:Organization'],
         'examples': [{'value': 'Legal entities like companies; non-legal entities '
                                'like clubs, committees, or departments.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class GovernmentOrganization(Organization):
    """
    An independent organization exercising political and/or regulatory authority over a political unit, people, geographical region, etc., as well as performing certain functions for this unit or body.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Government Organization'],
         'broad_mappings': ['common_domain_model:LegalEntity'],
         'class_uri': 'gist:GovernmentOrganization',
         'comments': ['Includes administrative, regulatory, and enforcement '
                      'organizations created or sanctioned by country or sub-country '
                      'governments.'],
         'disjoint_with': ['IntergovernmentalOrganization'],
         'examples': [{'value': 'Negative example: A corporation, which is owned and '
                                'therefore not independent.'},
                      {'value': 'The State of Washington Office of Financial '
                                'Management; the Food and Drug Administration; the '
                                'Scottish Parliament.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class CountryGovernment(GovernmentOrganization):
    """
    A government organization which asserts both sovereignty (i.e., it is not governed by some other government organization) and governance over an entity generally recognized as a country.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Country Government'],
         'class_uri': 'gist:CountryGovernment',
         'comments': ['While a country government may enter into treaties with other '
                      'country governments, there are no governing relationships among '
                      'the treaty members.'],
         'disjoint_with': ['SubCountryGovernment'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL subClassOf restrictions: _bnode_; '
                   '≤0isGovernedBy.gist:GovernmentOrganization',
                   'OWL equivalentClass: (gist:GovernmentOrganization & '
                   '∃^isGovernedBy.gist:CountryGeoRegion)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class IntergovernmentalOrganization(Organization):
    """
    An organization whose members are government organizations. This can comprise regional, municipal, state/province, or national level entities.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Intergovernmental Organization'],
         'class_uri': 'gist:IntergovernmentalOrganization',
         'examples': [{'value': 'The United Nations, the European Union, the '
                                'Metropolitan Transit Authority.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Organization & '
                   '≥2^isMemberOf.gist:GovernmentOrganization)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Permission(Intention):
    """
    A description of things one is permitted to do.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Permission'],
         'class_uri': 'gist:Permission',
         'exact_mappings': ['dpvs:Permission'],
         'examples': [{'value': 'Permission could be broad, such as free speech, but '
                                'more often is very specific, such as the right to '
                                'enter a particular property.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Intention & ∃allows.gist:Behavior)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class PhysicalActionType(Category):
    """
    A category indicating the type of an action based on its effect in the physical world.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Physical Action Type'],
         'class_uri': 'gist:PhysicalActionType',
         'examples': [{'value': 'Lifting a garage door, turning off a valve, dropping '
                                'cadmium rods.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class PhysicalAddress(Address):
    """
    An address that refers to a locatable place within the physical universe.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Physical Address'],
         'class_uri': 'gist:PhysicalAddress',
         'examples': [{'value': '1600 Pennsylvania Avenue NW, Washington, DC 20500; PO '
                                'Box 7704, San Francisco, CA 94120-7704; Room 317 in '
                                'the Louvre Museum.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Address & ∃refersTo.gist:GeoLocation)'],
         'related_mappings': ['common_domain_model:Address']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class PhysicalAddressType(Category):
    """
    A category indicating local customary characterizations of physical addresses.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Physical Address Type'],
         'class_uri': 'gist:PhysicalAddressType',
         'examples': [{'value': 'Street address, PO box, FPO code.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class PhysicalEvent(Event):
    """
    An event that can be said to have occurred at some place in space.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Physical Event'],
         'class_uri': 'gist:PhysicalEvent',
         'examples': [{'value': 'A meeting, a car accident.'},
                      {'value': 'Negative examples: Excludes events that have no '
                                'meaningful location, such as financial events or '
                                'project milestones.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Event & ∃occursIn.gist:GeoLocation)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class PhysicalIdentifiableItem(GistThing):
    """
    A discrete physical object which, if subdivided, will result in parts that are distinguishable in nature from the whole and in general also from the other parts.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Physical Identifiable Item'],
         'class_uri': 'gist:PhysicalIdentifiableItem',
         'comments': ['This concept generally corresponds to count nouns in English. '
                      'By contrast, physical substances, such as an amount of water, '
                      'flour, or sand, are mass nouns. Physical identifiable items are '
                      'made up of physical substances; e.g., a cake is made up of '
                      'butter, flour, and sugar; a statue is made of bronze. If you '
                      'divide a physical substance such as an amount of water into '
                      'parts, you have two amounts of water otherwise '
                      'indistinguishable from one another; if you divide a physical '
                      'identifiable item such as a computer into parts, each part is '
                      'different from the whole.'],
         'disjoint_with': ['SchemaMetaData', 'UnitOfMeasure'],
         'examples': [{'value': 'A laptop, a physical book, a car, a building, a '
                                'landmark (such as a tree stump with an etched marking '
                                'to denote a campsite).'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing'],
         'notes': ['OWL subClassOf restrictions: ∃isMadeUpOf.gist:PhysicalSubstance; '
                   '∃hasMagnitude.∃hasAspect=_Aspect_mass; '
                   '∃hasMagnitude.∃hasAspect=_Aspect_volume']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Equipment(PhysicalIdentifiableItem):
    """
    Human-made, tangible property other than land or buildings used to perform a task or activity.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Equipment'],
         'class_uri': 'gist:Equipment',
         'examples': [{'value': 'A machine, a router, a car, a baseball bat.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:PhysicalIdentifiableItem & '
                   '∃isCategorizedBy.gist:EquipmentType)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Landmark(PhysicalIdentifiableItem):
    """
    Something permanently attached to the Earth.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Landmark'],
         'class_uri': 'gist:Landmark',
         'deprecated': 'true',
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL subClassOf restrictions: ∃hasPhysicalLocation.(gist:GeoRegion '
                   '| gist:GeoVolume)',
                   'See guidance on removing the term in the next major release at '
                   'https://github.com/semanticarts/gist/issues/947#issuecomment-1679566885.']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Building(Landmark):
    """
    A relatively permanent man-made structure situated on a plot of land, having a roof and walls, commonly used for dwelling, entertaining, or working.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Building'],
         'class_uri': 'gist:Building',
         'comments': ['User discretion can be applied to edge cases: e.g., is a '
                      "traditional yurt 'relatively permanently situated' although it "
                      'is portable and has a tent-like construction?'],
         'deprecated': 'true',
         'examples': [{'value': 'A house, school, store, factory, chicken coop.'},
                      {'value': 'Negative examples: houseboats (not built on land), '
                                'caves (not man-made), food trucks and RVs (not '
                                'permanently situated).'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class LivingThing(PhysicalIdentifiableItem):
    """
    Something that is currently, or at some point in time was, alive.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Living Thing'],
         'class_uri': 'gist:LivingThing',
         'comments': ['Not all life forms have exactly two parents, so the restriction '
                      'only specifies a minimum of one.'],
         'examples': [{'value': 'A cat, a mushroom, a tree.'},
                      {'value': 'Negative examples: fictional life forms such as '
                                'unicorns or Mickey Mouse.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:PhysicalIdentifiableItem & '
                   '∃hasBiologicalParent.gist:LivingThing & =1birthDate)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Person(LivingThing):
    """
    A human being who was or is alive.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Person'],
         'broad_mappings': ['dpvs:DataSubject'],
         'class_uri': 'gist:Person',
         'close_mappings': ['common_domain_model:NaturalPerson',
                            'iso22989:AIUser',
                            'iso22989:DataSubject'],
         'exact_mappings': ['dpvs:NaturalPerson'],
         'examples': [{'value': 'Negative example: fictional characters.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL subClassOf restrictions: ∀hasBiologicalParent.gist:Person',
                   'OWL equivalentClass: (gist:LivingThing & '
                   '∃hasBiologicalParent.gist:Person)'],
         'related_mappings': ['common_domain_model:Party']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class PhysicalSubstance(GistThing):
    """
    An undifferentiated amount of physical material which, when subdivided, results in each part being indistinguishable in nature from the whole and from every other part.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Physical Substance'],
         'class_uri': 'gist:PhysicalSubstance',
         'comments': ['An instance of this class has weight and takes up space. We '
                      'mean the physical gold in a ring, not the concept of gold that '
                      'shows up in the periodic table. The latter would be an instance '
                      'of gist:KnowledgeConcept.',
                      'This concept generally corresponds to mass nouns in English. By '
                      'contrast, instances of gist:PhysicalIdentifiableItem, such as a '
                      'computer, book, or car, are count nouns. Physical identifiable '
                      'items are made up of physical substances; e.g., a cake is made '
                      'up of butter, flour, and sugar; a ring is made of gold. If you '
                      'divide a physical substance such as an amount of water into '
                      'parts, you have different amounts of water otherwise '
                      'indistinguishable from one another; if you divide a physical '
                      'identifiable item such as a computer into parts, each part will '
                      'be distinguishable from the original whole.'],
         'disjoint_with': ['UnitOfMeasure'],
         'examples': [{'value': 'An amount of water, penicillin, sand, or gold.'},
                      {'value': 'Negative example: the concept of gold.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing'],
         'notes': ['OWL subClassOf restrictions: '
                   '∃hasMagnitude.∃hasAspect=_Aspect_volume; '
                   '∃hasMagnitude.∃hasAspect=_Aspect_mass']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ProductCategory(Category):
    """
    Any of many ways of categorizing products.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Product Category'],
         'class_uri': 'gist:ProductCategory',
         'examples': [{'value': 'Automobile models, NATO product codes.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ReferenceValue(Magnitude):
    """
    A magnitude that was neither measured nor estimated but set by fiat.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Reference Value'],
         'class_uri': 'gist:ReferenceValue',
         'examples': [{'value': 'The sales goal for a company.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class RenderedContent(FormattedContent):
    """
    Content expressed via some physical medium.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Rendered Content'],
         'class_uri': 'gist:RenderedContent',
         'comments': ['Renderings of the same file on two different monitors are '
                      'separate instances of rendered content.'],
         'examples': [{'value': 'Words printed on paper; audio played on speakers; an '
                                'image displayed on a monitor; an original painting.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:FormattedContent & '
                   '∃isRenderedOn.gist:Medium)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Requirement(Intention):
    """
    The obligation of a person or organization to behave in a certain way.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Requirement'],
         'class_uri': 'gist:Requirement',
         'examples': [{'value': 'In the US, drivers must drive on the right side of '
                                'the road.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Restriction(Intention):
    """
    A description of things one is prevented from doing.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Restriction'],
         'class_uri': 'gist:Restriction',
         'examples': [{'value': 'In the US, tax laws restrict the amount of money a '
                                'person can put in retirement accounts over the course '
                                'of a year.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Intention & ∃prevents.gist:Behavior)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ScheduledEvent(Event):
    """
    An event with a planned start datetime.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Scheduled Event'],
         'class_uri': 'gist:ScheduledEvent',
         'comments': ['If the event already started, but has not yet ended, it is a '
                      'contemporary event with an actual start datetime. If the event '
                      'is over, it is a historical event having an actual end '
                      'datetime. The event always retains its planned start datetime, '
                      'and thus continues to be a scheduled event.'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Event & '
                   '∃plannedStartDateTime.<http://www.w3.org/2001/XMLSchema#dateTime>)'],
         'related_mappings': ['common_domain_model:Schedule']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ScheduledTask(ScheduledEvent):
    """
    A task with a planned start datetime.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Scheduled Task'],
         'class_uri': 'gist:ScheduledTask',
         'comments': ['If work on the task has already started, but has not yet ended, '
                      'it will have an actual start datetime. If the task is '
                      'completed, it will also have an actual end datetime. The task '
                      'always retains its planned start time, and thus continues to be '
                      'a scheduled task.'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['Additional named superclasses (modelled as OWL multiple '
                   'inheritance): Task',
                   'OWL equivalentClass: (gist:ScheduledEvent & gist:Task)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class SchemaMetaData(GistThing):
    """
    Superclass for all types of metadata.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Schema Meta Data'],
         'class_uri': 'gist:SchemaMetaData',
         'comments': ['The definition of this class needs additional work.'],
         'deprecated': 'true',
         'disjoint_with': ['UnitOfMeasure'],
         'examples': [{'value': 'Relational concepts, such as tables and columns; tool '
                                'inputs, such as queries and R2RML maps.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Specification(Intention):
    """
    The set of characteristics and constraints on their values that specify what it means to be a particular type of thing, such as a material, product, service or event. A specification is sufficiently precise to allow evaluating conformance to the specification.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Specification'],
         'class_uri': 'gist:Specification',
         'comments': ['Although a characterization of how to do something is often '
                      'called a specification, the intended meaning here is limited to '
                      'specifying what something is. The focus is on the what, not the '
                      'how. Use gist:TaskTemplate for specifying the how, such as a '
                      'plan or process specification. Use gist:conformsTo to assert '
                      'that something conforms to a specification. To represent a '
                      'definition of a particular type of thing that is not '
                      'sufficiently precise to be a gist:Specification, consider using '
                      'gist:KnowledgeConcept.'],
         'examples': [{'value': 'The specification of the iPhone 14; hypothetical '
                                "events covered by a homeowner's insurance policy; a "
                                'drug quality specification - a set of acceptance '
                                'criteria for quality characteristics that must be '
                                'controlled to ensure a drug is fit for its intended '
                                'use.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'related_mappings': ['common_domain_model:EligibleCollateralCriteria']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class CatalogItem(Specification):
    """
    A description of a product or service to be delivered, given in a sufficient level of detail that a receiver could determine whether delivery constituted discharge of the obligation to deliver.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Catalog Item'],
         'class_uri': 'gist:CatalogItem',
         'comments': ['In short, an unambiguous characterization of what it is that a '
                      'potential buyer is paying for.'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class BundledCatalogItem(CatalogItem):
    """
    Any combination of descriptions of things offered together.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Bundled Catalog Item'],
         'class_uri': 'gist:BundledCatalogItem',
         'examples': [{'value': 'A kit containing several parts offered together; a '
                                'product plus a warranty.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:CatalogItem & '
                   '∃^isDirectPartOf.gist:CatalogItem)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ContractTerm(Specification):
    """
    A specification of some aspect of a contract.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Contract Term'],
         'class_uri': 'gist:ContractTerm',
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'related_mappings': ['common_domain_model:CollateralProvisions']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class EventSpecification(Specification):
    """
    A characterization of an event that might happen.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Event Specification'],
         'class_uri': 'gist:EventSpecification',
         'comments': ['This concept is useful for risk assessment and insurance '
                      'policies.'],
         'examples': [{'value': 'An insurance company defines the characteristics of a '
                                'weather event that must be satisfied for it to '
                                "qualify as a hail storm covered in its homeowner's "
                                'policy; a bank defines the point at which a borrower '
                                'defaults on a loan.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ProductSpecification(CatalogItem):
    """
    A description of something that could be physically warehoused or digitally stored and physically or digitally delivered.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Product Specification'],
         'class_uri': 'gist:ProductSpecification',
         'close_mappings': ['common_domain_model:TradableProduct'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:CatalogItem & '
                   '∃isCategorizedBy.gist:ProductCategory)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class ServiceSpecification(CatalogItem):
    """
    A description of something that can be done for a person or organization (which produces some form of an act).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Service Specification'],
         'class_uri': 'gist:ServiceSpecification',
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:CatalogItem & ∃^isBasedOn.gist:Event)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class SubCountryGovernment(GovernmentOrganization):
    """
    The government of a governed geographic region other than a country which is under the direct or indirect control of a country government.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Sub-Country Government'],
         'class_uri': 'gist:SubCountryGovernment',
         'comments': ['Note that the predicate gist:isGovernedBy is used both for the '
                      'relationship a governed geographic region has to its government '
                      'and for the relationship a sub-region government has to the '
                      'government of the larger region.',
                      'There are many types of sub-regions of a country and the '
                      'governments thereof (as well as different terms, like '
                      "'province' and 'state,' which refer to essentially the same "
                      "type of thing). We should not automatically assume 'state,' "
                      "'county,' and 'city.' Subclasses or categories can be defined "
                      'if greater specificity is needed.',
                      'This class applies only to organizations governing geographic '
                      'regions. Regulatory and bureaucratic organizations are members '
                      'of the more generic gist:GovernmentOrganization class.'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:GovernmentOrganization & '
                   '∃isGovernedBy.gist:CountryGovernment & '
                   '∃^isGovernedBy.gist:GeoRegion)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class System(Composite):
    """
    A composite made up of interacting or interdependent components that together operate as a whole.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['System'],
         'class_uri': 'gist:System',
         'comments': ['May be used to refer to either man-made or natural systems.'],
         'examples': [{'value': 'A manufacturing system, a storm system.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Composite & '
                   '∃^isDirectPartOf.gist:Component)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Tag(Category):
    """
    A term in a folksonomy used to categorize things. Tags can be made up on the fly by users.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Tag'],
         'class_uri': 'gist:Tag',
         'comments': ['Whether to use gist:containedText or gist:uniqueText on tags is '
                      'an implementation decision. Since the latter is a subproperty '
                      'of the former, the restriction remains valid either way.'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL subClassOf restrictions: '
                   '∃containedText.<http://www.w3.org/2001/XMLSchema#string>']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Task(Event):
    """
    An activity or piece of work that is either proposed, planned, scheduled, underway, or completed.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Task'],
         'class_uri': 'gist:Task',
         'close_mappings': ['iso22989:Task'],
         'comments': ['Something that could potentially be executed, which is merely '
                      'described but not proposed in any specific way, such as a '
                      'business process for onboarding a new employee, or the steps in '
                      'a recipe for making polyethylene from ethylene, is not a task '
                      'but rather a task template.',
                      "This term is broader than the English word 'task,' which "
                      'implies assignment, responsibility, or duty. In ordinary '
                      'English going to a concert has a goal but is (generally) done '
                      'for pleasure rather than out of obligation, and would not be '
                      'considered a task, while according to the gist definition it is '
                      'a task. The expansion of meaning is deliberate, so that '
                      'anything that has a goal and can be specified by a task '
                      'template is a task.',
                      'Use the property gist:isBasedOn to link a task back to the task '
                      'template.'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Event & ∃hasGoal.gist:Intention)'],
         'related_mappings': ['common_domain_model:Workflow']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Project(Task):
    """
    A task, usually of longer duration, made up of other tasks.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Project'],
         'class_uri': 'gist:Project',
         'examples': [{'value': 'Designing an insurance product; adding a new feature '
                                'to a software application; assessing the level of '
                                'risk for a mortgage application.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Task & ∃^isPartOf.gist:Task)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Template(GistThing):
    """
    Something used to make objects in its own image.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Template'],
         'class_uri': 'gist:Template',
         'comments': ['Use gist:isBasedOn to link the object made from the template '
                      'back to the template.'],
         'disjoint_with': ['UnitOfMeasure'],
         'examples': [{'value': 'A die in manufacturing is used to make stamped parts; '
                                'a form provides a structure and fields to be filled '
                                'in; a cookie cutter is a template for cookies.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class TaskTemplate(Template):
    """
    An outline of a task of a particular type, which is the basis for executing such tasks.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Task Template'],
         'class_uri': 'gist:TaskTemplate',
         'comments': ['A task template may define a single activity or a series of '
                      'activities; the level of granularity can be varied according to '
                      'use case. For example, in a new employee onboarding process, '
                      'signing up for benefits might be one activity, or it might be '
                      'broken down into signing up for health insurance, signing up '
                      'for dental insurance, etc.',
                      'Use the property isBasedOn to link the Task back to the '
                      'TaskTemplate.'],
         'examples': [{'value': 'A business process for onboarding new employees.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:Template & ∃hasGoal.gist:Intention)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class TemporalRelation(GistThing):
    """
    A relationship existing for a period of time.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Temporal Relation'],
         'class_uri': 'gist:TemporalRelation',
         'comments': ['A temporal relation must have a minimum of two participants. '
                      'For example, both the employer and the employee are '
                      'participants in a temporal relation representing a period of '
                      "employment. Note that 'participant' does not imply agency; a "
                      'non-sentient being can participate in a temporal relation. For '
                      'example, both a person and a house could be participants in a '
                      "hypothetical relation 'lives at.'"],
         'examples': [{'value': 'The relationship between a person and their employer; '
                                'the relationship between a person or business and an '
                                'address.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing'],
         'notes': ['OWL subClassOf restrictions: =1startDateTime; ≥2hasParticipant']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Assignment(TemporalRelation):
    """
    A temporal relationship between an assignee, the thing assigned, and the resource that made the assignment.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Assignment'],
         'class_uri': 'gist:Assignment',
         'close_mappings': ['common_domain_model:RelatedParty',
                            'common_domain_model:Counterparty',
                            'common_domain_model:NaturalPersonRole'],
         'comments': ['Based on the Open World Assumption, the assigner may not be '
                      'asserted or known.',
                      'For some assignments, such as the assignment of a person to a '
                      'task, it may seem equally correct in ordinary speech to say it '
                      'is an assignment of a task to a person. Since '
                      'gist:isAssignmentTo and gist:isAssignmentOf have no formal '
                      'domains or ranges, the choice of which predicate to use for '
                      'which is left as an implementation decision. Consistency is a '
                      'key consideration.'],
         'examples': [{'value': 'An employee is assigned to a task by a supervisor. A '
                                'person is assigned to a position.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:TemporalRelation & ∃hasGiver.owl:Thing '
                   '& ∃isAssignmentOf.owl:Thing & ∃isAssignmentTo.owl:Thing)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Text(ContentExpression):
    """
    Content expressed as a written sequence of characters.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Text'],
         'class_uri': 'gist:Text',
         'comments': ['Text is expressed in a language (human or computer) and may but '
                      'need not specify an encoding.'],
         'examples': [{'value': 'Negative example: photographs or scans of text are '
                                'not text. These instead depict a subject, which '
                                'happens to be text.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL equivalentClass: (gist:ContentExpression & '
                   '∃isExpressedIn.gist:Language & '
                   '∃containedText.<http://www.w3.org/2001/XMLSchema#string>)']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class TimeInterval(GistThing):
    """
    A span of time with a known start time, end time, and duration. As long as two of the three are known, the third can be inferred.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Time Interval'],
         'class_uri': 'gist:TimeInterval',
         'close_mappings': ['common_domain_model:Period'],
         'comments': ['An ongoing state of affairs with an unknown end time in the '
                      'future cannot be a time interval; e.g. the lifespan of a living '
                      'person cannot be a time interval, as the end time is unknown.',
                      'This is distinct from a duration, which describes how long a '
                      'time interval lasts (e.g., one hour; 3 days; 22 minutes).'],
         'examples': [{'value': '7pm to 9pm on Jan 1, 2001; fiscal year 2023 '
                                '(according to some particular definition of fiscal '
                                'year); the week starting at midnight of January 12, '
                                '2023 and lasting exactly 168 hours.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing'],
         'notes': ['OWL subClassOf restrictions: =1startDateTime; _bnode_; '
                   '=1endDateTime']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class Transaction(Event):
    """
    An exchange or transfer of goods, services, or funds.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Transaction'],
         'class_uri': 'gist:Transaction',
         'close_mappings': ['common_domain_model:Trade'],
         'comments': ['Different sorts of transactions can have different datetime '
                      'precisions. For example, an electronic transaction would have a '
                      'gist:actualEndMicrosecond.'],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'related_mappings': ['common_domain_model:TradeState']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class UnitGroup(Collection):
    """
    A collection of units of measure that can all be used to measure the same aspects.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Unit Group'],
         'class_uri': 'gist:UnitGroup',
         'comments': ['Typically there is one unit group per aspect. An example of an '
                      'aspect with two unit groups is vehicle efficiency, which can be '
                      'measured by miles per gallon (distance per volume) or by liters '
                      'per 100 kilometers (volume per distance). These two units of '
                      'measure need to be in different unit groups because they have '
                      'different values of exponents. When adding a unit of measure to '
                      'a unit group, make sure it has the same exponents as the other '
                      'members of the unit group.'],
         'disjoint_with': ['UnitOfMeasure'],
         'examples': [{'value': 'The units of measure bit, byte, kilobit, kilobyte, '
                                'etc. are all in the same unit group because they can '
                                'all be used to measure an amount of data.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'notes': ['OWL subClassOf restrictions: ∃^isMemberOf.gist:UnitOfMeasure']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


class UnitOfMeasure(GistThing):
    """
    A standard amount used to measure or specify things.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['Unit of Measure'],
         'class_uri': 'gist:UnitOfMeasure',
         'close_mappings': ['common_domain_model:UnitType'],
         'examples': [{'value': 'An acre is a unit for measuring area.'}],
         'from_schema': 'https://w3id.org/lmodel/gist/core',
         'in_subset': ['gist_core'],
         'mixins': ['GistThing']})

    name: Optional[str] = Field(default=None, description="""Relates an individual to (one of) its name(s).""", json_schema_extra = { "linkml_meta": {'aliases': ['name'],
         'domain_of': ['GistThing'],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:name'} })
    description: Optional[str] = Field(default=None, description="""A statement about someone or something's attributes or characteristics.""", json_schema_extra = { "linkml_meta": {'aliases': ['description'],
         'comments': ['This property is used to describe instance data which is not '
                      'part of the ontology. A definition and a description have '
                      'different semantics. Use skos:definition for a statement of the '
                      "meaning of a thing and gist:description to describe a thing's "
                      'attributes, characteristics, or features.'],
         'domain_of': ['GistThing'],
         'examples': [{'value': "'The Empire State Building is a 102-story Art Deco "
                                'skyscraper in midtown Manhattan in New York City. It '
                                'was designed by Shreve, Lamb & Harmon and built from '
                                "1930 to 1931.'"},
                      {'value': 'A person does not have a definition, but might be '
                                'described as being six feet tall with brown hair and '
                                'blue eyes; an ontology class or taxonomy term has a '
                                'definition.'}],
         'in_subset': ['gist_core'],
         'slot_uri': 'gist:description'} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
GistThing.model_rebuild()
Aspect.model_rebuild()
Category.model_rebuild()
AddressUsageType.model_rebuild()
Behavior.model_rebuild()
Component.model_rebuild()
Composite.model_rebuild()
Collection.model_rebuild()
Content.model_rebuild()
Address.model_rebuild()
ContentExpression.model_rebuild()
ControlledVocabulary.model_rebuild()
DegreeOfCommitment.model_rebuild()
Discipline.model_rebuild()
ElectronicAddress.model_rebuild()
ElectronicAddressType.model_rebuild()
EquipmentType.model_rebuild()
Event.model_rebuild()
ContemporaryEvent.model_rebuild()
ContingentEvent.model_rebuild()
Determination.model_rebuild()
FormattedContent.model_rebuild()
GeneralMediaType.model_rebuild()
GeoLocation.model_rebuild()
GeoPoint.model_rebuild()
GeoRegion.model_rebuild()
GeoVolume.model_rebuild()
GovernedGeoRegion.model_rebuild()
CountryGeoRegion.model_rebuild()
HistoricalEvent.model_rebuild()
ID.model_rebuild()
IntellectualProperty.model_rebuild()
Intention.model_rebuild()
Agreement.model_rebuild()
Account.model_rebuild()
Commitment.model_rebuild()
ContingentObligation.model_rebuild()
Contract.model_rebuild()
Function.model_rebuild()
KnowledgeConcept.model_rebuild()
Language.model_rebuild()
Magnitude.model_rebuild()
MediaType.model_rebuild()
Medium.model_rebuild()
Message.model_rebuild()
Network.model_rebuild()
NetworkLink.model_rebuild()
NetworkNode.model_rebuild()
Offer.model_rebuild()
OrderedCollection.model_rebuild()
GeoRoute.model_rebuild()
OrderedMember.model_rebuild()
Organization.model_rebuild()
GovernmentOrganization.model_rebuild()
CountryGovernment.model_rebuild()
IntergovernmentalOrganization.model_rebuild()
Permission.model_rebuild()
PhysicalActionType.model_rebuild()
PhysicalAddress.model_rebuild()
PhysicalAddressType.model_rebuild()
PhysicalEvent.model_rebuild()
PhysicalIdentifiableItem.model_rebuild()
Equipment.model_rebuild()
Landmark.model_rebuild()
Building.model_rebuild()
LivingThing.model_rebuild()
Person.model_rebuild()
PhysicalSubstance.model_rebuild()
ProductCategory.model_rebuild()
ReferenceValue.model_rebuild()
RenderedContent.model_rebuild()
Requirement.model_rebuild()
Restriction.model_rebuild()
ScheduledEvent.model_rebuild()
ScheduledTask.model_rebuild()
SchemaMetaData.model_rebuild()
Specification.model_rebuild()
CatalogItem.model_rebuild()
BundledCatalogItem.model_rebuild()
ContractTerm.model_rebuild()
EventSpecification.model_rebuild()
ProductSpecification.model_rebuild()
ServiceSpecification.model_rebuild()
SubCountryGovernment.model_rebuild()
System.model_rebuild()
Tag.model_rebuild()
Task.model_rebuild()
Project.model_rebuild()
Template.model_rebuild()
TaskTemplate.model_rebuild()
TemporalRelation.model_rebuild()
Assignment.model_rebuild()
Text.model_rebuild()
TimeInterval.model_rebuild()
Transaction.model_rebuild()
UnitGroup.model_rebuild()
UnitOfMeasure.model_rebuild()
