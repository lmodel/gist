<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# gist

GIST (Semantic Arts, Upper Enterprise Ontology) - LinkML Schema

This repository is an independent LinkML rendering of [gist](https://github.com/semanticarts/gist), Semantic Arts' upper enterprise ontology. It is not a Semantic Arts release, and it defines nothing in gist's namespace.

> **Only want to ask?** Install `ktl-docent` into any agent you use, by a route from [the install page](https://w3id.org/ktl/docs/install/), and ask it about this repository. It answers from the bundle and says how far each answer has been checked.
>
> **Agents:** if `.lokf/knowledge/index.md` exists, read it first. `llms.txt` says how to weigh it.

## Documentation Website

[https://lmodel.github.io/gist](https://lmodel.github.io/gist)

## Repository Structure

* [docs/](docs/): documentation that mkdocs builds
  * [elements/](docs/elements/): generated schema documentation
* [examples/](examples/): examples of using the schema
* [project/](project/): generated project files (do not edit them)
* [src/](src/): source files (edit these)
  * [gist](src/gist)
    * [schema/](src/gist/schema): the LinkML schema (edit this)
    * [datamodel/](src/gist/datamodel): the generated Python datamodel
* [tests/](tests/): Python tests
  * [data/](tests/data): example data

## Developer Tools

The project's predefined recipes run with the command runner [just](https://github.com/casey/just/).
To list them, run `just` or `just --list`.

## License and attribution

gist is Semantic Arts' upper ontology, published under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This schema is
derived from the gist 14.1.0 release.
[scripts/gist_to_linkml.py](scripts/gist_to_linkml.py) converts its OWL modules
to LinkML. Their RDFS annotations and subclass assertions are merged into the
schema, and SSSOM mappings to other vocabularies are added from
[src/gist/mappings/](src/gist/mappings). The release is kept unmodified in
[upstream/](upstream/gist14.1.0_webDownload) with its
[LICENSE.txt](upstream/gist14.1.0_webDownload/LICENSE.txt). The code in this
repository is Apache-2.0 ([LICENSE](LICENSE)). [NOTICE](NOTICE) lists every
third-party work it carries or derives from, and is included in the package.

Semantic Arts also asks that terms used from gist stay in the gist namespace
and that nobody else defines terms there. The schema and every generated
artefact hold to both:

* **`gist:`** (`https://w3id.org/semanticarts/ns/ontology/gist/`) and
  **`gistd:`** are Semantic Arts' namespaces. Every gist class, property and
  individual keeps its gist IRI.
* **`gist_linkml:`** (`https://w3id.org/lmodel/gist/`) is this project's
  namespace. It holds only what the LinkML rendering adds: the schema
  documents, the `GistThing` mixin, the enums, the subsets, the SHACL shapes,
  and the LinkML element definitions the OWL links to the gist terms they
  render.
* Tests in [tests/test_schema_validation.py](tests/test_schema_validation.py)
  and [tests/test_generated_artifacts.py](tests/test_generated_artifacts.py)
  check both rules against the vendored release.

## Contributing and security

[CONTRIBUTING.md](CONTRIBUTING.md) is the checklist for a pull request and
for releasing. [AI_COVENANT.md](AI_COVENANT.md) sets the rules for AI-assisted
work. [SECURITY.md](SECURITY.md) says how to report a vulnerability.
[CHANGELOG.md](CHANGELOG.md) records the changes.

## Credits

This project uses the template [linkml-project-copier](https://github.com/linkml/linkml-project-copier).
