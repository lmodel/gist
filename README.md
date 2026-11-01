<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# gist

GIST, the Semantic Arts Upper Enterprise Ontology (LinkML)

This repository is an independent LinkML rendering of [gist](https://github.com/semanticarts/gist), Semantic Arts' upper enterprise ontology. It is not a Semantic Arts release, and it defines nothing in gist's namespace.

> **Only want to ask?** Install `ktl-docent` into any agent you use, by a route from [the install page](https://w3id.org/ktl/docs/install/), and ask it about this repository. It answers from the bundle and says how far each answer has been checked.
>
> **Agents:** if `.lokf/knowledge/index.md` exists, read it first. `llms.txt` says how to weigh it.

## Documentation Website

[https://lmodel.github.io/gist](https://lmodel.github.io/gist)

## Repository Structure

* [docs/](docs/): the documentation pages the website shows
  * [elements/](docs/elements/): generated schema documentation
* [examples/](examples/): examples of using the schema
* [project/](project/): generated project files (do not edit them)
* [src/](src/): source files (edit these)
  * [gist](src/gist)
    * [schema/](src/gist/schema): the LinkML schema (edit this)
    * [datamodel/](src/gist/datamodel): the generated Python datamodel
* [tests/](tests/): Python tests
  * [data/](tests/data): example data
* [website/](website/): the documentation website, an Astro Starlight site built from the README, `docs/`, the schema's pages and the knowledge bundle

## Developer Tools

The project's predefined recipes run with the command runner [just](https://github.com/casey/just/).
To list them, run `just` or `just --list`.

## Knowledge Trust Ladder (KTL)

`.lokf/` holds this project's [KTL](https://w3id.org/ktl/) knowledge bundle, which validates against LOKF's own schema.

Each release also attaches `schema-<tag>-gist.yaml`, the copy of `gist_core.yaml` that `lokf adapt` writes and `just gen-lokf-copy` builds, for a bundle whose domain schema imports gist. Save it beside `lokf.yaml` as `gist_core_lokf.yaml` and import `gist_core_lokf`. The copy roots these classes on LOKF's `Concept`, so a concept may name any gist class but `GistThing` and `Any` as its `type`:

```text
Aspect, Category, Component, Composite, Content, Event, GeoLocation, IntellectualProperty, Intention, Language, Magnitude, GistOrganization, PhysicalIdentifiableItem, PhysicalSubstance, SchemaMetaData, Template, TemporalRelation, TimeInterval, UnitOfMeasure
```

`lokf.yaml` defines `Person`, `Organization`, `name`, `description` and `license`, so the copy renames them `GistPerson`, `GistOrganization`, `gist_name`, `gist_description` and `gist_license`, and each keeps its gist IRI. A slot ranged over a gist class takes the IRI of the concept it names.

## License and attribution

gist is Semantic Arts' upper ontology, published under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). [scripts/gist_to_linkml.py](scripts/gist_to_linkml.py) converts the OWL modules of the gist 14.1.0 release to LinkML, and SSSOM mappings to other vocabularies come from [src/gist/mappings/](src/gist/mappings). The release is kept unmodified in [upstream/](upstream/gist14.1.0_webDownload) with its [LICENSE.txt](upstream/gist14.1.0_webDownload/LICENSE.txt). The code is under the Apache License 2.0 ([LICENSE](LICENSE)), and [NOTICE](NOTICE) lists every third-party work it carries or derives from.

Semantic Arts asks that terms used from gist stay in the gist namespace and that nobody else defines terms there. The schema and every generated artefact hold to both:

* **`gist:`** (`https://w3id.org/semanticarts/ns/ontology/gist/`) and **`gistd:`** are Semantic Arts' namespaces. Every gist class, property and individual keeps its gist IRI.
* **`gist_linkml:`** (`https://w3id.org/lmodel/gist/`) is this project's namespace. It holds only what the LinkML rendering adds, such as the `GistThing` mixin, the enums, the subsets and the SHACL shapes.
* [tests/test_schema_validation.py](tests/test_schema_validation.py) and [tests/test_generated_artifacts.py](tests/test_generated_artifacts.py) check both rules against the vendored release.

## Contributing and security

[CONTRIBUTING.md](CONTRIBUTING.md) is the checklist for a pull request and
for releasing. [AI_COVENANT.md](AI_COVENANT.md) sets the rules for AI-assisted
work. [SECURITY.md](SECURITY.md) says how to report a vulnerability.
[CHANGELOG.md](CHANGELOG.md) records the changes.

## Credits

This project uses the template [linkml-project-copier](https://github.com/linkml/linkml-project-copier).
