# About gist

A LinkML rendering of [gist](https://www.semanticarts.com/gist/), Semantic
Arts' minimalist upper ontology for the enterprise, from release 14.1.0.

## License and attribution

gist is published by Semantic Arts under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This schema is
derived from the 14.1.0 release: its OWL modules are converted to LinkML, its
annotations folded in, and SSSOM mappings to other vocabularies added. Semantic
Arts asks that terms used from gist stay in the gist namespace and that nobody
else defines terms there; this schema does both.

## Namespaces

| Prefix | Namespace | Holds |
| --- | --- | --- |
| `gist` | `https://w3id.org/semanticarts/ns/ontology/gist/` | gist's classes and properties (Semantic Arts) |
| `gistd` | `https://w3id.org/semanticarts/ns/data/gist/` | gist's named individuals (Semantic Arts) |
| `gist_linkml` | `https://w3id.org/lmodel/gist/` | what this rendering adds: schema documents, the `GistThing` mixin, enums, subsets, SHACL shapes, LinkML element definitions |

For reasoning over gist itself, use Semantic Arts' own OWL release; the OWL
generated here is a projection of the LinkML schema.

# References

- [gist](https://www.semanticarts.com/gist/)
- [gist on GitHub](https://github.com/semanticarts/gist)
