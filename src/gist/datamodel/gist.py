# Auto generated from gist.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-09-30T01:46:34
# Schema: gist
#
# id: https://w3id.org/lmodel/gist
# description: gist  is a minimalist upper ontology created by Semantic Arts for enterprise knowledge graph applications. This LinkML schema (version 14.1.0) aggregates the gist modules: Core (classes and properties), MediaTypes (IANA media type instances), and PrefixDeclarations (SHACL namespace bindings). Supplementary schemas gist_rdfs_annotations and gist_sub_class_assertions are available for annotation enrichment and OWL RL reasoner support.
# license: CC-BY-4.0

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Datetime, Decimal, Float, Integer, String
from linkml_runtime.utils.metamodelcore import Decimal, XSDDateTime

metamodel_version = "1.11.0"
version = "14.1.0"

# Namespaces
COMMON_DOMAIN_MODEL = CurieNamespace('common_domain_model', 'https://w3id.org/lmodel/common-domain-model/')
DPV = CurieNamespace('dpv', 'https://w3id.org/lmodel/dpv/')
GIST = CurieNamespace('gist', 'https://w3id.org/semanticarts/ns/ontology/gist/')
GIST_LINKML = CurieNamespace('gist_linkml', 'https://w3id.org/lmodel/gist/')
GISTD = CurieNamespace('gistd', 'https://w3id.org/semanticarts/ns/data/gist/')
ISO22989 = CurieNamespace('iso22989', 'https://w3id.org/lmodel/iso22989/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
MEDIA_APP = CurieNamespace('media_app', 'https://www.iana.org/assignments/media-types/application/')
MEDIA_IMG = CurieNamespace('media_img', 'https://www.iana.org/assignments/media-types/image/')
MEDIA_TXT = CurieNamespace('media_txt', 'https://www.iana.org/assignments/media-types/text/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
DEFAULT_ = GIST_LINKML


# Types

# Class references



@dataclass(repr=False)
class Aspect(YAMLRoot):
    """
    A measurable characteristic.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Aspect"]
    class_class_curie: ClassVar[str] = "gist:Aspect"
    class_name: ClassVar[str] = "Aspect"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Aspect

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Category(YAMLRoot):
    """
    A concept or label used to categorize other instances without specifying any formal semantics.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Category"]
    class_class_curie: ClassVar[str] = "gist:Category"
    class_name: ClassVar[str] = "Category"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Category

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


class AddressUsageType(Category):
    """
    A category indicating the context or manner in which an address may be used.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["AddressUsageType"]
    class_class_curie: ClassVar[str] = "gist:AddressUsageType"
    class_name: ClassVar[str] = "AddressUsageType"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.AddressUsageType


class Behavior(Category):
    """
    A category indicating the nature of an activity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Behavior"]
    class_class_curie: ClassVar[str] = "gist:Behavior"
    class_name: ClassVar[str] = "Behavior"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Behavior


@dataclass(repr=False)
class Component(YAMLRoot):
    """
    Something that, while having an independent existence, is inherently part of or designed to be part of a larger
    entity, such as a system or network.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Component"]
    class_class_curie: ClassVar[str] = "gist:Component"
    class_name: ClassVar[str] = "Component"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Component

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Composite(YAMLRoot):
    """
    Something which is made up of various parts or elements that are independently identifiable.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Composite"]
    class_class_curie: ClassVar[str] = "gist:Composite"
    class_name: ClassVar[str] = "Composite"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Composite

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


class Collection(Composite):
    """
    A grouping of things.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Collection"]
    class_class_curie: ClassVar[str] = "gist:Collection"
    class_name: ClassVar[str] = "Collection"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Collection


@dataclass(repr=False)
class Content(YAMLRoot):
    """
    Information available in some medium.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Content"]
    class_class_curie: ClassVar[str] = "gist:Content"
    class_name: ClassVar[str] = "Content"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Content

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


class Address(Content):
    """
    A reference to a place (real or virtual) that can be located by some routing algorithm and where messages or
    things can be sent or received.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Address"]
    class_class_curie: ClassVar[str] = "gist:Address"
    class_name: ClassVar[str] = "Address"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Address


class ContentExpression(Content):
    """
    Content reduced to text, audio, etc.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ContentExpression"]
    class_class_curie: ClassVar[str] = "gist:ContentExpression"
    class_name: ClassVar[str] = "ContentExpression"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ContentExpression


class ControlledVocabulary(Collection):
    """
    A collection of terms approved and managed by some organization or person.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ControlledVocabulary"]
    class_class_curie: ClassVar[str] = "gist:ControlledVocabulary"
    class_name: ClassVar[str] = "ControlledVocabulary"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ControlledVocabulary


class DegreeOfCommitment(Category):
    """
    The difficulty of reversing a commitment.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["DegreeOfCommitment"]
    class_class_curie: ClassVar[str] = "gist:DegreeOfCommitment"
    class_name: ClassVar[str] = "DegreeOfCommitment"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.DegreeOfCommitment


class Discipline(Category):
    """
    An area of study or practice.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Discipline"]
    class_class_curie: ClassVar[str] = "gist:Discipline"
    class_name: ClassVar[str] = "Discipline"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Discipline


class ElectronicAddress(Address):
    """
    An address referring to a locatable virtual place that does not physically exist but is made by software or
    electronics to appear to do so.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ElectronicAddress"]
    class_class_curie: ClassVar[str] = "gist:ElectronicAddress"
    class_name: ClassVar[str] = "ElectronicAddress"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ElectronicAddress


class ElectronicAddressType(Category):
    """
    A category indicating a kind of electronic address. Such a category is usually based on the technology that
    enables routing to the address referent.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ElectronicAddressType"]
    class_class_curie: ClassVar[str] = "gist:ElectronicAddressType"
    class_name: ClassVar[str] = "ElectronicAddressType"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ElectronicAddressType


class EquipmentType(Category):
    """
    A category of equipment.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["EquipmentType"]
    class_class_curie: ClassVar[str] = "gist:EquipmentType"
    class_name: ClassVar[str] = "EquipmentType"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.EquipmentType


@dataclass(repr=False)
class Event(YAMLRoot):
    """
    Something that occurs over a period of time, often characterized as an activity being carried out by some person,
    organization, or software application or brought about by natural forces.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Event"]
    class_class_curie: ClassVar[str] = "gist:Event"
    class_name: ClassVar[str] = "Event"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Event

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


class ContemporaryEvent(Event):
    """
    An event that has started but has not yet ended.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ContemporaryEvent"]
    class_class_curie: ClassVar[str] = "gist:ContemporaryEvent"
    class_name: ClassVar[str] = "ContemporaryEvent"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ContemporaryEvent


class ContingentEvent(Event):
    """
    An event with a probability of happening in the future, and usually dependent upon some other event or condition.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ContingentEvent"]
    class_class_curie: ClassVar[str] = "gist:ContingentEvent"
    class_name: ClassVar[str] = "ContingentEvent"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ContingentEvent


class Determination(Event):
    """
    An event whose purpose is to establish a specific result, value, or outcome, usually by research, measuring,
    evaluating, or calculating.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Determination"]
    class_class_curie: ClassVar[str] = "gist:Determination"
    class_name: ClassVar[str] = "Determination"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Determination


class FormattedContent(ContentExpression):
    """
    Content encoded in a specific format, but existing as data independent of any particular physical medium.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["FormattedContent"]
    class_class_curie: ClassVar[str] = "gist:FormattedContent"
    class_name: ClassVar[str] = "FormattedContent"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.FormattedContent


class GeneralMediaType(Category):
    """
    The real-world media type for content.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["GeneralMediaType"]
    class_class_curie: ClassVar[str] = "gist:GeneralMediaType"
    class_name: ClassVar[str] = "GeneralMediaType"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.GeneralMediaType


@dataclass(repr=False)
class GeoLocation(YAMLRoot):
    """
    A physical location, with the earth as a frame of reference.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["GeoLocation"]
    class_class_curie: ClassVar[str] = "gist:GeoLocation"
    class_name: ClassVar[str] = "GeoLocation"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.GeoLocation

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


class GeoPoint(GeoLocation):
    """
    An individual point on or above the Earth's surface, identified by latitude, longitude and altitude. Altitude is
    the distance measured from sea level. If altitude is missing, the point is assumed to be at the Earth's surface.
    These points are described using decimal latitude/longitude.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["GeoPoint"]
    class_class_curie: ClassVar[str] = "gist:GeoPoint"
    class_name: ClassVar[str] = "GeoPoint"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.GeoPoint


class GeoRegion(GeoLocation):
    """
    A bounded region (or set of regions) on the surface of the Earth.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["GeoRegion"]
    class_class_curie: ClassVar[str] = "gist:GeoRegion"
    class_name: ClassVar[str] = "GeoRegion"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.GeoRegion


class GeoVolume(GeoLocation):
    """
    A three-dimensional space on or near the surface of the Earth.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["GeoVolume"]
    class_class_curie: ClassVar[str] = "gist:GeoVolume"
    class_name: ClassVar[str] = "GeoVolume"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.GeoVolume


class GovernedGeoRegion(GeoRegion):
    """
    A geographic region governed by at least one government organization.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["GovernedGeoRegion"]
    class_class_curie: ClassVar[str] = "gist:GovernedGeoRegion"
    class_name: ClassVar[str] = "GovernedGeoRegion"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.GovernedGeoRegion


class CountryGeoRegion(GovernedGeoRegion):
    """
    A geographic region governed by exactly one country government.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["CountryGeoRegion"]
    class_class_curie: ClassVar[str] = "gist:CountryGeoRegion"
    class_name: ClassVar[str] = "CountryGeoRegion"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.CountryGeoRegion


class HistoricalEvent(Event):
    """
    An event which occurred in time, with an actual end earlier than the present moment.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["HistoricalEvent"]
    class_class_curie: ClassVar[str] = "gist:HistoricalEvent"
    class_name: ClassVar[str] = "HistoricalEvent"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.HistoricalEvent


class ID(Content):
    """
    Content that is used to uniquely identify something or someone.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ID"]
    class_class_curie: ClassVar[str] = "gist:ID"
    class_name: ClassVar[str] = "ID"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ID


@dataclass(repr=False)
class IntellectualProperty(YAMLRoot):
    """
    An intangible work, invention, or concept, independent of its being expressed in text, audio, video, image, or
    live performance. IP can also be tacit knowledge, know-how, or skill.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["IntellectualProperty"]
    class_class_curie: ClassVar[str] = "gist:IntellectualProperty"
    class_name: ClassVar[str] = "IntellectualProperty"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.IntellectualProperty

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Intention(YAMLRoot):
    """
    A goal, desire, or aspiration.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Intention"]
    class_class_curie: ClassVar[str] = "gist:Intention"
    class_name: ClassVar[str] = "Intention"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Intention

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


class Agreement(Intention):
    """
    A mutually understood arrangement in which two or more parties make commitments to one another.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Agreement"]
    class_class_curie: ClassVar[str] = "gist:Agreement"
    class_name: ClassVar[str] = "Agreement"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Agreement


class Account(Agreement):
    """
    An agreement having a balance.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Account"]
    class_class_curie: ClassVar[str] = "gist:Account"
    class_name: ClassVar[str] = "Account"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Account


class Commitment(Intention):
    """
    A promise made by a single party to one or more parties to do or not do something or act in a particular way.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Commitment"]
    class_class_curie: ClassVar[str] = "gist:Commitment"
    class_name: ClassVar[str] = "Commitment"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Commitment


class ContingentObligation(Commitment):
    """
    An obligation that is not yet firm. There is some contingent event whose occurrence will cause the obligation to
    become firm.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ContingentObligation"]
    class_class_curie: ClassVar[str] = "gist:ContingentObligation"
    class_name: ClassVar[str] = "ContingentObligation"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ContingentObligation


class Contract(Agreement):
    """
    An agreement which can be enforced by law.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Contract"]
    class_class_curie: ClassVar[str] = "gist:Contract"
    class_name: ClassVar[str] = "Contract"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Contract


class Function(Intention):
    """
    The activity that a human-made item is intended to perform.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Function"]
    class_class_curie: ClassVar[str] = "gist:Function"
    class_name: ClassVar[str] = "Function"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Function


class KnowledgeConcept(IntellectualProperty):
    """
    An abstract concept that arises from the distillation of experience. It is similar to a category but, rather than
    being a simple tag, it has rich structure.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["KnowledgeConcept"]
    class_class_curie: ClassVar[str] = "gist:KnowledgeConcept"
    class_name: ClassVar[str] = "KnowledgeConcept"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.KnowledgeConcept


@dataclass(repr=False)
class Language(YAMLRoot):
    """
    A recognized, organized set of symbols and grammar.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Language"]
    class_class_curie: ClassVar[str] = "gist:Language"
    class_name: ClassVar[str] = "Language"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Language

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Magnitude(YAMLRoot):
    """
    The amount of a measurable characteristic (aspect).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Magnitude"]
    class_class_curie: ClassVar[str] = "gist:Magnitude"
    class_name: ClassVar[str] = "Magnitude"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Magnitude

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


class MediaType(Category):
    """
    A digitized type that computer applications can recognize.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["MediaType"]
    class_class_curie: ClassVar[str] = "gist:MediaType"
    class_name: ClassVar[str] = "MediaType"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.MediaType


class Medium(Category):
    """
    A physical material on which a work can be rendered, represented, or implemented.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Medium"]
    class_class_curie: ClassVar[str] = "gist:Medium"
    class_name: ClassVar[str] = "Medium"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Medium


class Message(ContentExpression):
    """
    A specific instance of content sent from a sender to at least one other recipient.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Message"]
    class_class_curie: ClassVar[str] = "gist:Message"
    class_name: ClassVar[str] = "Message"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Message


class Network(Composite):
    """
    A composite consisting of nodes connected by links.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Network"]
    class_class_curie: ClassVar[str] = "gist:Network"
    class_name: ClassVar[str] = "Network"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Network


class NetworkLink(Component):
    """
    An abstract representation of the connection between two or more nodes in a network.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["NetworkLink"]
    class_class_curie: ClassVar[str] = "gist:NetworkLink"
    class_name: ClassVar[str] = "NetworkLink"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.NetworkLink


class NetworkNode(Component):
    """
    A node in a network.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["NetworkNode"]
    class_class_curie: ClassVar[str] = "gist:NetworkNode"
    class_name: ClassVar[str] = "NetworkNode"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.NetworkNode


class Offer(ContingentObligation):
    """
    A contingent commitment to buy, sell, swap or provide one or more described or identified goods or services in
    exchange for another (or others).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Offer"]
    class_class_curie: ClassVar[str] = "gist:Offer"
    class_name: ClassVar[str] = "Offer"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Offer


class OrderedCollection(Collection):
    """
    A collection whose members are ordered in some way.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["OrderedCollection"]
    class_class_curie: ClassVar[str] = "gist:OrderedCollection"
    class_name: ClassVar[str] = "OrderedCollection"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.OrderedCollection


class GeoRoute(OrderedCollection):
    """
    An ordered set of geographic points that defines a path from a starting point to an ending point.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["GeoRoute"]
    class_class_curie: ClassVar[str] = "gist:GeoRoute"
    class_name: ClassVar[str] = "GeoRoute"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.GeoRoute


class OrderedMember(Component):
    """
    A member of an ordered collection serving as a proxy for a real world item, which can appear in different orders
    in different collections. The ordered member appears in exactly one ordered collection.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["OrderedMember"]
    class_class_curie: ClassVar[str] = "gist:OrderedMember"
    class_name: ClassVar[str] = "OrderedMember"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.OrderedMember


@dataclass(repr=False)
class Organization(YAMLRoot):
    """
    A structured entity formed to achieve specific goals, typically involving members with defined roles.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Organization"]
    class_class_curie: ClassVar[str] = "gist:Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Organization

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


class GovernmentOrganization(Organization):
    """
    An independent organization exercising political and/or regulatory authority over a political unit, people,
    geographical region, etc., as well as performing certain functions for this unit or body.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["GovernmentOrganization"]
    class_class_curie: ClassVar[str] = "gist:GovernmentOrganization"
    class_name: ClassVar[str] = "GovernmentOrganization"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.GovernmentOrganization


class CountryGovernment(GovernmentOrganization):
    """
    A government organization which asserts both sovereignty (i.e., it is not governed by some other government
    organization) and governance over an entity generally recognized as a country.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["CountryGovernment"]
    class_class_curie: ClassVar[str] = "gist:CountryGovernment"
    class_name: ClassVar[str] = "CountryGovernment"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.CountryGovernment


class IntergovernmentalOrganization(Organization):
    """
    An organization whose members are government organizations. This can comprise regional, municipal, state/province,
    or national level entities.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["IntergovernmentalOrganization"]
    class_class_curie: ClassVar[str] = "gist:IntergovernmentalOrganization"
    class_name: ClassVar[str] = "IntergovernmentalOrganization"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.IntergovernmentalOrganization


class Permission(Intention):
    """
    A description of things one is permitted to do.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Permission"]
    class_class_curie: ClassVar[str] = "gist:Permission"
    class_name: ClassVar[str] = "Permission"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Permission


class PhysicalActionType(Category):
    """
    A category indicating the type of an action based on its effect in the physical world.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["PhysicalActionType"]
    class_class_curie: ClassVar[str] = "gist:PhysicalActionType"
    class_name: ClassVar[str] = "PhysicalActionType"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.PhysicalActionType


class PhysicalAddress(Address):
    """
    An address that refers to a locatable place within the physical universe.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["PhysicalAddress"]
    class_class_curie: ClassVar[str] = "gist:PhysicalAddress"
    class_name: ClassVar[str] = "PhysicalAddress"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.PhysicalAddress


class PhysicalAddressType(Category):
    """
    A category indicating local customary characterizations of physical addresses.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["PhysicalAddressType"]
    class_class_curie: ClassVar[str] = "gist:PhysicalAddressType"
    class_name: ClassVar[str] = "PhysicalAddressType"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.PhysicalAddressType


class PhysicalEvent(Event):
    """
    An event that can be said to have occurred at some place in space.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["PhysicalEvent"]
    class_class_curie: ClassVar[str] = "gist:PhysicalEvent"
    class_name: ClassVar[str] = "PhysicalEvent"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.PhysicalEvent


@dataclass(repr=False)
class PhysicalIdentifiableItem(YAMLRoot):
    """
    A discrete physical object which, if subdivided, will result in parts that are distinguishable in nature from the
    whole and in general also from the other parts.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["PhysicalIdentifiableItem"]
    class_class_curie: ClassVar[str] = "gist:PhysicalIdentifiableItem"
    class_name: ClassVar[str] = "PhysicalIdentifiableItem"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.PhysicalIdentifiableItem

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


class Equipment(PhysicalIdentifiableItem):
    """
    Human-made, tangible property other than land or buildings used to perform a task or activity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Equipment"]
    class_class_curie: ClassVar[str] = "gist:Equipment"
    class_name: ClassVar[str] = "Equipment"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Equipment


class Landmark(PhysicalIdentifiableItem):
    """
    Something permanently attached to the Earth.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Landmark"]
    class_class_curie: ClassVar[str] = "gist:Landmark"
    class_name: ClassVar[str] = "Landmark"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Landmark


class Building(Landmark):
    """
    A relatively permanent man-made structure situated on a plot of land, having a roof and walls, commonly used for
    dwelling, entertaining, or working.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Building"]
    class_class_curie: ClassVar[str] = "gist:Building"
    class_name: ClassVar[str] = "Building"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Building


class LivingThing(PhysicalIdentifiableItem):
    """
    Something that is currently, or at some point in time was, alive.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["LivingThing"]
    class_class_curie: ClassVar[str] = "gist:LivingThing"
    class_name: ClassVar[str] = "LivingThing"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.LivingThing


class Person(LivingThing):
    """
    A human being who was or is alive.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Person"]
    class_class_curie: ClassVar[str] = "gist:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Person


@dataclass(repr=False)
class PhysicalSubstance(YAMLRoot):
    """
    An undifferentiated amount of physical material which, when subdivided, results in each part being
    indistinguishable in nature from the whole and from every other part.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["PhysicalSubstance"]
    class_class_curie: ClassVar[str] = "gist:PhysicalSubstance"
    class_name: ClassVar[str] = "PhysicalSubstance"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.PhysicalSubstance

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


class ProductCategory(Category):
    """
    Any of many ways of categorizing products.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ProductCategory"]
    class_class_curie: ClassVar[str] = "gist:ProductCategory"
    class_name: ClassVar[str] = "ProductCategory"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ProductCategory


class ReferenceValue(Magnitude):
    """
    A magnitude that was neither measured nor estimated but set by fiat.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ReferenceValue"]
    class_class_curie: ClassVar[str] = "gist:ReferenceValue"
    class_name: ClassVar[str] = "ReferenceValue"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ReferenceValue


class RenderedContent(FormattedContent):
    """
    Content expressed via some physical medium.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["RenderedContent"]
    class_class_curie: ClassVar[str] = "gist:RenderedContent"
    class_name: ClassVar[str] = "RenderedContent"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.RenderedContent


class Requirement(Intention):
    """
    The obligation of a person or organization to behave in a certain way.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Requirement"]
    class_class_curie: ClassVar[str] = "gist:Requirement"
    class_name: ClassVar[str] = "Requirement"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Requirement


class Restriction(Intention):
    """
    A description of things one is prevented from doing.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Restriction"]
    class_class_curie: ClassVar[str] = "gist:Restriction"
    class_name: ClassVar[str] = "Restriction"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Restriction


class ScheduledEvent(Event):
    """
    An event with a planned start datetime.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ScheduledEvent"]
    class_class_curie: ClassVar[str] = "gist:ScheduledEvent"
    class_name: ClassVar[str] = "ScheduledEvent"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ScheduledEvent


class ScheduledTask(ScheduledEvent):
    """
    A task with a planned start datetime.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ScheduledTask"]
    class_class_curie: ClassVar[str] = "gist:ScheduledTask"
    class_name: ClassVar[str] = "ScheduledTask"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ScheduledTask


@dataclass(repr=False)
class SchemaMetaData(YAMLRoot):
    """
    Superclass for all types of metadata.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["SchemaMetaData"]
    class_class_curie: ClassVar[str] = "gist:SchemaMetaData"
    class_name: ClassVar[str] = "SchemaMetaData"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.SchemaMetaData

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


class Specification(Intention):
    """
    The set of characteristics and constraints on their values that specify what it means to be a particular type of
    thing, such as a material, product, service or event. A specification is sufficiently precise to allow evaluating
    conformance to the specification.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Specification"]
    class_class_curie: ClassVar[str] = "gist:Specification"
    class_name: ClassVar[str] = "Specification"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Specification


class CatalogItem(Specification):
    """
    A description of a product or service to be delivered, given in a sufficient level of detail that a receiver could
    determine whether delivery constituted discharge of the obligation to deliver.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["CatalogItem"]
    class_class_curie: ClassVar[str] = "gist:CatalogItem"
    class_name: ClassVar[str] = "CatalogItem"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.CatalogItem


class BundledCatalogItem(CatalogItem):
    """
    Any combination of descriptions of things offered together.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["BundledCatalogItem"]
    class_class_curie: ClassVar[str] = "gist:BundledCatalogItem"
    class_name: ClassVar[str] = "BundledCatalogItem"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.BundledCatalogItem


class ContractTerm(Specification):
    """
    A specification of some aspect of a contract.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ContractTerm"]
    class_class_curie: ClassVar[str] = "gist:ContractTerm"
    class_name: ClassVar[str] = "ContractTerm"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ContractTerm


class EventSpecification(Specification):
    """
    A characterization of an event that might happen.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["EventSpecification"]
    class_class_curie: ClassVar[str] = "gist:EventSpecification"
    class_name: ClassVar[str] = "EventSpecification"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.EventSpecification


class ProductSpecification(CatalogItem):
    """
    A description of something that could be physically warehoused or digitally stored and physically or digitally
    delivered.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ProductSpecification"]
    class_class_curie: ClassVar[str] = "gist:ProductSpecification"
    class_name: ClassVar[str] = "ProductSpecification"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ProductSpecification


class ServiceSpecification(CatalogItem):
    """
    A description of something that can be done for a person or organization (which produces some form of an act).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["ServiceSpecification"]
    class_class_curie: ClassVar[str] = "gist:ServiceSpecification"
    class_name: ClassVar[str] = "ServiceSpecification"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.ServiceSpecification


class SubCountryGovernment(GovernmentOrganization):
    """
    The government of a governed geographic region other than a country which is under the direct or indirect control
    of a country government.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["SubCountryGovernment"]
    class_class_curie: ClassVar[str] = "gist:SubCountryGovernment"
    class_name: ClassVar[str] = "SubCountryGovernment"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.SubCountryGovernment


class System(Composite):
    """
    A composite made up of interacting or interdependent components that together operate as a whole.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["System"]
    class_class_curie: ClassVar[str] = "gist:System"
    class_name: ClassVar[str] = "System"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.System


class Tag(Category):
    """
    A term in a folksonomy used to categorize things. Tags can be made up on the fly by users.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Tag"]
    class_class_curie: ClassVar[str] = "gist:Tag"
    class_name: ClassVar[str] = "Tag"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Tag


class Task(Event):
    """
    An activity or piece of work that is either proposed, planned, scheduled, underway, or completed.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Task"]
    class_class_curie: ClassVar[str] = "gist:Task"
    class_name: ClassVar[str] = "Task"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Task


class Project(Task):
    """
    A task, usually of longer duration, made up of other tasks.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Project"]
    class_class_curie: ClassVar[str] = "gist:Project"
    class_name: ClassVar[str] = "Project"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Project


@dataclass(repr=False)
class Template(YAMLRoot):
    """
    Something used to make objects in its own image.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Template"]
    class_class_curie: ClassVar[str] = "gist:Template"
    class_name: ClassVar[str] = "Template"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Template

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


class TaskTemplate(Template):
    """
    An outline of a task of a particular type, which is the basis for executing such tasks.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["TaskTemplate"]
    class_class_curie: ClassVar[str] = "gist:TaskTemplate"
    class_name: ClassVar[str] = "TaskTemplate"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.TaskTemplate


@dataclass(repr=False)
class TemporalRelation(YAMLRoot):
    """
    A relationship existing for a period of time.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["TemporalRelation"]
    class_class_curie: ClassVar[str] = "gist:TemporalRelation"
    class_name: ClassVar[str] = "TemporalRelation"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.TemporalRelation

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


class Assignment(TemporalRelation):
    """
    A temporal relationship between an assignee, the thing assigned, and the resource that made the assignment.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Assignment"]
    class_class_curie: ClassVar[str] = "gist:Assignment"
    class_name: ClassVar[str] = "Assignment"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Assignment


class Text(ContentExpression):
    """
    Content expressed as a written sequence of characters.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Text"]
    class_class_curie: ClassVar[str] = "gist:Text"
    class_name: ClassVar[str] = "Text"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Text


@dataclass(repr=False)
class TimeInterval(YAMLRoot):
    """
    A span of time with a known start time, end time, and duration. As long as two of the three are known, the third
    can be inferred.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["TimeInterval"]
    class_class_curie: ClassVar[str] = "gist:TimeInterval"
    class_name: ClassVar[str] = "TimeInterval"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.TimeInterval

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


class Transaction(Event):
    """
    An exchange or transfer of goods, services, or funds.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["Transaction"]
    class_class_curie: ClassVar[str] = "gist:Transaction"
    class_name: ClassVar[str] = "Transaction"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.Transaction


class UnitGroup(Collection):
    """
    A collection of units of measure that can all be used to measure the same aspects.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["UnitGroup"]
    class_class_curie: ClassVar[str] = "gist:UnitGroup"
    class_name: ClassVar[str] = "UnitGroup"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.UnitGroup


@dataclass(repr=False)
class UnitOfMeasure(YAMLRoot):
    """
    A standard amount used to measure or specify things.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST["UnitOfMeasure"]
    class_class_curie: ClassVar[str] = "gist:UnitOfMeasure"
    class_name: ClassVar[str] = "UnitOfMeasure"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.UnitOfMeasure

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GistThing(YAMLRoot):
    """
    Mixin providing universal slots applicable to any GIST entity. Covers OWL properties with no rdfs:domain
    (open-world).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = GIST_LINKML["GistThing"]
    class_class_curie: ClassVar[str] = "gist_linkml:GistThing"
    class_name: ClassVar[str] = "GistThing"
    class_model_uri: ClassVar[URIRef] = GIST_LINKML.GistThing

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


Any = Any

# Enumerations
class AspectInstance(EnumDefinitionImpl):
    """
    Named instances of gist:Aspect from gist reference data.
    """
    ASPECT_ALTITUDE = PermissibleValue(
        text="ASPECT_ALTITUDE",
        title="altitude",
        description="The aspect altitude.",
        meaning=GISTD["_Aspect_altitude"])
    ASPECT_AREA = PermissibleValue(
        text="ASPECT_AREA",
        title="area",
        description="The aspect area.",
        meaning=GISTD["_Aspect_area"])
    ASPECT_DURATION = PermissibleValue(
        text="ASPECT_DURATION",
        title="duration",
        description="The aspect duration.",
        meaning=GISTD["_Aspect_duration"])
    ASPECT_FINANCIAL_BALANCE = PermissibleValue(
        text="ASPECT_FINANCIAL_BALANCE",
        title="balance",
        description="The aspect financial balance.",
        meaning=GISTD["_Aspect_financial_balance"])
    ASPECT_MASS = PermissibleValue(
        text="ASPECT_MASS",
        title="mass",
        description="The aspect mass.",
        meaning=GISTD["_Aspect_mass"])
    ASPECT_MONETARY_VALUE = PermissibleValue(
        text="ASPECT_MONETARY_VALUE",
        title="monetary value",
        description="The aspect monetary value.",
        meaning=GISTD["_Aspect_monetary_value"])
    ASPECT_PROBABILITY = PermissibleValue(
        text="ASPECT_PROBABILITY",
        title="probability",
        description="The aspect probability.",
        meaning=GISTD["_Aspect_probability"])
    ASPECT_VOLUME = PermissibleValue(
        text="ASPECT_VOLUME",
        title="volume",
        description="The aspect volume.",
        meaning=GISTD["_Aspect_volume"])

    _defn = EnumDefinition(
        name="AspectInstance",
        description="Named instances of gist:Aspect from gist reference data.",
    )

class MediaTypeInstance(EnumDefinitionImpl):
    """
    Named instances of gist:MediaType from gist reference data.
    """
    JSON = PermissibleValue(
        text="JSON",
        title="JSON",
        meaning=MEDIA_APP["json"])
    LD_PLUS_JSON = PermissibleValue(
        text="LD_PLUS_JSON",
        title="JSON-LD",
        meaning=MEDIA_APP["ld+json"])
    N_QUADS = PermissibleValue(
        text="N_QUADS",
        title="N-Quads",
        meaning=MEDIA_APP["n-quads"])
    N_TRIPLES = PermissibleValue(
        text="N_TRIPLES",
        title="N-Triples",
        meaning=MEDIA_APP["n-triples"])
    RDF_PLUS_XML = PermissibleValue(
        text="RDF_PLUS_XML",
        title="RDF/XML",
        meaning=MEDIA_APP["rdf+xml"])
    SPARQL_RESULTS_PLUS_JSON = PermissibleValue(
        text="SPARQL_RESULTS_PLUS_JSON",
        title="SPARQL 1.1 Query Results JSON",
        meaning=MEDIA_APP["sparql-results+json"])
    SPARQL_RESULTS_PLUS_XML = PermissibleValue(
        text="SPARQL_RESULTS_PLUS_XML",
        title="SPARQL 1.1 Query Results XML",
        meaning=MEDIA_APP["sparql-results+xml"])
    TRIG = PermissibleValue(
        text="TRIG",
        title="TriG",
        meaning=MEDIA_APP["trig"])
    JPG = PermissibleValue(
        text="JPG",
        title="JPG",
        meaning=MEDIA_IMG["jpg"])
    PNG = PermissibleValue(
        text="PNG",
        title="PNG",
        meaning=MEDIA_IMG["png"])
    CSV = PermissibleValue(
        text="CSV",
        title="CSV",
        meaning=MEDIA_TXT["csv"])
    HTML = PermissibleValue(
        text="HTML",
        title="HTML",
        meaning=MEDIA_TXT["html"])
    PLAIN = PermissibleValue(
        text="PLAIN",
        title="Plain Text",
        meaning=MEDIA_TXT["plain"])
    TURTLE = PermissibleValue(
        text="TURTLE",
        title="Turtle",
        meaning=MEDIA_TXT["turtle"])

    _defn = EnumDefinition(
        name="MediaTypeInstance",
        description="Named instances of gist:MediaType from gist reference data.",
    )

class PrefixDeclarationInstance(EnumDefinitionImpl):
    """
    Named SHACL prefix declarations from the gist ontology.
    """
    PREFIXDECLARATION_GIST = PermissibleValue(
        text="PREFIXDECLARATION_GIST",
        title="gist",
        description="Prefix 'gist' for namespace <https://w3id.org/semanticarts/ns/ontology/gist/>.",
        meaning=GIST["_PrefixDeclaration_gist"])
    PREFIXDECLARATION_OWL = PermissibleValue(
        text="PREFIXDECLARATION_OWL",
        title="owl",
        description="Prefix 'owl' for namespace <http://www.w3.org/2002/07/owl#>.",
        meaning=GIST["_PrefixDeclaration_owl"])
    PREFIXDECLARATION_RDF = PermissibleValue(
        text="PREFIXDECLARATION_RDF",
        title="rdf",
        description="Prefix 'rdf' for namespace <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.",
        meaning=GIST["_PrefixDeclaration_rdf"])
    PREFIXDECLARATION_RDFS = PermissibleValue(
        text="PREFIXDECLARATION_RDFS",
        title="rdfs",
        description="Prefix 'rdfs' for namespace <http://www.w3.org/2000/01/rdf-schema#>.",
        meaning=GIST["_PrefixDeclaration_rdfs"])
    PREFIXDECLARATION_SH = PermissibleValue(
        text="PREFIXDECLARATION_SH",
        title="sh",
        description="Prefix 'sh' for namespace <http://www.w3.org/ns/shacl#>.",
        meaning=GIST["_PrefixDeclaration_sh"])
    PREFIXDECLARATION_SKOS = PermissibleValue(
        text="PREFIXDECLARATION_SKOS",
        title="skos",
        description="Prefix 'skos' for namespace <http://www.w3.org/2004/02/skos/core#>.",
        meaning=GIST["_PrefixDeclaration_skos"])
    PREFIXDECLARATION_XSD = PermissibleValue(
        text="PREFIXDECLARATION_XSD",
        title="xsd",
        description="Prefix 'xsd' for namespace <http://www.w3.org/2001/XMLSchema#>.",
        meaning=GIST["_PrefixDeclaration_xsd"])

    _defn = EnumDefinition(
        name="PrefixDeclarationInstance",
        description="Named SHACL prefix declarations from the gist ontology.",
    )

# Slots
class slots:
    pass

slots.allows = Slot(uri=GIST.allows, name="allows", curie=GIST.curie('allows'),
                   model_uri=GIST_LINKML.allows, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.comes_from_agent = Slot(uri=GIST.comesFromAgent, name="comes_from_agent", curie=GIST.curie('comesFromAgent'),
                   model_uri=GIST_LINKML.comes_from_agent, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.comes_from_place = Slot(uri=GIST.comesFromPlace, name="comes_from_place", curie=GIST.curie('comesFromPlace'),
                   model_uri=GIST_LINKML.comes_from_place, domain=None, range=Optional[Union[str, list[str]]])

slots.conforms_to = Slot(uri=GIST.conformsTo, name="conforms_to", curie=GIST.curie('conformsTo'),
                   model_uri=GIST_LINKML.conforms_to, domain=None, range=Optional[Union[Union[dict, Intention], list[Union[dict, Intention]]]])

slots.contributes_to = Slot(uri=GIST.contributesTo, name="contributes_to", curie=GIST.curie('contributesTo'),
                   model_uri=GIST_LINKML.contributes_to, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.goes_to_agent = Slot(uri=GIST.goesToAgent, name="goes_to_agent", curie=GIST.curie('goesToAgent'),
                   model_uri=GIST_LINKML.goes_to_agent, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.goes_to_place = Slot(uri=GIST.goesToPlace, name="goes_to_place", curie=GIST.curie('goesToPlace'),
                   model_uri=GIST_LINKML.goes_to_place, domain=None, range=Optional[Union[str, list[str]]])

slots.has_accuracy = Slot(uri=GIST.hasAccuracy, name="has_accuracy", curie=GIST.curie('hasAccuracy'),
                   model_uri=GIST_LINKML.has_accuracy, domain=Magnitude, range=Optional[Union[dict, "Magnitude"]])

slots.has_addend = Slot(uri=GIST.hasAddend, name="has_addend", curie=GIST.curie('hasAddend'),
                   model_uri=GIST_LINKML.has_addend, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.has_address = Slot(uri=GIST.hasAddress, name="has_address", curie=GIST.curie('hasAddress'),
                   model_uri=GIST_LINKML.has_address, domain=None, range=Optional[Union[Union[dict, Address], list[Union[dict, Address]]]])

slots.has_aspect = Slot(uri=GIST.hasAspect, name="has_aspect", curie=GIST.curie('hasAspect'),
                   model_uri=GIST_LINKML.has_aspect, domain=None, range=Optional[Union[dict, Aspect]])

slots.has_biological_parent = Slot(uri=GIST.hasBiologicalParent, name="has_biological_parent", curie=GIST.curie('hasBiologicalParent'),
                   model_uri=GIST_LINKML.has_biological_parent, domain=LivingThing, range=Optional[Union[Union[dict, "LivingThing"], list[Union[dict, "LivingThing"]]]])

slots.has_broader = Slot(uri=GIST.hasBroader, name="has_broader", curie=GIST.curie('hasBroader'),
                   model_uri=GIST_LINKML.has_broader, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.has_direct_broader = Slot(uri=GIST.hasDirectBroader, name="has_direct_broader", curie=GIST.curie('hasDirectBroader'),
                   model_uri=GIST_LINKML.has_direct_broader, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.has_divisor = Slot(uri=GIST.hasDivisor, name="has_divisor", curie=GIST.curie('hasDivisor'),
                   model_uri=GIST_LINKML.has_divisor, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.has_giver = Slot(uri=GIST.hasGiver, name="has_giver", curie=GIST.curie('hasGiver'),
                   model_uri=GIST_LINKML.has_giver, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.has_goal = Slot(uri=GIST.hasGoal, name="has_goal", curie=GIST.curie('hasGoal'),
                   model_uri=GIST_LINKML.has_goal, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.has_incumbent = Slot(uri=GIST.hasIncumbent, name="has_incumbent", curie=GIST.curie('hasIncumbent'),
                   model_uri=GIST_LINKML.has_incumbent, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.has_magnitude = Slot(uri=GIST.hasMagnitude, name="has_magnitude", curie=GIST.curie('hasMagnitude'),
                   model_uri=GIST_LINKML.has_magnitude, domain=None, range=Optional[Union[Union[dict, Magnitude], list[Union[dict, Magnitude]]]])

slots.has_multiplier = Slot(uri=GIST.hasMultiplier, name="has_multiplier", curie=GIST.curie('hasMultiplier'),
                   model_uri=GIST_LINKML.has_multiplier, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.has_navigational_parent = Slot(uri=GIST.hasNavigationalParent, name="has_navigational_parent", curie=GIST.curie('hasNavigationalParent'),
                   model_uri=GIST_LINKML.has_navigational_parent, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.has_participant = Slot(uri=GIST.hasParticipant, name="has_participant", curie=GIST.curie('hasParticipant'),
                   model_uri=GIST_LINKML.has_participant, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.has_party = Slot(uri=GIST.hasParty, name="has_party", curie=GIST.curie('hasParty'),
                   model_uri=GIST_LINKML.has_party, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.has_physical_location = Slot(uri=GIST.hasPhysicalLocation, name="has_physical_location", curie=GIST.curie('hasPhysicalLocation'),
                   model_uri=GIST_LINKML.has_physical_location, domain=None, range=Optional[Union[Union[dict, GeoLocation], list[Union[dict, GeoLocation]]]])

slots.has_recipient = Slot(uri=GIST.hasRecipient, name="has_recipient", curie=GIST.curie('hasRecipient'),
                   model_uri=GIST_LINKML.has_recipient, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.has_subtrahend = Slot(uri=GIST.hasSubtrahend, name="has_subtrahend", curie=GIST.curie('hasSubtrahend'),
                   model_uri=GIST_LINKML.has_subtrahend, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.has_unique_broader = Slot(uri=GIST.hasUniqueBroader, name="has_unique_broader", curie=GIST.curie('hasUniqueBroader'),
                   model_uri=GIST_LINKML.has_unique_broader, domain=None, range=Optional[Union[dict, Any]])

slots.has_unique_navigational_parent = Slot(uri=GIST.hasUniqueNavigationalParent, name="has_unique_navigational_parent", curie=GIST.curie('hasUniqueNavigationalParent'),
                   model_uri=GIST_LINKML.has_unique_navigational_parent, domain=None, range=Optional[Union[dict, Any]])

slots.has_unit_group = Slot(uri=GIST.hasUnitGroup, name="has_unit_group", curie=GIST.curie('hasUnitGroup'),
                   model_uri=GIST_LINKML.has_unit_group, domain=Aspect, range=Optional[Union[Union[dict, "UnitGroup"], list[Union[dict, "UnitGroup"]]]])

slots.has_unit_of_measure = Slot(uri=GIST.hasUnitOfMeasure, name="has_unit_of_measure", curie=GIST.curie('hasUnitOfMeasure'),
                   model_uri=GIST_LINKML.has_unit_of_measure, domain=Magnitude, range=Optional[Union[Union[dict, "UnitOfMeasure"], list[Union[dict, "UnitOfMeasure"]]]])

slots.is_about = Slot(uri=GIST.isAbout, name="is_about", curie=GIST.curie('isAbout'),
                   model_uri=GIST_LINKML.is_about, domain=Content, range=Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]])

slots.is_affected_by = Slot(uri=GIST.isAffectedBy, name="is_affected_by", curie=GIST.curie('isAffectedBy'),
                   model_uri=GIST_LINKML.is_affected_by, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.is_allocated_by = Slot(uri=GIST.isAllocatedBy, name="is_allocated_by", curie=GIST.curie('isAllocatedBy'),
                   model_uri=GIST_LINKML.is_allocated_by, domain=None, range=Optional[Union[str, list[str]]])

slots.is_assignment_of = Slot(uri=GIST.isAssignmentOf, name="is_assignment_of", curie=GIST.curie('isAssignmentOf'),
                   model_uri=GIST_LINKML.is_assignment_of, domain=Assignment, range=Optional[Union[str, list[str]]])

slots.is_assignment_to = Slot(uri=GIST.isAssignmentTo, name="is_assignment_to", curie=GIST.curie('isAssignmentTo'),
                   model_uri=GIST_LINKML.is_assignment_to, domain=Assignment, range=Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]])

slots.is_based_on = Slot(uri=GIST.isBasedOn, name="is_based_on", curie=GIST.curie('isBasedOn'),
                   model_uri=GIST_LINKML.is_based_on, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.is_categorized_by = Slot(uri=GIST.isCategorizedBy, name="is_categorized_by", curie=GIST.curie('isCategorizedBy'),
                   model_uri=GIST_LINKML.is_categorized_by, domain=None, range=Optional[Union[Union[dict, Category], list[Union[dict, Category]]]])

slots.is_connected_to = Slot(uri=GIST.isConnectedTo, name="is_connected_to", curie=GIST.curie('isConnectedTo'),
                   model_uri=GIST_LINKML.is_connected_to, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.is_direct_part_of = Slot(uri=GIST.isDirectPartOf, name="is_direct_part_of", curie=GIST.curie('isDirectPartOf'),
                   model_uri=GIST_LINKML.is_direct_part_of, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.is_expressed_in = Slot(uri=GIST.isExpressedIn, name="is_expressed_in", curie=GIST.curie('isExpressedIn'),
                   model_uri=GIST_LINKML.is_expressed_in, domain=Text, range=Optional[Union[Union[dict, Language], list[Union[dict, Language]]]])

slots.is_first_member_of = Slot(uri=GIST.isFirstMemberOf, name="is_first_member_of", curie=GIST.curie('isFirstMemberOf'),
                   model_uri=GIST_LINKML.is_first_member_of, domain=OrderedMember, range=Optional[Union[dict, OrderedCollection]])

slots.is_geo_contained_in = Slot(uri=GIST.isGeoContainedIn, name="is_geo_contained_in", curie=GIST.curie('isGeoContainedIn'),
                   model_uri=GIST_LINKML.is_geo_contained_in, domain=GeoLocation, range=Optional[Union[Union[dict, "GeoLocation"], list[Union[dict, "GeoLocation"]]]])

slots.is_governed_by = Slot(uri=GIST.isGovernedBy, name="is_governed_by", curie=GIST.curie('isGovernedBy'),
                   model_uri=GIST_LINKML.is_governed_by, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.is_identified_by = Slot(uri=GIST.isIdentifiedBy, name="is_identified_by", curie=GIST.curie('isIdentifiedBy'),
                   model_uri=GIST_LINKML.is_identified_by, domain=None, range=Optional[Union[Union[dict, ID], list[Union[dict, ID]]]])

slots.is_made_up_of = Slot(uri=GIST.isMadeUpOf, name="is_made_up_of", curie=GIST.curie('isMadeUpOf'),
                   model_uri=GIST_LINKML.is_made_up_of, domain=None, range=Optional[Union[Union[dict, PhysicalSubstance], list[Union[dict, PhysicalSubstance]]]])

slots.is_member_of = Slot(uri=GIST.isMemberOf, name="is_member_of", curie=GIST.curie('isMemberOf'),
                   model_uri=GIST_LINKML.is_member_of, domain=None, range=Optional[Union[str, list[str]]])

slots.is_part_of = Slot(uri=GIST.isPartOf, name="is_part_of", curie=GIST.curie('isPartOf'),
                   model_uri=GIST_LINKML.is_part_of, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.is_produced_by = Slot(uri=GIST.isProducedBy, name="is_produced_by", curie=GIST.curie('isProducedBy'),
                   model_uri=GIST_LINKML.is_produced_by, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.is_recognized_by = Slot(uri=GIST.isRecognizedBy, name="is_recognized_by", curie=GIST.curie('isRecognizedBy'),
                   model_uri=GIST_LINKML.is_recognized_by, domain=None, range=Optional[Union[str, list[str]]])

slots.is_rendered_on = Slot(uri=GIST.isRenderedOn, name="is_rendered_on", curie=GIST.curie('isRenderedOn'),
                   model_uri=GIST_LINKML.is_rendered_on, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.is_triggered_by = Slot(uri=GIST.isTriggeredBy, name="is_triggered_by", curie=GIST.curie('isTriggeredBy'),
                   model_uri=GIST_LINKML.is_triggered_by, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.is_under_jurisdiction_of = Slot(uri=GIST.isUnderJurisdictionOf, name="is_under_jurisdiction_of", curie=GIST.curie('isUnderJurisdictionOf'),
                   model_uri=GIST_LINKML.is_under_jurisdiction_of, domain=None, range=Optional[Union[Union[dict, GovernmentOrganization], list[Union[dict, GovernmentOrganization]]]])

slots.links = Slot(uri=GIST.links, name="links", curie=GIST.curie('links'),
                   model_uri=GIST_LINKML.links, domain=NetworkLink, range=Optional[Union[Union[dict, "NetworkNode"], list[Union[dict, "NetworkNode"]]]])

slots.links_from = Slot(uri=GIST.linksFrom, name="links_from", curie=GIST.curie('linksFrom'),
                   model_uri=GIST_LINKML.links_from, domain=NetworkLink, range=Optional[Union[Union[dict, "NetworkNode"], list[Union[dict, "NetworkNode"]]]])

slots.links_to = Slot(uri=GIST.linksTo, name="links_to", curie=GIST.curie('linksTo'),
                   model_uri=GIST_LINKML.links_to, domain=NetworkLink, range=Optional[Union[Union[dict, "NetworkNode"], list[Union[dict, "NetworkNode"]]]])

slots.occurs_in = Slot(uri=GIST.occursIn, name="occurs_in", curie=GIST.curie('occursIn'),
                   model_uri=GIST_LINKML.occurs_in, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.offers_to_provide = Slot(uri=GIST.offersToProvide, name="offers_to_provide", curie=GIST.curie('offersToProvide'),
                   model_uri=GIST_LINKML.offers_to_provide, domain=Offer, range=Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]])

slots.offers_to_receive = Slot(uri=GIST.offersToReceive, name="offers_to_receive", curie=GIST.curie('offersToReceive'),
                   model_uri=GIST_LINKML.offers_to_receive, domain=Offer, range=Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]])

slots.owns = Slot(uri=GIST.owns, name="owns", curie=GIST.curie('owns'),
                   model_uri=GIST_LINKML.owns, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.precedes = Slot(uri=GIST.precedes, name="precedes", curie=GIST.curie('precedes'),
                   model_uri=GIST_LINKML.precedes, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.precedes_directly = Slot(uri=GIST.precedesDirectly, name="precedes_directly", curie=GIST.curie('precedesDirectly'),
                   model_uri=GIST_LINKML.precedes_directly, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.prevents = Slot(uri=GIST.prevents, name="prevents", curie=GIST.curie('prevents'),
                   model_uri=GIST_LINKML.prevents, domain=Intention, range=Optional[Union[Union[dict, Behavior], list[Union[dict, Behavior]]]])

slots.prohibits = Slot(uri=GIST.prohibits, name="prohibits", curie=GIST.curie('prohibits'),
                   model_uri=GIST_LINKML.prohibits, domain=Intention, range=Optional[Union[Union[dict, Behavior], list[Union[dict, Behavior]]]])

slots.provides_order_for = Slot(uri=GIST.providesOrderFor, name="provides_order_for", curie=GIST.curie('providesOrderFor'),
                   model_uri=GIST_LINKML.provides_order_for, domain=OrderedMember, range=Optional[Union[dict, "Any"]])

slots.refers_to = Slot(uri=GIST.refersTo, name="refers_to", curie=GIST.curie('refersTo'),
                   model_uri=GIST_LINKML.refers_to, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.requires = Slot(uri=GIST.requires, name="requires", curie=GIST.curie('requires'),
                   model_uri=GIST_LINKML.requires, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.actual_end_date = Slot(uri=GIST.actualEndDate, name="actual_end_date", curie=GIST.curie('actualEndDate'),
                   model_uri=GIST_LINKML.actual_end_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.actual_end_date_time = Slot(uri=GIST.actualEndDateTime, name="actual_end_date_time", curie=GIST.curie('actualEndDateTime'),
                   model_uri=GIST_LINKML.actual_end_date_time, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.actual_end_microsecond = Slot(uri=GIST.actualEndMicrosecond, name="actual_end_microsecond", curie=GIST.curie('actualEndMicrosecond'),
                   model_uri=GIST_LINKML.actual_end_microsecond, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.actual_end_minute = Slot(uri=GIST.actualEndMinute, name="actual_end_minute", curie=GIST.curie('actualEndMinute'),
                   model_uri=GIST_LINKML.actual_end_minute, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.actual_end_year = Slot(uri=GIST.actualEndYear, name="actual_end_year", curie=GIST.curie('actualEndYear'),
                   model_uri=GIST_LINKML.actual_end_year, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.actual_start_date = Slot(uri=GIST.actualStartDate, name="actual_start_date", curie=GIST.curie('actualStartDate'),
                   model_uri=GIST_LINKML.actual_start_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.actual_start_date_time = Slot(uri=GIST.actualStartDateTime, name="actual_start_date_time", curie=GIST.curie('actualStartDateTime'),
                   model_uri=GIST_LINKML.actual_start_date_time, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.actual_start_microsecond = Slot(uri=GIST.actualStartMicrosecond, name="actual_start_microsecond", curie=GIST.curie('actualStartMicrosecond'),
                   model_uri=GIST_LINKML.actual_start_microsecond, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.actual_start_minute = Slot(uri=GIST.actualStartMinute, name="actual_start_minute", curie=GIST.curie('actualStartMinute'),
                   model_uri=GIST_LINKML.actual_start_minute, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.actual_start_year = Slot(uri=GIST.actualStartYear, name="actual_start_year", curie=GIST.curie('actualStartYear'),
                   model_uri=GIST_LINKML.actual_start_year, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.at_date_time = Slot(uri=GIST.atDateTime, name="at_date_time", curie=GIST.curie('atDateTime'),
                   model_uri=GIST_LINKML.at_date_time, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.birth_date = Slot(uri=GIST.birthDate, name="birth_date", curie=GIST.curie('birthDate'),
                   model_uri=GIST_LINKML.birth_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.contained_text = Slot(uri=GIST.containedText, name="contained_text", curie=GIST.curie('containedText'),
                   model_uri=GIST_LINKML.contained_text, domain=None, range=Optional[str])

slots.conversion_factor = Slot(uri=GIST.conversionFactor, name="conversion_factor", curie=GIST.curie('conversionFactor'),
                   model_uri=GIST_LINKML.conversion_factor, domain=UnitOfMeasure, range=Optional[str])

slots.conversion_offset = Slot(uri=GIST.conversionOffset, name="conversion_offset", curie=GIST.curie('conversionOffset'),
                   model_uri=GIST_LINKML.conversion_offset, domain=UnitOfMeasure, range=Optional[Decimal])

slots.death_date = Slot(uri=GIST.deathDate, name="death_date", curie=GIST.curie('deathDate'),
                   model_uri=GIST_LINKML.death_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.description = Slot(uri=GIST.description, name="description", curie=GIST.curie('description'),
                   model_uri=GIST_LINKML.description, domain=None, range=Optional[str])

slots.encrypted_text = Slot(uri=GIST.encryptedText, name="encrypted_text", curie=GIST.curie('encryptedText'),
                   model_uri=GIST_LINKML.encrypted_text, domain=None, range=Optional[str])

slots.end_date_time = Slot(uri=GIST.endDateTime, name="end_date_time", curie=GIST.curie('endDateTime'),
                   model_uri=GIST_LINKML.end_date_time, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.exponent_of_ampere = Slot(uri=GIST.exponentOfAmpere, name="exponent_of_ampere", curie=GIST.curie('exponentOfAmpere'),
                   model_uri=GIST_LINKML.exponent_of_ampere, domain=None, range=Optional[Decimal])

slots.exponent_of_bit = Slot(uri=GIST.exponentOfBit, name="exponent_of_bit", curie=GIST.curie('exponentOfBit'),
                   model_uri=GIST_LINKML.exponent_of_bit, domain=None, range=Optional[Decimal])

slots.exponent_of_candela = Slot(uri=GIST.exponentOfCandela, name="exponent_of_candela", curie=GIST.curie('exponentOfCandela'),
                   model_uri=GIST_LINKML.exponent_of_candela, domain=None, range=Optional[Decimal])

slots.exponent_of_kelvin = Slot(uri=GIST.exponentOfKelvin, name="exponent_of_kelvin", curie=GIST.curie('exponentOfKelvin'),
                   model_uri=GIST_LINKML.exponent_of_kelvin, domain=None, range=Optional[Decimal])

slots.exponent_of_kilogram = Slot(uri=GIST.exponentOfKilogram, name="exponent_of_kilogram", curie=GIST.curie('exponentOfKilogram'),
                   model_uri=GIST_LINKML.exponent_of_kilogram, domain=None, range=Optional[Decimal])

slots.exponent_of_meter = Slot(uri=GIST.exponentOfMeter, name="exponent_of_meter", curie=GIST.curie('exponentOfMeter'),
                   model_uri=GIST_LINKML.exponent_of_meter, domain=None, range=Optional[Decimal])

slots.exponent_of_mole = Slot(uri=GIST.exponentOfMole, name="exponent_of_mole", curie=GIST.curie('exponentOfMole'),
                   model_uri=GIST_LINKML.exponent_of_mole, domain=None, range=Optional[Decimal])

slots.exponent_of_number = Slot(uri=GIST.exponentOfNumber, name="exponent_of_number", curie=GIST.curie('exponentOfNumber'),
                   model_uri=GIST_LINKML.exponent_of_number, domain=None, range=Optional[Decimal])

slots.exponent_of_other = Slot(uri=GIST.exponentOfOther, name="exponent_of_other", curie=GIST.curie('exponentOfOther'),
                   model_uri=GIST_LINKML.exponent_of_other, domain=None, range=Optional[Decimal])

slots.exponent_of_radian = Slot(uri=GIST.exponentOfRadian, name="exponent_of_radian", curie=GIST.curie('exponentOfRadian'),
                   model_uri=GIST_LINKML.exponent_of_radian, domain=None, range=Optional[Decimal])

slots.exponent_of_second = Slot(uri=GIST.exponentOfSecond, name="exponent_of_second", curie=GIST.curie('exponentOfSecond'),
                   model_uri=GIST_LINKML.exponent_of_second, domain=None, range=Optional[Decimal])

slots.exponent_of_steradian = Slot(uri=GIST.exponentOfSteradian, name="exponent_of_steradian", curie=GIST.curie('exponentOfSteradian'),
                   model_uri=GIST_LINKML.exponent_of_steradian, domain=None, range=Optional[Decimal])

slots.exponent_of_us_dollar = Slot(uri=GIST.exponentOfUSDollar, name="exponent_of_us_dollar", curie=GIST.curie('exponentOfUSDollar'),
                   model_uri=GIST_LINKML.exponent_of_us_dollar, domain=None, range=Optional[Decimal])

slots.id_text = Slot(uri=GIST.idText, name="id_text", curie=GIST.curie('idText'),
                   model_uri=GIST_LINKML.id_text, domain=None, range=Optional[str])

slots.is_recorded_at = Slot(uri=GIST.isRecordedAt, name="is_recorded_at", curie=GIST.curie('isRecordedAt'),
                   model_uri=GIST_LINKML.is_recorded_at, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.latitude = Slot(uri=GIST.latitude, name="latitude", curie=GIST.curie('latitude'),
                   model_uri=GIST_LINKML.latitude, domain=GeoPoint, range=Optional[float])

slots.longitude = Slot(uri=GIST.longitude, name="longitude", curie=GIST.curie('longitude'),
                   model_uri=GIST_LINKML.longitude, domain=GeoPoint, range=Optional[float])

slots.name = Slot(uri=GIST.name, name="name", curie=GIST.curie('name'),
                   model_uri=GIST_LINKML.name, domain=None, range=Optional[str])

slots.numeric_value = Slot(uri=GIST.numericValue, name="numeric_value", curie=GIST.curie('numericValue'),
                   model_uri=GIST_LINKML.numeric_value, domain=None, range=Optional[str])

slots.planned_end_date = Slot(uri=GIST.plannedEndDate, name="planned_end_date", curie=GIST.curie('plannedEndDate'),
                   model_uri=GIST_LINKML.planned_end_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.planned_end_date_time = Slot(uri=GIST.plannedEndDateTime, name="planned_end_date_time", curie=GIST.curie('plannedEndDateTime'),
                   model_uri=GIST_LINKML.planned_end_date_time, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.planned_end_minute = Slot(uri=GIST.plannedEndMinute, name="planned_end_minute", curie=GIST.curie('plannedEndMinute'),
                   model_uri=GIST_LINKML.planned_end_minute, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.planned_end_year = Slot(uri=GIST.plannedEndYear, name="planned_end_year", curie=GIST.curie('plannedEndYear'),
                   model_uri=GIST_LINKML.planned_end_year, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.planned_start_date = Slot(uri=GIST.plannedStartDate, name="planned_start_date", curie=GIST.curie('plannedStartDate'),
                   model_uri=GIST_LINKML.planned_start_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.planned_start_date_time = Slot(uri=GIST.plannedStartDateTime, name="planned_start_date_time", curie=GIST.curie('plannedStartDateTime'),
                   model_uri=GIST_LINKML.planned_start_date_time, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.planned_start_minute = Slot(uri=GIST.plannedStartMinute, name="planned_start_minute", curie=GIST.curie('plannedStartMinute'),
                   model_uri=GIST_LINKML.planned_start_minute, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.planned_start_year = Slot(uri=GIST.plannedStartYear, name="planned_start_year", curie=GIST.curie('plannedStartYear'),
                   model_uri=GIST_LINKML.planned_start_year, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.sequence = Slot(uri=GIST.sequence, name="sequence", curie=GIST.curie('sequence'),
                   model_uri=GIST_LINKML.sequence, domain=OrderedMember, range=Optional[int])

slots.start_date_time = Slot(uri=GIST.startDateTime, name="start_date_time", curie=GIST.curie('startDateTime'),
                   model_uri=GIST_LINKML.start_date_time, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.symbol = Slot(uri=GIST.symbol, name="symbol", curie=GIST.curie('symbol'),
                   model_uri=GIST_LINKML.symbol, domain=UnitOfMeasure, range=Optional[str])

slots.unique_text = Slot(uri=GIST.uniqueText, name="unique_text", curie=GIST.curie('uniqueText'),
                   model_uri=GIST_LINKML.unique_text, domain=None, range=Optional[str])

slots.domain_includes = Slot(uri=GIST.domainIncludes, name="domain_includes", curie=GIST.curie('domainIncludes'),
                   model_uri=GIST_LINKML.domain_includes, domain=None, range=Optional[str])

slots.is_superseded_by = Slot(uri=GIST.isSupersededBy, name="is_superseded_by", curie=GIST.curie('isSupersededBy'),
                   model_uri=GIST_LINKML.is_superseded_by, domain=None, range=Optional[str])

slots.license = Slot(uri=GIST.license, name="license", curie=GIST.curie('license'),
                   model_uri=GIST_LINKML.license, domain=None, range=Optional[str])

slots.range_includes = Slot(uri=GIST.rangeIncludes, name="range_includes", curie=GIST.curie('rangeIncludes'),
                   model_uri=GIST_LINKML.range_includes, domain=None, range=Optional[str])
