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
    /** Relates an aspect to a unit group. The aspect can be measured using any of the members of the unit group. */
    has_unit_group?: UnitGroup[],
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
    /** Subject matter of a document. */
    is_about?: Any[],
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
    /** Relates one geographic location to another that contains it. */
    is_geo_contained_in?: GeoLocation[],
}


/**
 * An individual point on or above the Earth's surface, identified by latitude, longitude and altitude. Altitude is the distance measured from sea level. If altitude is missing, the point is assumed to be at the Earth's surface. These points are described using decimal latitude/longitude.
 */
export interface GeoPoint extends GeoLocation {
    /** Degrees above or below the equator. */
    latitude?: number,
    /** Degrees from the prime meridian. */
    longitude?: number,
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
    /** Relates an intention to behavior that it prohibits. */
    prevents?: Behavior[],
    /** Relates an intention to a behavior that it forbids or seeks to prevent. */
    prohibits?: Behavior[],
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
    /** Relates a living thing to its biological parent. */
    has_biological_parent?: LivingThing[],
}


/**
 * The amount of a measurable characteristic (aspect).
 */
export interface Magnitude extends GistThing {
    /** Relates a magnitude to its unit of measure. */
    has_unit_of_measure?: UnitOfMeasure[],
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
    /** Relates the first member of an ordered collection to the collection. */
    is_first_member_of?: OrderedCollection[],
    /** Links a member of an ordered collection to the real-world item it represents in that collection. */
    provides_order_for?: Any,
}


/**
 * A structured entity formed to achieve specific goals, typically involving members with defined roles.
 */
export interface Organization extends GistThing {
    /** Relates a party to something that it possesses and controls. */
    owns?: Any[],
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
    /** Relates a party to something that it possesses and controls. */
    owns?: Any[],
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
    /** The exponent of ampere in a product of powers of base units. */
    exponent_of_ampere?: string,
    /** The exponent of bit in a product of powers of base units. */
    exponent_of_bit?: string,
    /** The exponent of candela in a product of powers of base units. */
    exponent_of_candela?: string,
    /** The exponent of Kelvin in a product of powers of base units. */
    exponent_of_kelvin?: string,
    /** The exponent of kilogram in a product of powers of base units. */
    exponent_of_kilogram?: string,
    /** The exponent of meter in a product of powers of base units. */
    exponent_of_meter?: string,
    /** The exponent of mole in a product of powers of base units. */
    exponent_of_mole?: string,
    /** The exponent of number in a product of powers of base units. */
    exponent_of_number?: string,
    /** Indicates whether a unit of measure can be expressed in terms of the standard exponents (as shown in the examples). */
    exponent_of_other?: string,
    /** The exponent of radian in a product of powers of base units. */
    exponent_of_radian?: string,
    /** The exponent of second in a product of powers of base units. */
    exponent_of_second?: string,
    /** The exponent of steradian in a product of powers of base units. */
    exponent_of_steradian?: string,
    /** The exponent of US Dollar in a product of powers of base units. */
    exponent_of_us_dollar?: string,
}


/**
 * A standard amount used to measure or specify things.
 */
export interface UnitOfMeasure extends GistThing {
    /** A value that relates a unit of measure to units of the International System of Units. */
    conversion_factor?: string,
    /** A value used along with a conversion factor to relate a unit to its corresponding unit in the International System of Units. In the equation below, the conversion offset is 459.669607 and the conversion factor is 5/9.

y degrees Fahrenheit = (y + 459.669607) x 5/9 degrees Kelvin

To convert from Fahrenheit to Kelvin, first add the offset and then multiply by the conversion factor.

To convert from Kelvin to Fahrenheit, reverse the steps: first divide by the conversion factor and then subtract the offset. */
    conversion_offset?: string,
    /** The exponent of ampere in a product of powers of base units. */
    exponent_of_ampere?: string,
    /** The exponent of bit in a product of powers of base units. */
    exponent_of_bit?: string,
    /** The exponent of candela in a product of powers of base units. */
    exponent_of_candela?: string,
    /** The exponent of Kelvin in a product of powers of base units. */
    exponent_of_kelvin?: string,
    /** The exponent of kilogram in a product of powers of base units. */
    exponent_of_kilogram?: string,
    /** The exponent of meter in a product of powers of base units. */
    exponent_of_meter?: string,
    /** The exponent of mole in a product of powers of base units. */
    exponent_of_mole?: string,
    /** The exponent of number in a product of powers of base units. */
    exponent_of_number?: string,
    /** Indicates whether a unit of measure can be expressed in terms of the standard exponents (as shown in the examples). */
    exponent_of_other?: string,
    /** The exponent of radian in a product of powers of base units. */
    exponent_of_radian?: string,
    /** The exponent of second in a product of powers of base units. */
    exponent_of_second?: string,
    /** The exponent of steradian in a product of powers of base units. */
    exponent_of_steradian?: string,
    /** The exponent of US Dollar in a product of powers of base units. */
    exponent_of_us_dollar?: string,
}


/**
 * Mixin that gives every gist class the slots of the properties gist declares without a domain, since OWL lets those describe any individual.
 */
export interface GistThing {
    /** The actual date that something ended, with precision of one day. */
    actual_end_date?: string,
    /** The actual date and time that something ended, with no implied precision. */
    actual_end_date_time?: string,
    /** The actual time that something ended, expressed as a system time used for timestamps. */
    actual_end_microsecond?: string,
    /** The actual date and time that something ended, with precision of one minute. */
    actual_end_minute?: string,
    /** The actual date that something ended, with precision of one year. */
    actual_end_year?: string,
    /** The actual date that something started, with precision of one day. */
    actual_start_date?: string,
    /** The actual date and time that something started, with no implied precision. */
    actual_start_date_time?: string,
    /** The actual time that something started, expressed as a system time used for timestamps. */
    actual_start_microsecond?: string,
    /** The actual date and time that something started, with precision of one minute. */
    actual_start_minute?: string,
    /** The actual date that something started, with precision of one year. */
    actual_start_year?: string,
    /** Relates a permission to a particular activity or type of activity it allows. */
    allows?: Any[],
    /** The date and time at which something did or will occur, with variants for precision, start and end, and actual vs. planned. */
    at_date_time?: string,
    /** The date some living thing was or will be born, with precision of one day. */
    birth_date?: string,
    /** Relates something to the originating agent. */
    comes_from_agent?: Any[],
    /** Relates something to its place of origin. */
    comes_from_place?: Any[],
    /** The subject is consistent with or satisfies the requirements, rules, or expectations established by the object. */
    conforms_to?: Any[],
    /** Relates an entity containing textual information to the string constituting that textual information. */
    contained_text?: string,
    /** The subject helps achieve or fulfill the goals or functions of the object. */
    contributes_to?: Any[],
    /** The date some living thing died. */
    death_date?: string,
    /** A statement about someone or something's attributes or characteristics. */
    description?: string,
    /** Encoded text produced from readable data by an algorithm so that it can only be understood or restored with a decryption key. */
    encrypted_text?: string,
    /** The date and time that something ends. */
    end_date_time?: string,
    /** Relates something to the agent that receives it. */
    goes_to_agent?: Any[],
    /** Relates something to its destination place. */
    goes_to_place?: Any[],
    /** Relates a magnitude to another magnitude that describes its accuracy. */
    has_accuracy?: Magnitude,
    /** Relates an aspect to another aspect that is an additive component of it. */
    has_addend?: Any[],
    /** Relates something to its physical or electronic address. */
    has_address?: Address[],
    /** Relates a magnitude to its aspect (measurable characteristic). */
    has_aspect?: Aspect,
    /** Relates a thing to another thing with a broader meaning. */
    has_broader?: Any[],
    /** Relates a thing to another thing with a broader meaning, when there is no intermediate between them. */
    has_direct_broader?: Any[],
    /** Relates a unit of measure to another unit of measure that is a divisor, or relates an aspect to another aspect that is a divisor. */
    has_divisor?: Any[],
    /** Relates something to the participant that provides it. */
    has_giver?: Any[],
    /** Relates something to the end towards which it directs effort. */
    has_goal?: Any[],
    /** Relates a position to the thing or person that currently holds that position. */
    has_incumbent?: Any[],
    /** Relates a thing to a magnitude. */
    has_magnitude?: Magnitude[],
    /** Relates a unit of measure to another unit of measure that is a factor, or relates an aspect to another aspect that is a factor. */
    has_multiplier?: Any[],
    /** Relates a child category to a parent category in an informal (e.g., faceted) hierarchy. */
    has_navigational_parent?: Any[],
    /** Relates something (e.g. an agreement) to things that play a role, or take part or are otherwise involved in some way. */
    has_participant?: Any[],
    /** Relates an event, agreement, or obligation to a participating person or organization. */
    has_party?: Any[],
    /** Relates something to its physical location. */
    has_physical_location?: GeoLocation[],
    /** Relates something to the participant that receives or is intended to receive it. */
    has_recipient?: Any[],
    /** Relates an aspect to another aspect that is a subtracted component of it. */
    has_subtrahend?: Any[],
    /** Relates a thing to a unique other thing with a broader meaning. */
    has_unique_broader?: Any[],
    /** Relates a subject category to a unique parent category in an informal (e.g., faceted) hierarchy. */
    has_unique_navigational_parent?: Any[],
    /** A text string that identifies an individual. */
    id_text?: string,
    /** Relates an affected thing to the source of the effect. */
    is_affected_by?: Any[],
    /** Relates something to whomever or whatever assigns or distributes it. */
    is_allocated_by?: Any[],
    /** Relates an assignment to the resource it assigns. */
    is_assignment_of?: Any[],
    /** Relates something (typically an assignment) to the thing the resource is assigned to, such as a project, position, organization, pay rate, or billing rate. */
    is_assignment_to?: Any[],
    /** The object is a foundation for, a starting point for, gave rise to, or justifies the subject. */
    is_based_on?: Any[],
    /** Relates something to a taxonomy term or other less formally defined classification. */
    is_categorized_by?: Any[],
    /** A non-owning, non-causal, non-subordinate (i.e., peer-to-peer) relationship. */
    is_connected_to?: Any[],
    /** The relationship between a part and a whole where the part has independent existence and there are no other parts in between. */
    is_direct_part_of?: Any[],
    /** Relates something to the language it is expressed in. */
    is_expressed_in?: Any[],
    /** Relates an entity to another entity that controls, directs, determines or has a guiding influence or authority over it. */
    is_governed_by?: Any[],
    /** Relates something to a content object that uniquely identifies it. */
    is_identified_by?: ID[],
    /** Relates something to a substance that it is made up of. */
    is_made_up_of?: PhysicalSubstance[],
    /** Relates a member individual to the thing, such as a collection or organization, that it is a member of. */
    is_member_of?: Any[],
    /** The relationship between a part and a whole where the part has independent existence. */
    is_part_of?: Any[],
    /** Relates something to the thing that created, composed, or brought it into existence. */
    is_produced_by?: Any[],
    /** Relates something to a party that formally acknowledges its existence, validity, or legality. */
    is_recognized_by?: Any[],
    /** The date that something was posted (which is not necessarily the date it occurred). It must be after the date of occurrence, but could be before or after the planned date. */
    is_recorded_at?: string,
    /** Relates content to the media on which it is rendered. */
    is_rendered_on?: Any[],
    /** Relates a contingency, such as an event or obligation, to the event that gives rise to it. */
    is_triggered_by?: Any[],
    /** Relates a law, contract, etc., to the system of law or government which has the power, right, or authority to interpret and apply it. */
    is_under_jurisdiction_of?: Any[],
    /** Relates a network link to a network node that it connects to another node. Used when the connection is undirected or the direction is not known. */
    links?: Any[],
    /** Relates a network link to its origin network node. Unlike the superproperty, this represents a directed connection. */
    links_from?: Any[],
    /** Relates a network link to its destination network node. Unlike the superproperty, this represents a directed connection. */
    links_to?: Any[],
    /** Relates an individual to (one of) its name(s). */
    name?: string,
    /** The actual value of a magnitude. */
    numeric_value?: string,
    /** Relates something, such as an event, to the geographic location where it did, does, or will happen. */
    occurs_in?: Any[],
    /** Relates an offer to the thing being made available for exchange. */
    offers_to_provide?: Any[],
    /** Relates an offer to the thing expected in return for the offered item. */
    offers_to_receive?: Any[],
    /** The date that something is or was planned to end, with precision of one day. */
    planned_end_date?: string,
    /** The date that something is or was planned to end, with no implied precision. */
    planned_end_date_time?: string,
    /** The date and time that something is or was planned to end, with precision of one minute. */
    planned_end_minute?: string,
    /** The date that something is or was planned to end, with precision of one year. */
    planned_end_year?: string,
    /** The date that something is or was planned to start, with precision of one day. */
    planned_start_date?: string,
    /** The date and time that something is or was planned to start, with no implied precision. */
    planned_start_date_time?: string,
    /** The date and time that something is or was planned to start, with precision of one minute. */
    planned_start_minute?: string,
    /** The date that something is or was planned to start, with precision of one year. */
    planned_start_year?: string,
    /** A generic ordering relation indicating that the subject comes before the object. */
    precedes?: Any[],
    /** A generic ordering relation indicating that the subject comes immediately before the object. */
    precedes_directly?: Any[],
    /** Relates something to another resource that it points to, indicates, or references. */
    refers_to?: Any[],
    /** The subject needs the object or makes it necessary, mandatory, or compulsory. */
    requires?: Any[],
    /** A number that specifies the position of an element within a series. */
    sequence?: number,
    /** The date and time that something starts. */
    start_date_time?: string,
    /** A symbol for something using only ASCII characters. */
    symbol?: string,
    /** The unique string value of some content object, to be used when there is no possibility of having more than one value. */
    unique_text?: string,
}


/**
 * Any individual: the range of an object property gist leaves open.
 */
export interface Any {
}



