/**
* Named instances of gist:Aspect from gist reference data.
*/
export enum AspectInstance {
    
    /** The aspect altitude. */
    altitude = "ASPECT_ALTITUDE",
    /** The aspect area. */
    area = "ASPECT_AREA",
    /** The aspect duration. */
    duration = "ASPECT_DURATION",
    /** The aspect financial balance. */
    balance = "ASPECT_FINANCIAL_BALANCE",
    /** The aspect mass. */
    mass = "ASPECT_MASS",
    /** The aspect monetary value. */
    monetary_value = "ASPECT_MONETARY_VALUE",
    /** The aspect probability. */
    probability = "ASPECT_PROBABILITY",
    /** The aspect volume. */
    volume = "ASPECT_VOLUME",
};
/**
* Named instances of gist:MediaType from gist reference data.
*/
export enum MediaTypeInstance {
    
    JSON = "JSON",
    JSON_LD = "LD_PLUS_JSON",
    N_Quads = "N_QUADS",
    N_Triples = "N_TRIPLES",
    RDFSOLIDUSXML = "RDF_PLUS_XML",
    SPARQL_1FULL_STOP1_Query_Results_JSON = "SPARQL_RESULTS_PLUS_JSON",
    SPARQL_1FULL_STOP1_Query_Results_XML = "SPARQL_RESULTS_PLUS_XML",
    TriG = "TRIG",
    JPG = "JPG",
    PNG = "PNG",
    CSV = "CSV",
    HTML = "HTML",
    Plain_Text = "PLAIN",
    Turtle = "TURTLE",
};
/**
* Named SHACL prefix declarations from the gist ontology.
*/
export enum PrefixDeclarationInstance {
    
    /** Prefix 'gist' for namespace <https://w3id.org/semanticarts/ns/ontology/gist/>. */
    gist = "PREFIXDECLARATION_GIST",
    /** Prefix 'owl' for namespace <http://www.w3.org/2002/07/owl#>. */
    owl = "PREFIXDECLARATION_OWL",
    /** Prefix 'rdf' for namespace <http://www.w3.org/1999/02/22-rdf-syntax-ns#>. */
    rdf = "PREFIXDECLARATION_RDF",
    /** Prefix 'rdfs' for namespace <http://www.w3.org/2000/01/rdf-schema#>. */
    rdfs = "PREFIXDECLARATION_RDFS",
    /** Prefix 'sh' for namespace <http://www.w3.org/ns/shacl#>. */
    sh = "PREFIXDECLARATION_SH",
    /** Prefix 'skos' for namespace <http://www.w3.org/2004/02/skos/core#>. */
    skos = "PREFIXDECLARATION_SKOS",
    /** Prefix 'xsd' for namespace <http://www.w3.org/2001/XMLSchema#>. */
    xsd = "PREFIXDECLARATION_XSD",
};


/**
 * An agreement having a balance.
 */
export interface Account extends Agreement {
}


/**
 * A reference to a place (real or virtual) that can be located by some routing algorithm and where messages or things can be sent or received.
 */
export interface Address extends Content {
}


/**
 * A category indicating the context or manner in which an address may be used.
 */
export interface AddressUsageType extends Category {
}


/**
 * A mutually understood arrangement in which two or more parties make commitments to one another.
 */
export interface Agreement extends Intention {
}


/**
 * A measurable characteristic.
 */
export interface Aspect extends GistThing {
}


/**
 * A temporal relationship between an assignee, the thing assigned, and the resource that made the assignment.
 */
export interface Assignment extends TemporalRelation {
}


/**
 * A category indicating the nature of an activity.
 */
export interface Behavior extends Category {
}


/**
 * A relatively permanent man-made structure situated on a plot of land, having a roof and walls, commonly used for dwelling, entertaining, or working.
 */
export interface Building extends Landmark {
}


/**
 * Any combination of descriptions of things offered together.
 */
export interface BundledCatalogItem extends CatalogItem {
}


/**
 * A description of a product or service to be delivered, given in a sufficient level of detail that a receiver could determine whether delivery constituted discharge of the obligation to deliver.
 */
export interface CatalogItem extends Specification {
}


/**
 * A concept or label used to categorize other instances without specifying any formal semantics.
 */
export interface Category extends GistThing {
}


/**
 * A grouping of things.
 */
export interface Collection extends Composite {
}


/**
 * A promise made by a single party to one or more parties to do or not do something or act in a particular way.
 */
export interface Commitment extends Intention {
}


/**
 * Something that, while having an independent existence, is inherently part of or designed to be part of a larger entity, such as a system or network.
 */
export interface Component extends GistThing {
}


/**
 * Something which is made up of various parts or elements that are independently identifiable.
 */
export interface Composite extends GistThing {
}


/**
 * An event that has started but has not yet ended.
 */
export interface ContemporaryEvent extends Event {
}


/**
 * Information available in some medium.
 */
export interface Content extends GistThing {
}


/**
 * Content reduced to text, audio, etc.
 */
export interface ContentExpression extends Content {
}


/**
 * An event with a probability of happening in the future, and usually dependent upon some other event or condition.
 */
export interface ContingentEvent extends Event {
}


/**
 * An obligation that is not yet firm. There is some contingent event whose occurrence will cause the obligation to become firm.
 */
export interface ContingentObligation extends Commitment {
}


/**
 * An agreement which can be enforced by law.
 */
export interface Contract extends Agreement {
}


/**
 * A specification of some aspect of a contract.
 */
export interface ContractTerm extends Specification {
}


/**
 * A collection of terms approved and managed by some organization or person.
 */
export interface ControlledVocabulary extends Collection {
}


/**
 * A geographic region governed by exactly one country government.
 */
export interface CountryGeoRegion extends GovernedGeoRegion {
}


/**
 * A government organization which asserts both sovereignty (i.e., it is not governed by some other government organization) and governance over an entity generally recognized as a country.
 */
export interface CountryGovernment extends GovernmentOrganization {
}


/**
 * The difficulty of reversing a commitment.
 */
export interface DegreeOfCommitment extends Category {
}


/**
 * An event whose purpose is to establish a specific result, value, or outcome, usually by research, measuring, evaluating, or calculating.
 */
export interface Determination extends Event {
}


/**
 * An area of study or practice.
 */
export interface Discipline extends Category {
}


/**
 * An address referring to a locatable virtual place that does not physically exist but is made by software or electronics to appear to do so.
 */
export interface ElectronicAddress extends Address {
}


/**
 * A category indicating a kind of electronic address. Such a category is usually based on the technology that enables routing to the address referent.
 */
export interface ElectronicAddressType extends Category {
}


/**
 * Human-made, tangible property other than land or buildings used to perform a task or activity.
 */
export interface Equipment extends PhysicalIdentifiableItem {
}


/**
 * A category of equipment.
 */
export interface EquipmentType extends Category {
}


/**
 * Something that occurs over a period of time, often characterized as an activity being carried out by some person, organization, or software application or brought about by natural forces.
 */
export interface Event extends GistThing {
}


/**
 * A characterization of an event that might happen.
 */
export interface EventSpecification extends Specification {
}


/**
 * Content encoded in a specific format, but existing as data independent of any particular physical medium.
 */
export interface FormattedContent extends ContentExpression {
}


/**
 * The activity that a human-made item is intended to perform.
 */
export interface Function extends Intention {
}


/**
 * The real-world media type for content.
 */
export interface GeneralMediaType extends Category {
}


/**
 * A physical location, with the earth as a frame of reference.
 */
export interface GeoLocation extends GistThing {
}


/**
 * An individual point on or above the Earth's surface, identified by latitude, longitude and altitude. Altitude is the distance measured from sea level. If altitude is missing, the point is assumed to be at the Earth's surface. These points are described using decimal latitude/longitude.
 */
export interface GeoPoint extends GeoLocation {
}


/**
 * A bounded region (or set of regions) on the surface of the Earth.
 */
export interface GeoRegion extends GeoLocation {
}


/**
 * An ordered set of geographic points that defines a path from a starting point to an ending point.
 */
export interface GeoRoute extends OrderedCollection {
}


/**
 * A three-dimensional space on or near the surface of the Earth.
 */
export interface GeoVolume extends GeoLocation {
}


/**
 * A geographic region governed by at least one government organization.
 */
export interface GovernedGeoRegion extends GeoRegion {
}


/**
 * An independent organization exercising political and/or regulatory authority over a political unit, people, geographical region, etc., as well as performing certain functions for this unit or body.
 */
export interface GovernmentOrganization extends Organization {
}


/**
 * An event which occurred in time, with an actual end earlier than the present moment.
 */
export interface HistoricalEvent extends Event {
}


/**
 * Content that is used to uniquely identify something or someone.
 */
export interface ID extends Content {
}


/**
 * An intangible work, invention, or concept, independent of its being expressed in text, audio, video, image, or live performance. IP can also be tacit knowledge, know-how, or skill.
 */
export interface IntellectualProperty extends GistThing {
}


/**
 * A goal, desire, or aspiration.
 */
export interface Intention extends GistThing {
}


/**
 * An organization whose members are government organizations. This can comprise regional, municipal, state/province, or national level entities.
 */
export interface IntergovernmentalOrganization extends Organization {
}


/**
 * An abstract concept that arises from the distillation of experience. It is similar to a category but, rather than being a simple tag, it has rich structure.
 */
export interface KnowledgeConcept extends IntellectualProperty {
}


/**
 * Something permanently attached to the Earth.
 */
export interface Landmark extends PhysicalIdentifiableItem {
}


/**
 * A recognized, organized set of symbols and grammar.
 */
export interface Language extends GistThing {
}


/**
 * Something that is currently, or at some point in time was, alive.
 */
export interface LivingThing extends PhysicalIdentifiableItem {
}


/**
 * The amount of a measurable characteristic (aspect).
 */
export interface Magnitude extends GistThing {
}


/**
 * A digitized type that computer applications can recognize.
 */
export interface MediaType extends Category {
}


/**
 * A physical material on which a work can be rendered, represented, or implemented.
 */
export interface Medium extends Category {
}


/**
 * A specific instance of content sent from a sender to at least one other recipient.
 */
export interface Message extends ContentExpression {
}


/**
 * A composite consisting of nodes connected by links.
 */
export interface Network extends Composite {
}


/**
 * An abstract representation of the connection between two or more nodes in a network.
 */
export interface NetworkLink extends Component {
}


/**
 * A node in a network.
 */
export interface NetworkNode extends Component {
}


/**
 * A contingent commitment to buy, sell, swap or provide one or more described or identified goods or services in exchange for another (or others).
 */
export interface Offer extends ContingentObligation {
}


/**
 * A collection whose members are ordered in some way.
 */
export interface OrderedCollection extends Collection {
}


/**
 * A member of an ordered collection serving as a proxy for a real world item, which can appear in different orders in different collections. The ordered member appears in exactly one ordered collection.
 */
export interface OrderedMember extends Component {
}


/**
 * A structured entity formed to achieve specific goals, typically involving members with defined roles.
 */
export interface Organization extends GistThing {
}


/**
 * A description of things one is permitted to do.
 */
export interface Permission extends Intention {
}


/**
 * A human being who was or is alive.
 */
export interface Person extends LivingThing {
}


/**
 * A category indicating the type of an action based on its effect in the physical world.
 */
export interface PhysicalActionType extends Category {
}


/**
 * An address that refers to a locatable place within the physical universe.
 */
export interface PhysicalAddress extends Address {
}


/**
 * A category indicating local customary characterizations of physical addresses.
 */
export interface PhysicalAddressType extends Category {
}


/**
 * An event that can be said to have occurred at some place in space.
 */
export interface PhysicalEvent extends Event {
}


/**
 * A discrete physical object which, if subdivided, will result in parts that are distinguishable in nature from the whole and in general also from the other parts.
 */
export interface PhysicalIdentifiableItem extends GistThing {
}


/**
 * An undifferentiated amount of physical material which, when subdivided, results in each part being indistinguishable in nature from the whole and from every other part.
 */
export interface PhysicalSubstance extends GistThing {
}


/**
 * Any of many ways of categorizing products.
 */
export interface ProductCategory extends Category {
}


/**
 * A description of something that could be physically warehoused or digitally stored and physically or digitally delivered.
 */
export interface ProductSpecification extends CatalogItem {
}


/**
 * A task, usually of longer duration, made up of other tasks.
 */
export interface Project extends Task {
}


/**
 * A magnitude that was neither measured nor estimated but set by fiat.
 */
export interface ReferenceValue extends Magnitude {
}


/**
 * Content expressed via some physical medium.
 */
export interface RenderedContent extends FormattedContent {
}


/**
 * The obligation of a person or organization to behave in a certain way.
 */
export interface Requirement extends Intention {
}


/**
 * A description of things one is prevented from doing.
 */
export interface Restriction extends Intention {
}


/**
 * An event with a planned start datetime.
 */
export interface ScheduledEvent extends Event {
}


/**
 * A task with a planned start datetime.
 */
export interface ScheduledTask extends ScheduledEvent {
}


/**
 * Superclass for all types of metadata.
 */
export interface SchemaMetaData extends GistThing {
}


/**
 * A description of something that can be done for a person or organization (which produces some form of an act).
 */
export interface ServiceSpecification extends CatalogItem {
}


/**
 * The set of characteristics and constraints on their values that specify what it means to be a particular type of thing, such as a material, product, service or event. A specification is sufficiently precise to allow evaluating conformance to the specification.
 */
export interface Specification extends Intention {
}


/**
 * The government of a governed geographic region other than a country which is under the direct or indirect control of a country government.
 */
export interface SubCountryGovernment extends GovernmentOrganization {
}


/**
 * A composite made up of interacting or interdependent components that together operate as a whole.
 */
export interface System extends Composite {
}


/**
 * A term in a folksonomy used to categorize things. Tags can be made up on the fly by users.
 */
export interface Tag extends Category {
}


/**
 * An activity or piece of work that is either proposed, planned, scheduled, underway, or completed.
 */
export interface Task extends Event {
}


/**
 * An outline of a task of a particular type, which is the basis for executing such tasks.
 */
export interface TaskTemplate extends Template {
}


/**
 * Something used to make objects in its own image.
 */
export interface Template extends GistThing {
}


/**
 * A relationship existing for a period of time.
 */
export interface TemporalRelation extends GistThing {
}


/**
 * Content expressed as a written sequence of characters.
 */
export interface Text extends ContentExpression {
}


/**
 * A span of time with a known start time, end time, and duration. As long as two of the three are known, the third can be inferred.
 */
export interface TimeInterval extends GistThing {
}


/**
 * An exchange or transfer of goods, services, or funds.
 */
export interface Transaction extends Event {
}


/**
 * A collection of units of measure that can all be used to measure the same aspects.
 */
export interface UnitGroup extends Collection {
}


/**
 * A standard amount used to measure or specify things.
 */
export interface UnitOfMeasure extends GistThing {
}


/**
 * Mixin providing universal slots applicable to any GIST entity. Covers OWL properties with no rdfs:domain (open-world).
 */
export interface GistThing {
    /** Relates an individual to (one of) its name(s). */
    name?: string,
    /** A statement about someone or something's attributes or characteristics. */
    description?: string,
}



