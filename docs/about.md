# About gist

This schema is a LinkML rendering of [gist](https://www.semanticarts.com/gist/),
Semantic Arts' minimalist upper ontology for the enterprise, from release 14.1.0.

## License and attribution

gist is published by Semantic Arts under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This schema is
derived from the 14.1.0 release: its OWL modules are converted to LinkML, its
annotations merged in, and SSSOM mappings to other vocabularies added. Semantic
Arts asks that terms used from gist stay in the gist namespace and that nobody
else defines terms there. This schema holds to both.

## Namespaces

| Prefix | Namespace | Holds |
| --- | --- | --- |
| `gist` | `https://w3id.org/semanticarts/ns/ontology/gist/` | gist's classes and properties (Semantic Arts) |
| `gistd` | `https://w3id.org/semanticarts/ns/data/gist/` | gist's named individuals (Semantic Arts) |
| `gist_linkml` | `https://w3id.org/lmodel/gist/` | what this rendering adds: schema documents, the `GistThing` mixin, enums, subsets, SHACL shapes, LinkML element definitions |

## How the classes carry gist's properties

A property's slot belongs to each class its `rdfs:domain` names, and to that
class's subclasses. gist declares most of its properties without a domain, so
OWL lets them describe any individual; their 89 slots sit on the `GistThing`
mixin, which every class takes. gist's `domainIncludes` and `rangeIncludes`
hints stay annotations on each slot and never limit where it is used, since
gist's own axioms use properties outside them.

## Where the schema is narrower than gist

The JSON Schema, the Python models and the SHACL shapes check data more
strictly than gist's OWL in three ways:

- Each datatype property holds one value, as LinkML's slots do by default,
  though gist declares only `conversionFactor`, `conversionOffset` and
  `uniqueText` functional. A thing with two names, which gist allows, fails.
- A datatype property gist leaves without a range, such as `name`, takes a
  string, so the shapes reject a language-tagged literal.
- No class has an identifier slot, so a slot ranged over a gist class, such
  as `has_unit_of_measure`, takes the individual written out in full, not
  its IRI. A slot ranged over `Any` takes either.

For reasoning over gist itself, use Semantic Arts' own OWL release. The OWL
generated here is a projection of the LinkML schema. It adds restrictions
gist does not make, such as at most one value for each single-valued slot,
and an object property gist leaves unranged, or ranges over a union, has
`linkml:Any` in its range.

# References

- [gist](https://www.semanticarts.com/gist/)
- [gist on GitHub](https://github.com/semanticarts/gist)
